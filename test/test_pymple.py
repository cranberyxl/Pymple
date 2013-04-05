import unittest
from pymple import Pymple

class TestPymple(unittest.TestCase):
    def setUp(self):
        self.p = Pymple()
        self.p['service'] = lambda p: Service()
        self.p['string'] = 'string value'

    def test_string(self):
        self.assertEqual(self.p['string'], 'string value')

    def test_callback(self):
        self.assertIsInstance(self.p['service'], Service)

    def test_service_different(self):
        serviceOne = self.p['service']
        self.assertIsInstance(serviceOne, Service)

        serviceTwo = self.p['service']
        self.assertIsInstance(serviceTwo, Service)

        self.assertNotEqual(serviceOne, serviceTwo)

    def test_pass_pymple_to_callback(self):
        self.p['container'] = lambda c: c

        self.assertEqual(self.p, self.p['container'])
        self.assertNotEqual(self.p, self.p['service'])

    def test_constructor(self):
        params = {'foo': 'bar', 'baz': 'boo'}
        p = Pymple(params)

        self.assertEqual(params['foo'], p['foo'])
        self.assertEqual(params['baz'], p['baz'])

    def test_set_null(self):
        self.p['test'] = None
        self.assertEqual(self.p['test'], None)

    def test_acts_like_dict(self):
        self.assertIn('service',self.p)

        del self.p['service']

        self.assertNotIn('service',self.p)

    def test_share(self):
        self.p['shared_service']  = self.p.share(lambda c: Service())

        serviceOne = self.p['shared_service']
        self.assertIsInstance(serviceOne, Service)

        serviceTwo = self.p['shared_service']
        self.assertIsInstance(serviceTwo, Service)

        self.assertEqual(serviceOne, serviceTwo)

    def test_protect(self):
        callback = lambda c: 'foo'
        self.p['test'] = self.p.protect(callback)
        self.assertEqual(callback, self.p['test'])

    def test_raw(self):
        callback = lambda c: 'foo'
        self.p['test'] = callback
        self.assertEqual(callback, self.p.raw('test'))

    def test_extend(self):
        self.p['shared_service']  = self.p.share(lambda c: Service())

        value = 12345

        def callback(service, container):
            service.value = value
            service.container = container
            return service

        self.p.extend('shared_service', callback)

        serviceOne = self.p['shared_service']
        self.assertIsInstance(serviceOne, Service)
        self.assertEqual(value, serviceOne.value)
        self.assertEqual(self.p, serviceOne.container)

        serviceTwo = self.p['shared_service']
        self.assertIsInstance(serviceTwo, Service)
        self.assertEqual(value, serviceTwo.value)
        self.assertEqual(self.p, serviceTwo.container)

        self.assertEqual(serviceOne, serviceTwo)

    def test_callable_class_as_factory(self):
        self.p['callable_class'] = CallableClass()

        self.assertEqual('called', self.p['callable_class'])

    def test_uncallable_class_as_factory(self):
        self.p['uncallable_class'] = UnCallableClass()

        self.assertIsInstance(self.p['uncallable_class'], UnCallableClass)

class Service(object):
    pass

class CallableClass(object):
    def __call__(self, c):
        return 'called'

class UnCallableClass(object):
    pass
