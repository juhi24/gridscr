from os import environ, path

environ['PYART_QUIET'] = ''
conf_path = path.join(path.dirname(path.realpath(__file__)), 'pyart_config.py')
environ['PYART_CONFIG'] = conf_path
#conf = config.load_config(conf_path)
