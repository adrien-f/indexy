import av

class Converter(object):

    app = None

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

    def get_resolution(self, file):
        container = av.open(str(file))
        video = next(s for s in container.streams if s.type == b'video')
        return video.width, video.height

    def convert(self, file):
        pass