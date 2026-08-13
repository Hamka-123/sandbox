__all__ = ['start_project']

import pathlib
from .constants import DB_FOLDER, REPORTS_FOLDER
from .utilities import start_project, create_database

# init tasks:
'''
- create folders structure
- create DB file
'''

print("Init started, creating folders structure ...")

try:
    pathlib.Path(DB_FOLDER).mkdir()
    pathlib.Path(REPORTS_FOLDER).mkdir()
    # pathlib.Path(DB_FOLDER).mkdir(exist_ok=True)
    # pathlib.Path(REPORTS_FOLDER).mkdir(exist_ok=True)

    pass
except Exception as e:
    print("ATTN:  Folders exists already!!!")
    pass

create_database()






