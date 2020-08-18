class Mixin:
    def __init__(self, **kwargs):
        for cls in type(self).__mro__:
            init = getattr(cls, '_init', None)
            if init is not None:
                init(**kwargs)
