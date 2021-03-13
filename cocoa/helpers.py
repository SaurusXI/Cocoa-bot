import os

from yaml import load, Loader

config_path = os.path.join('config.yaml')

with open(config_path, 'r') as f:
    config = load(f, Loader=Loader)

class envloader:
    config=config