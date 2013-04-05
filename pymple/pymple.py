class Pymple(dict):
    def __getitem__(self, id):
        value = self.raw(id)

        return value(self) if callable(value) else value

    def share(self, callback):
        def inner(c):
            if not hasattr(inner, 'object'):
                inner.object = callback(c)

            return inner.object
        return inner

    def extend(self, id, callback):
        factory = self.raw(id)

        if not callable(factory):
            raise KeyError('Identifier "%s" does not contain an object definition.' % (id))

        def inner(c):
            return callback(factory(c), c)

        self[id] = inner

        return self[id]

    def raw(self, id):
        if id not in self:
            raise KeyError('Ientifier "%s" is not defined.' % (id))

        return super(Pymple, self).__getitem__(id)

    def protect(self, callback):
        def inner(c):
            return callback
        return inner
