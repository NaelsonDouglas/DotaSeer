import logging
import colorlog
from datetime import datetime
import sys
def  configure_logging(action_name, level=logging.INFO):
        for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)
        logger = logging.getLogger()
        logger.setLevel(level)
        bold_seq = '\033[1m'
        colorlog_format = (
        f'{bold_seq} '
        f'%(log_color)s '        
        )
        colorlog.basicConfig(format=colorlog_format)        
        
        TERMINAL_FORMAT = colorlog.ColoredFormatter(
	"%(log_color)s%(levelname)-8s%(reset)s:%(blue)s%(asctime)s\n%(cyan)slocation:%(white)s%(module)s.py:%(lineno)s-->%(funcName)s\n%(green)s%(message)s",
        
	datefmt=None,
	reset=True,
	log_colors={
		'DEBUG':    'white,bg_cyan',
		'INFO':     'white,bg_blue',
		'WARNING':  'white,bg_yellow',
		'ERROR':    'white,bg_red',
		'CRITICAL': 'black,bg_red',
	},
	secondary_log_colors={},
	style='%'
        )        
        #TERMINAL_FORMAT = logging.Formatter('[%(levelname)s]:%(name)s:%(message)s')
        terminal_handler = logging.StreamHandler(sys.stdout)
        terminal_handler.setLevel(level)
        terminal_handler.setFormatter(TERMINAL_FORMAT)        
        logging.getLogger().addHandler(terminal_handler)