from pathlib import Path
import shutil
from guessit import guess_file_info
from six import itervalues
from indexy.media_types import ALL_TYPES


class Organizer(object):
    """
    Naive file mover based on extension and content find by guessit.
    """

    app = None
    collection_folders = []
    destination = Path()
    default_config = dict(collection_folders=[], destination=Path())
    destination_folders = {}

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.collection_folders = [Path(folder) for folder in self.app.config.get('ORGANIZER', self.default_config)['collection_folders']]
        self.destination = self.app.config.get('ORGANIZER', self.default_config)['destination']
        for folder in self.collection_folders:
            assert(folder.exists())
        self.destination_folders = {
            'audio': self.destination / Path('Audio'),
            'documents': self.destination / Path('Documents'),
            'movies': self.destination / Path('Movies'),
            'software': self.destination / Path('Software'),
            'tv': self.destination / Path('TV')
        }
        for folder in itervalues(self.destination_folders):
            if not folder.exists():
                folder.mkdir()

    def organize(self, commit=False):

        operations = []

        def recursive(path: Path):
            for element in path.iterdir():
                if element.is_dir():
                    recursive(element)
                if element.suffix in ALL_TYPES['video']:
                    metadata = guess_file_info(filename=element.name)
                    if metadata['type'] == 'movie':
                        if metadata.get('year'):
                            operations.append((element, self.destination_folders['movies'] / Path(
                                "{} - {}{}".format(metadata['title'], metadata.get('year'), element.suffix))))
                        else:
                            operations.append((element, self.destination_folders['movies'] / Path(
                                "{}.{}".format(metadata['title'], element.suffix))))
                    elif metadata['type'] == 'episode':
                        if not metadata.get('season'):
                            # Assume it's an anime
                            operations.append((element, self.destination_folders['tv'] / Path(metadata['series']) / Path(
                                "{} - {:02d}{}".format(metadata['series'], metadata['episodeNumber'], element.suffix)
                            )))
                        else:
                            # Assume it's a TV Show:
                            operations.append((element, self.destination_folders['tv'] / Path(metadata['series']) / Path('Season {:02d}'.format(metadata['season'])) / Path(
                                "{} S{:02d}E{:02d}{}".format(metadata['series'], metadata['episodeNumber'], metadata['season'], element.suffix)
                            )))
                    else:
                        # TODO: More file cases for moving and renaming
                        continue

        for folder in self.collection_folders:
            recursive(folder)

        if commit:
            self.commit(operations)
        return operations

    def commit(self, operations):
        failed = []
        for original, new in operations:
            if not new.parent.exists():
                new.parent.mkdir(parents=True)
            try:
                shutil.move(str(original), str(new))
            except (IOError, shutil.Error) as e:
                self.app.logger.error('Error commit organizer changes: ' + str(e))
                failed.append((original, new))
        if failed:
            self.app.logger.error('Failed to commit changes for these files: ' + str(failed))

organizer = Organizer()