import json
import string
import random

def random_password(length=24, prefix=''):

    password = prefix + ''.join(random.choices(string.ascii_lowercase  +
                                               string.ascii_uppercase +
                                               string.punctuation     +
                                               string.digits          ,
                                               k=length))
    # replace these chars with _  (to make prevent errors in command prompts)
    items = ['"', '\'', '`','\\','}']
    for item in items:
        password = password.replace(item, '_')
    return password

def split_lines(text):
    return text.split('\n')

def json_round_trip(data):
    return json.loads(json.dumps(data))