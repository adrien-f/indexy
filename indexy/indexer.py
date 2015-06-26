import pickle
import zlib
from flask import request, jsonify
from flask.ext.classy import FlaskView, route
from fuzzywuzzy import fuzz, process
from indexy.app import redis
from indexy.walker import walker


class Indexer(object):
    """
    Index all filenames, store it in redis and allow it to be queried
    """

    app = None

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.IndexerView.register(app)

    def build_index(self):
        files = []

        def recursive(items):
            for file in items['files']:
                files.append(str(walker.make_relative(file)))
            for folder in items['folders']:
                recursive(walker.list(folder))

        recursive(walker.get_root())

        pickled_files = pickle.dumps(files)
        compressed_list = zlib.compress(pickled_files)
        redis.set('indexy_index', compressed_list)
        redis.expire('indexy_index', 3600)
        return compressed_list

    def query_index(self, query):
        index = redis.get('indexy_index')
        if not index:
            index = self.build_index()
        index = zlib.decompress(index)
        index = pickle.loads(index)
        return (x[0] for x in process.extract(query, index, scorer=fuzz.token_set_ratio) if x[1] > 80)

    class IndexerView(FlaskView):
        route_prefix = '/indexer'

        @route('/', methods=['POST'], endpoint='indexer-query')
        def post(self):
            query = request.json.get('query') or request.args.get('query')
            return jsonify({'results': list(indexer.query_index(query))})





indexer = Indexer()