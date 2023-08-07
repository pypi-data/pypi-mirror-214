#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from __future__ import annotations

import random
import re
from typing import Any, Optional

from kazoo.client import KazooClient
from kazoo.retry import KazooRetry
from airflow.providers.apache.hive.hooks.hive import HiveServer2Hook
from airflow.configuration import conf
from airflow.exceptions import AirflowException
from pyhive.hive import connect

_KV_PATTERN = re.compile('([^=;]*)=([^;]*);?')


class HiveZKHook(HiveServer2Hook):
    """
    Interact with Oracle SQL.

    :param oracle_conn_id: The :ref:`Oracle connection id <howto/connection:oracle>`
        used for Oracle credentials.
    """

    conn_name_attr = 'hiveserver2_conn_id'
    default_conn_name = 'hiveserver2_default'
    conn_type = 'hiveserver2zk'
    hook_name = 'Hive Server 2 Thrift with Zookeeper discovery'
    supports_autocommit = False

    def get_conn(self, schema: Optional[str] = None) -> Any:
        """Returns a Hive connection object."""
        username: Optional[str] = None
        password: Optional[str] = None

        db = self.get_connection(self.hiveserver2_conn_id)  # type: ignore

        auth_mechanism = db.extra_dejson.get('authMechanism', 'NONE')
        if auth_mechanism == 'NONE' and db.login is None:
            # we need to give a username
            username = 'airflow'
        kerberos_service_name = None
        zookeeper_name_space = None

        if conf.get('core', 'security') == 'kerberos':
            auth_mechanism = db.extra_dejson.get('authMechanism', 'KERBEROS')
            kerberos_service_name = db.extra_dejson.get(
                'kerberos_service_name', 'hive')
            zookeeper_name_space = db.extra_dejson.get(
                'zookeeper_name_space', 'hiveserver2')

        # pyhive uses GSSAPI instead of KERBEROS as a auth_mechanism identifier
        if auth_mechanism == 'GSSAPI':
            self.log.warning(
                "Detected deprecated 'GSSAPI' for authMechanism for %s. Please use 'KERBEROS' instead",
                self.hiveserver2_conn_id,  # type: ignore
            )
            auth_mechanism = 'KERBEROS'

        # Password should be set if and only if in LDAP or CUSTOM mode
        if auth_mechanism in ('LDAP', 'CUSTOM'):
            password = db.password

        # It randomly shuffles node information stored in zookeeper.
        remaining_nodes = self._get_hiveserver2_info_with_zookeeper(
            db.host, db.port, zookeeper_name_space)
        random.shuffle(remaining_nodes)

        # Access nodes sequentially and if they fail, access other nodes.
        while len(remaining_nodes) > 0:
            node = remaining_nodes.pop()
            host = node['host']
            port = node['port']

            try:
                conn = connect(
                    host=host,
                    port=port,
                    auth=auth_mechanism,
                    kerberos_service_name=kerberos_service_name,
                    username=db.login or username,
                    password=password,
                    database=schema or db.schema or 'default')
                return conn
            except:
                continue

        raise AirflowException("No servers available")

    def _get_hiveserver2_info_with_zookeeper(self, host, port, zookeeper_name_space='hiveserver2'):
        """Get hiveserver2 URL information from zookeeper."""

        hosts = host.split(',')
        zk_hosts = ','.join(
            list(map(lambda x: ':'.join([x, str(port)]), hosts)))

        conn_retry_policy = KazooRetry(max_tries=-1, delay=0.1, max_delay=0.1)
        cmd_retry_policy = KazooRetry(
            max_tries=3, delay=0.3, backoff=1, max_delay=1, ignore_expire=False)
        zk = KazooClient(
            hosts=zk_hosts, connection_retry=conn_retry_policy, command_retry=cmd_retry_policy)

        zk.start()
        children = zk.get_children('/' + zookeeper_name_space)
        nodes = self.get_hiveserver2_info(zk, zookeeper_name_space, children)
        zk.stop()
        zk.close()

        if len(nodes) == 0:
            from kazoo.exceptions import ZookeeperError
            raise ZookeeperError(
                "Can not find child in zookeeper path({}).".format(zookeeper_name_space))

        return nodes

    @staticmethod
    def get_hiveserver2_info(zk, zookeeper_name_space, children):
        result = list()
        for child in children:
            data_node = zk.get('/' + zookeeper_name_space + '/' + child)
            data = str(data_node[0], 'utf-8')
            matcher = _KV_PATTERN.findall(data)
            if data != '' and len(matcher) == 0:
                split_data = data.split(":")
                if len(split_data) == 2:
                    result.append(
                        {'host': split_data[0], 'port': split_data[1]})
            else:
                params = {}
                for m in matcher:
                    if len(m) == 2:
                        key = m[0]
                        value = m[1]
                        if key == 'hive.server2.thrift.bind.host':
                            params['host'] = value
                        elif key == 'hive.server2.thrift.port' or key == 'hive.server2.thrift.http.port':
                            params['port'] = value
                if 'host' in params and 'port' in params:
                    result.append(
                        {'host': params['host'], 'port': params['port']})
        return result
