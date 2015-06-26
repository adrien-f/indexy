from flask import url_for
import bleach
import markdown
import arrow
from indexy.walker import walker


def humanize(date):
    try:
        return arrow.get(date).humanize()
    except Exception:
        return 'Invalid date'


def format_datetime(date):
    try:
        return arrow.get(date).format('DD MMMM YYYY - HH:ss')
    except Exception:
        return 'Invalid date'


def markdown_filter(content):
    bleach.ALLOWED_TAGS += 'p'
    return bleach.clean(markdown.markdown(content, strip=True))

def number_of_files(folder):
    if not folder.is_dir():
        return 0
    return sum(not path.is_dir() for path in folder.iterdir())

def number_of_folders(folder):
    if not folder.is_dir():
        return 0
    return sum(path.is_dir() for path in folder.iterdir())

def url_for_folder(folder):
    return url_for('index_folder', path=folder.relative_to(walker.root))

def get_icon(file):
    base = '<i class="fa fa-fw fa-{}"></i>'
    icon = 'file-o'
    if file.suffix in ['.pdf']:
        icon = 'file-pdf-o'
    if file.suffix in ['.jpg', '.jpeg', '.gif', '.png']:
        icon = 'file-image-o'
    if file.suffix in ['.c', '.cpp', '.py', '.js', '.css', '.html', '.htm', '.less']:
        icon = 'file-code-o'
    if file.suffix in ['.mp4', '.avi', '.mkv']:
        icon = 'file-video-o'
    return base.format(icon)

def safe_parents(path):
    return walker.safe_parents(path)

