import pendulum
import json
import random
import time

from context import EtcdWrapper


def generate_etcd_data() -> dict:

    data = {
        
        "fields": {
            "status":random.randint(0,1),

        },
        "timestamp":pendulum.now().int_timestamp,
    }
    node = "test" + str(random.randint(0, 10))
    time = pendulum.now().int_timestamp

    etcd_data = {
        "node": node,
        "data": data,
        "time": time
    }
    return etcd_data


def main():
    conf = {
    "host": "127.0.0.1",
    "port": 2379
}

    etcd = EtcdWrapper(conf)
    key_prefix = "/nodes_name/"

    while True:
        etcd_data = generate_etcd_data()
        key = key_prefix + etcd_data["node"]
        
        etcd.write(key, json.dumps(etcd_data))
        print("write etcd data done")
        time.sleep(1)


if __name__ == '__main__':
    main()




