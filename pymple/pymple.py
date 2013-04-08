class Pymple(dict):
    def __getitem__(self, key):
        value = self.raw(key)

        return value(self) if callable(value) else value

    @staticmethod
    def share(callback):
        def inner(c):
            if not hasattr(inner, 'object'):
                inner.object = callback(c)

            return inner.object
        return inner

    def extend(self, key, callback):
        factory = self.raw(key)

        if not callable(factory):
            raise KeyError('Identifier "%s" does not contain an object definition.' % (key))

        self[key] = lambda c: callback(factory(c), c)

        return self[key]

    def raw(self, key):
        if key not in self:
            raise KeyError('Ientifier "%s" is not defined.' % (key))

        return super(Pymple, self).__getitem__(key)

    @staticmethod
    def protect(callback):
        return lambda c: callback
