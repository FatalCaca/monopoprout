__author__ = 'Simon'


import re

def get_roll_score_from_message(message):
    return int(re.search("\d+", message).group(0))