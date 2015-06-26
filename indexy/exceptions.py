
class PathNotFoundError(Exception):

    path = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if args[0]:
            self.path = args[0]

class UnsafePathError(Exception):

    path = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if args[0]:
            self.path = args[0]
