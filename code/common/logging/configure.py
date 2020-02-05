import os
import json
import logging.config

def setup_logging(default_path='logging-config.json', default_level=logging.INFO, env_key='LOG_CFG'):
    """
    Setup logging configuration
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = default_path
    value = os.getenv(env_key, None)

    if value:
        file_path = value

    full_path = '{}/{}'.format(dir_path, file_path)

    if os.path.exists(full_path):
        with open(full_path, 'rt') as f:
            config = json.load(f)

        logging.config.dictConfig(config)

    else:
        logging.basicConfig(level=default_level)
