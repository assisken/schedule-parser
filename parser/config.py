from configparser import ConfigParser

CONFIG = ConfigParser()
CONFIG.read('config.ini')

GROUP_CHECK_URL = CONFIG.get('schedule_parser', 'group-check')
GROUP_SCHEDULE_URL = CONFIG.get('schedule_parser', 'group-schedule')
VERSION_CHECK_URL = CONFIG.get('schedule_parser', 'version-check')
SAVE_PATH = CONFIG.get('schedule_parser', 'save-to')
