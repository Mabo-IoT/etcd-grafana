import logging
import requests

from etcd import Client,EtcdResult


log = logging.getLogger(__name__)

class EtcdWrapper:
    """
    Pack etcd library, send data to etcd
    """

    def __init__(self, conf:dict):
        self.conf = conf
        self.host, self.port = self.conf['host'], self.conf['port']
        self.client = Client(host=self.host, port=self.port)
        self.test_connect()

    def test_connect(self) -> bool:
        """
        test etcd server
        :return: 
        """
        url = 'http://' + self.host + ':' + str(self.port) + '/version'
        try:
            data = requests.get(url)
            if data.status_code == 200:
                log.info("etcd client init ok!")
                return True
            else:
                return False
        except Exception as e:
            log.error("\n%s", e)
            log.info("Check etcd server or network")
            return False

    def write(self, key:str, value:str):
        try:
            self.client.write(key, value)
        except Exception as e:
            log.error("\n%s", e)

    def read(self, key:str) -> EtcdResult:
        try:
            return self.client.read(key)
        except Exception as e:
            log.error("\n%s", e)

    def delete(self, key):
        try:
            return self.client.delete(key)
        except Exception as e:
            log.error("\n%s", e)
