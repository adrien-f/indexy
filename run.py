import os
import yaml
from indexy.app import create_app

with open('./config.yml') as f:
    config_file = f.read()

app = create_app(config_object=yaml.load(config_file))

if __name__ == '__main__':
    app.run('0.0.0.0', port=int(os.environ.get('PORT', 5002)), debug=True)
