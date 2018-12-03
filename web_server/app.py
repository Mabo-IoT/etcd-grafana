import falcon
import logging 
import sys

from web_server.config import set_config
from web_server.log import setup_logging
from web_server.images import Resource, Search, Query, Annotations, Tag_keys, Tag_values


config = set_config('./web_server/config/conf.toml')

# init log just for now if not use gunicron, plz change log
log = logging.getLogger('web_server')
setup_logging(config['logging'], log)

log.debug("shall we begin")
api= application = falcon.API()

resource = Resource()
search = Search()
query = Query()
annotations = Annotations()
tag_keys = Tag_keys()
tag_values = Tag_values() 

api.add_route('/', resource)
api.add_route('/search', search)
api.add_route('/query', query)
api.add_route('/annotations', annotations)
api.add_route('/tag-keys', tag_keys)
api.add_route('/tag-values',tag_values)


