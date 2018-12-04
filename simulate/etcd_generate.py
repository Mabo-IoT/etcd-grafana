import pendulum

from context import EtcdWrapper


conf = {
    "host": "127.0.0.1",
    "port": 2379
}

etcd = EtcdWrapper(conf)



