import argparse
from . import __version__, monitor_log_file, LOG_FILE

def monitoring():
    monitor_log_file(LOG_FILE)
