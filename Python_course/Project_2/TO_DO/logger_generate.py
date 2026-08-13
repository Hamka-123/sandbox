import logging
import pathlib


# Logging levels:
"""
Level	    When it’s used

NOT_SET     = WARNING
DEBUG	    Подробная информация, обычно представляющая интерес только при диагностике проблем.
INFO	    Подтверждение того, что все работает так, как ожидалось.
WARNING	    Указание на то, что произошло что-то неожиданное, или указание на какую-то проблему в ближайшем будущем (например, «недостаточно места на диске»). Программное обеспечение по-прежнему работает, как ожидалось.
ERROR	    Из-за более серьезной проблемы программное обеспечение не может выполнять некоторые функции.
CRITICAL	Серьезная ошибка, указывающая на то, что сама программа не может продолжать работу.
"""

LOG_FILE = pathlib.Path(__file__).parent.joinpath('test_log1.log')
LOG_LEVEL = logging.DEBUG
FILE_MODE = 'w'
FILE_MODE = 'a' # Default mode

# config logger

logging.basicConfig(
    filename=LOG_FILE,
    level=LOG_LEVEL,
    format='%(asctime)-20s, %(levelname)-10s, %(message)-s',
    filemode=FILE_MODE

)

# write messages
logging.debug("Thiis is DEBUG type message")
logging.info("Thiis is INFO type message")
logging.warning("Thiis is warning type message")
logging.error("Thiis is error type message")
logging.critical("Thiis is critical type message")


