# airflow-providers-hive-zk

Provider for Hive for Airflow 2.X. It is using ZK discovery service to find Hive server.


Build and install locally:

```
python3 -m build

pip install airflow-providers-hive-zk --no-index --find-links file:///<path>/git/airflow_provider_hive_zk/dist/
```

Start airflow:

```
airflow webserver
```

Check if provider is registered and if new connection type has appeared.

Install:

```
pip install airflow-providers-hive-zk
```