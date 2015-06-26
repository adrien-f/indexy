from pathlib import Path
import itertools
from indexy.exceptions import PathNotFoundError, UnsafePathError


class WalkerElement(object):

    def __init__(self, path: Path):
        self.path = path

    def __getattr__(self, *args, **kwargs):
        return self.path.__getattribute__(*args, **kwargs)

    def is_video_media(self):
        return self.suffix in ['.mkv', '.avi', '.mp4']

    def thumbnail(self):
        return None


class Walker(object):

    app = None
    root = None
    default_config = dict(root='')

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.root = Path(self.app.config.get('WALKER', self.default_config)['root'])
        assert(self.root.exists())

    def get_root(self):
        return self.list(self.root)

    def list(self, folder):
        result = {'folders': [], 'files': [], 'current': folder}

        def group_func(item):
            if item.is_dir():
                return 'folders'
            return 'files'

        for item in folder.iterdir():
            if item.is_dir():
                result['folders'].append(WalkerElement(item))
            else:
                result['files'].append(WalkerElement(item))

        return result

    def get_path(self, path):
        path = self.root / Path(path)
        if not path.exists():
            raise PathNotFoundError(path)
        if not self.is_safe(path):
            raise UnsafePathError(path)
        return WalkerElement(path)

    def list_from_route(self, path):
        return self.list(self.get_path(path))

    def is_safe(self, path):
        try:
            path.relative_to(self.root)
        except ValueError:
            return False
        else:
            return True

    def safe_parents(self, path):
        return [parent for parent in path.parents if self.is_safe(parent)]

    def make_relative(self, path):
        return path.relative_to(self.root)

walker = Walker()