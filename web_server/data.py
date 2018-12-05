import logging
import pendulum
import json

from etcd import EtcdResult
from typing import Type, TypeVar

T = TypeVar('T', bound='GrafanaQuery')
S = TypeVar('S', bound='QueryResponse')

INVALID:int = 2
RUN:int = 1
STOP:int = 0
UNKNOWN:int = 3
UNDEFINED:int = 4


log = logging.getLogger(__name__)


class GrafanaQuery:
    def __init__(self, timeFrom:int, timeTo:int, targets:list,):
        self.timeFrom = timeFrom
        self.timeTo = timeTo
        self.targets = targets

    @classmethod
    def generate_query(cls:Type[T], data:dict) -> T:
        """
        parse request json to GrafanaQuery
        """
        timeFrom = pendulum.parse(data['range']['from']).int_timestamp
        timeTo = pendulum.parse(data['range']['to']).int_timestamp
        targets = [target['target'] for target in data['targets']]
        return cls(timeFrom, timeTo, targets)

    def etcd_keys(self, node_key:str, node_value:str) -> [str]:
        """
        generate etcd sql according to targets
        """

        keys = [node_key+'/'+target_node+node_value for target_node in self.targets]
        
        return keys


class QueryResponse:
    def __init__(self, node_name:str, timestamp:int, data:dict):
        self.node_name = node_name
        self.timestamp = timestamp
        self.data = data
        
    @classmethod
    def generate_response(cls:Type[S], data:EtcdResult) -> S:
        """
        generate response by etcd data
        """
        data = json.loads(data.value)
        
        return cls(data["node"], data["time"], data["data"])
        
    def point(self, time_range:int=1800) -> dict:
        """
        generate point by response and time_range;
        default time_range is 1800s;
        time_range to confirm if data is valid
        """
        point = {
            "target": self.node_name,
            "datapoints":[
                [self.generate_datapoint(self.data, time_range), self.timestamp]
            ]
        }

        return point
    
    @staticmethod
    def generate_datapoint(data:dict, time_range:int) -> int:
        """
        generate point data by self.data
        """
        time = pendulum.now().int_timestamp
        
        if time - data["timestamp"] > time_range:
            return INVALID
            
        else:
            if int(data["fields"].get("status", -1)) == 1:
                return RUN
            elif int(data["fields"].get("status", -1)) == 0:
                return STOP
            elif int(data["fields"].get("status", -1)) == -1:
                return UNKNOWN
            else:
                return UNDEFINED
        

"""
Quest sample
{'timezone': 'browser', 
'panelId': 2, 
'dashboardId': None, 
'range': {
    'from': '2018-12-03T00:39:54.863Z', 'to': '2018-12-03T06:39:54.863Z', 
        'raw': {
            'from': 'now-6h', 'to': 'now'
            }
        }, 
'rangeRaw': {
    'from': 'now-6h',
     'to': 'now'
    },
'interval': '5m', 
'intervalMs': 300000, 
'targets': [{'target': 'node_2', 'refId': 'A', 'hide': False, 'type': 'timeserie'}, 
{'target': 'status', 'refId': 'B', 'type': 'table'}], 
'maxDataPoints': 100, 
'scopedVars': {'__interval': {'text': '5m', 'value': '5m'}, 
'__interval_ms': {'text': 300000,'value': 300000}},
 'cacheTimeout': None, 
 'adhocFilters': []
 }
 """