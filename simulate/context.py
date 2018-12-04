import os
import sys

## add web-server path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web_server.lib.etcd_database import EtcdWrapper
