import logging
import logging.config
import os
import uuid
import yaml


def setup_logging(default_path=os.path.join(os.path.dirname(__file__), 'logging.yaml'), default_level='INFO', env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)

    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        print('Failed to load configuration file. Using default configs')


class LoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger):
        super(LoggerAdapter, self).__init__(logger, {})
        self.uuid = str(uuid.uuid4())

    def process(self, msg, kwargs):
        from src import app
        username = app.config['USERNAME']
        return '[%s] [%s] %s' % (self.uuid, username, msg), kwargs
