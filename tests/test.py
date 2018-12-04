import unittest

from context import EtcdWrapper


class Test_EtcdWarpper(unittest.TestCase):
    def setUp(self):
        """
        init a request instance
        """
        conf = {
            "host": "127.0.0.1",
            "port": 2379,
        }
        self.etcd = EtcdWrapper(conf)

    def test_connect(self):
        """
        test etcd connect
        """ 

        self.assertEqual(True, self.etcd.test_connect())
    
    def test_read_value(self):
        """
        test etcd get values
        """

        value = self.etcd.read("/nodes")
        print(dir(value))
        values = value.children
        for v in values:
            print(v.key)
        self.assertEqual("nodes", value.leaves)



if __name__ == '__main__':
    suite = unittest.TestSuite()
    tests = [Test_EtcdWarpper("test_connect"),Test_EtcdWarpper("test_read_value")]

    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
