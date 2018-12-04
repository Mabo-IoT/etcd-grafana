import logging
import pendulum

from typing import Type, TypeVar

T = TypeVar('T', bound='GrafanaQuery')
S = TypeVar('S', bound='QueryResponse')

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

    def etcd_key(self, node_key:str, node_value:str) -> [str]:
        """
        generate etcd sql according to targets
        """

        keys = [node_key+'/'+target_node+node_value for target_node in self.targets]
        
        return keys


class QueryResponse:
    def __init__(self):
        pass
    
    @classmethod
    def generate_response(cls:Type[S], data:dict) -> S:
        """
        generate response by etcd data
        """
        pass
    
    @property
    def json_data(self) -> dict:
        """
        generate json data by response
        """
        pass


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