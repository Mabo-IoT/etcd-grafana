## etcd-grafana
A simplejson datasource for grafana to show etcd data.
## Usage
1. install requirements;
```
pip install -r requirements.txt
```
2. start gunicorn server to host app;
```
gunicorn --reload web_server.app
```
3. ```/```,```/search```, ```/query```methods which grafana-simplejson datasource need are valid now.