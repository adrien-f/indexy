import pathlib
from flask import render_template, url_for, redirect, current_app, send_file, request
from flask.ext.classy import FlaskView, route
from itsdangerous import URLSafeTimedSerializer
from indexy.walker import walker

class TreeView(FlaskView):
    route_base = '/'

    @route('/view/<path:file>')
    def view(self, file, share=False):
        file = walker.get_path(file)
        if file.suffix in ['.mkv', '.mp4', '.avi', '.mp3']:
            return render_template('tree/view_video.html', file=file, share=share)
        return render_template('tree/view_file.html', file=file, share=share)

    @route('/download/<path:file>')
    def download(self, file):
        file = walker.get_path(file)
        return send_file(file.path.__str__(), as_attachment=True, attachment_filename=file.name)

    @route('/share/<path:file>')
    def share(self, file):
        file = walker.get_path(file)
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        share_code = s.dumps({'file': str(file.relative())})
        if request.args.get('modal', 'false') == 'true':
            return render_template('tree/share_modal.html', file=file, share_code=share_code)
        return render_template('tree/share.html', file=file, share_code=share_code)

    @route('/share_view/<code>')
    def share_view(self, code):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        share_code = s.loads(code, max_age=60 * 60 * 24)
        return self.view(share_code['file'], share=True)

    @route('/')
    @route('/list/<path:path>', endpoint='index_folder')
    @route('/list/', endpoint='index_root_folder')
    def index(self, path=None):
        root = False
        if not path:
            root = True
            view = walker.get_root()
        else:
            view = walker.list_from_route(path)
        return render_template('tree/index.html', view=view, root=root)
