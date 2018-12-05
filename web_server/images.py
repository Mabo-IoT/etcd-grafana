import json
import logging 
import falcon
import pendulum
import random

from web_server.data import QueryResponse, GrafanaQuery
from web_server.lib.etcd_database import EtcdWrapper


log = logging.getLogger(__name__)

class Resource:
    def on_get(self, req:falcon.Request, resp:falcon.Response):
        resp.body = None
        resp.status = falcon.HTTP_200


class Search:
    """
    request examples:
    {target}
    response examples:
    ["node_1", "node_2", "node_3"]
    """
    def __init__(self, conf:dict):
        self.etcd = EtcdWrapper(conf["etcd"])
        self.node_prefix = conf["app"]["node_prefix"]
        self.node_suffix = conf["app"]["node_suffix"]

    def on_get(self, req:falcon.Request, resp:falcon.Response):
        log.debug("Recived search get method:")
        # data = json.dumps(req)

        resp.status = falcon.HTTP_200
    
    def on_post(self, req:falcon.Request, resp:falcon.Response):
        
        log.debug("Recived search post method")
        log.debug("Recived request is:\n{} ".format(req))
        data = req.stream.read()
        log.debug("Recived request stream is:\n{} ".format(data))
        data = json.loads(data)
        log.debug("recived json data is:\n{}".format(data))
        log.debug(data['target'])

        ## generate targets list
        targets = self.genarate_targets()
        
        resp.body = json.dumps(targets)
        resp.status = falcon.HTTP_200
    
    def genarate_targets(self) -> list:
        """
        generate a targets list according to etcd monitor keys
        """
        etcd_result = self.etcd.read(self.node_prefix) # etcd monitor key dir
        log.debug(dir(etcd_result))
        log.debug(etcd_result.ttl)
        log.debug(etcd_result.expiration)
        nodes = etcd_result.children # dir children dir

        targets_key = [node.key for node in nodes] # key name
        log.debug("targets_key is {}".format(targets_key))
        targets = [key.split("/")[-1] for key in targets_key] # format name
        log.debug("targets is {}".format(targets))

        return targets

class Query:
    """
    request json sample:
    {
    "range": { "from": "2015-12-22T03:06:13.851Z", "to": "2015-12-22T06:48:24.137Z" },
    "interval": "5s",
    "targets": [
        { "refId": "B", "target": "upper_75" },
        { "refId": "A", "target": "upper_90" }
    ],
    "format": "json",
    "maxDataPoints": 2495 //decided by the panel
    }

    time series response sample:
    [
  {
    "target":"upper_75",
    "datapoints":[
      [622, 1450754160000],
      [365, 1450754220000]
    ]
  },
  {
    "target":"upper_90",
    "datapoints":[
      [861, 1450754160000],
      [767, 1450754220000]
    ]
  }
]
    """
    def __init__(self, conf:dict):
        self.etcd = EtcdWrapper(conf["etcd"])
        self.node_prefix = conf["app"]["node_prefix"]
        self.node_suffix = conf["app"]["node_suffix"]
        self.time_range = conf["app"]["time_range"]

    def on_get(self, req:falcon.Request, resp:falcon.Response):
        resp.body = "this is a query api"
        resp.status = falcon.HTTP_200
    
    def on_post(self, req:falcon.Request, resp:falcon.Response):
        log.debug("Recived query post method")
        # log.debug("Recived request is:\n{} ".format(req))
        data = req.stream.read()
        data = json.loads(data)
        log.debug("Query request body is:\n {}".format(data))
        request = GrafanaQuery.generate_query(data)
        log.debug(self.node_prefix)
        responses = self.generate_response(request)
        
        resp.body = json.dumps(responses)
        resp.status = falcon.HTTP_200
    
    def generate_response(self, request:dict) -> list:
        """
        generate json dict according to etcd
        """
        etcd_keys = request.etcd_keys(self.node_prefix, self.node_suffix)
        etcd_results = [self.etcd.read(key) for key in etcd_keys]
        query_responses = [QueryResponse.generate_response(result) for result in etcd_results]
        responses = [response.point(self.time_range) for response in query_responses]
        return responses

class Annotations:
    def on_get(self, req:falcon.Request, resp:falcon.Response):
        resp.body = "this is a annotations api"
        resp.status = falcon.HTTP_200

class Tag_keys:
    def on_get(self, req:falcon.Request, resp:falcon.Response):
        resp.body = "this is a tag-keys api"
        resp.status = falcon.HTTP_200

class Tag_values:
    def on_get(self, req:falcon.Request, resp:falcon.Response):
        resp.body = "this is a tag_value api"
        resp.status = falcon.HTTP_200