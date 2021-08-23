""" Script to create a connection to sqlite dbs depending on input path. """

# ## Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import yaml
from pathlib import Path

# ## Open Configuration-file and set paths to models (trained and retrained)
with open(Path(r'C:\Users\Christine\Documents\Qualifikationsentwicklungsforschung\quenfo\quenfo_py\code\config.yaml'), 'r') as yamlfile:
    cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)

# ## Input-Paths
input_path = cfg['resources']['input_path']

# input_path = os.path.join('..','..', 'traindata_sql.db')
# input_path = os.path.join('..','..', 'text_kernel_orm_2018_03.db')

# Create engine with path
engine = create_engine('sqlite:///' + input_path, echo=False)

# Bind engine to recieve a session
Session = sessionmaker(bind=engine)

# Instantiate a session object
session = Session()
