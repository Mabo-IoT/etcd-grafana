import json
import logging 
import falcon
import pendulum
import random

from web_server.data import QueryResponse, GrafanaQuery


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
        generate a targets list
        """
        targets = ["node_1", "node_2"]
        # targets = [
        #         {
        #         "text":"node_1",
        #         "value": "status",
        #         },
        #         {
        #         "text":"node_3",
        #         "value": "status",
        #         },
        #         ]
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
    def on_get(self, req:falcon.Request, resp:falcon.Response):
        resp.body = "this is a query api"
        resp.status = falcon.HTTP_200
    
    def on_post(self, req:falcon.Request, resp:falcon.Response):
        log.debug("Recived query post method")
        # log.debug("Recived request is:\n{} ".format(req))
        data = req.stream.read()
        data = json.loads(data)
        log.debug("Query request body is:\n {}".format(data))
        # request = GrafanaQuery.generate_query(data)

        # responese = QueryResponse()
        time = pendulum.now().int_timestamp
        response = [
            {   
                "target": "node_1",
                "datapoints":[
                    [random.randint(0,1), time]
                ]
            },
        ]
        
        resp.body = json.dumps(response)
        resp.status = falcon.HTTP_200

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