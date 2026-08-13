import pathlib
from mybudget import constants

#Path
ROOT_FOLDER = pathlib.Path(__file__).parent
DB_PATH = ROOT_FOLDER.joinpath(constants.DB_FOLDER)
REPORT_PATH = ROOT_FOLDER.joinpath(constants.REPORT_FOLDER)
