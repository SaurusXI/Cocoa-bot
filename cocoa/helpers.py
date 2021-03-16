import os
import config_vars
from yaml import load, Loader

config_path = os.path.join('config_vars.py')

'''with open(config_path, 'r') as f:
    config = load(f, Loader=Loader)'''

class envloader:
    config = config_vars.Config()