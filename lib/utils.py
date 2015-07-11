import random
from clint.textui import puts,colored
from datetime import datetime, timedelta
import re


# Some Cursor UTILS
"""
for more cursor magic things, see http://www.termsys.demon.co.uk/vtansi.htm#cursor
"""
MOVE_CURSOR_UP = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

"""
Our System wide date_format.
"""
DATE_FORMAT = '%Y-%m-%d %H:%M'

"""
Email Regex String almost similar to RFC5322
"""

EMAIL_REGEX = re.compile("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)")

"""
Counter Class for making Ever-Increasing Counters.
"""
class Counter(object):
    def __init__(self, name, base):
        self._todobase = base
        self._name = name
        self._count = self._todobase.get('/counter', self._name)
        if self._count is None:
            self._count = random.randint(1,1000)
            self._todobase.put('/counter', self._name, self._count)

    def get(self):
        print("self._count =>", self._count)
        self._count += 1
        self._todobase.put('/counter', self._name, self._count)
        return self._count


def foreach(collection, callback):
    for key in collection.keys():
        item = collection[key]
        callback(item, key)

def print_todo_item(item, key=None):
    """
    prints an todo item.
    """
    if item is not None:
        donestring = colored.green(chr(0x2714))
        puts( str(key) + " : "+colored.blue(str(item['bounty'])) + " : " + item['task']
             + " " + (donestring if item['done'] else ''))
    else:
        puts( colored.red('404: Nothing Found'))

def print_reward_item(item, key=None):
    """
    prints an Reward Item.
    """
    if item is not None:
        puts ( str(key) + " : " + colored.green(str(item['bounty'])) + " : "  + item ['reward']
              + " -> redeemed " + ( str(item['redeemed']) ) + " times." )
    else:
        puts( colored.red('404: Nothing Found'))

def parse_duestring(duestring, start_datetime=None):
    if duestring[0] in ['+', '-']:
        """
        That means the duestring is of the format [+,-][0-9][hdwmy]

        """
        pattern = re.compile(r'(\+|\-)([0-9]+)([Mhdwmy])')
        matches = pattern.findall(duestring)
        if start_datetime is None:
            time_now = datetime.now()
        else:
            time_now = datetime.strptime(start_datetime, DATE_FORMAT)
        due_datetime = time_now
        for match in matches:
            sign = match[0]
            n = int(match[1])
            unit = match[2]
            if unit == 'h':
                delta = timedelta(hours=n)
            elif unit == 'M':
                delta = timedelta(minutes=n)
            elif unit == 'd':
                delta = timedelta(days=n)
            elif unit == 'w':
                delta = timedelta(weeks=n)
            elif unit == 'm':
                delta = timedelta(days=n*30)
            elif unit == 'y':
                delta = timedelta(days=n*365)
            else:
                delta = timedelta(days=0)

            if sign == '+':
                due_datetime += delta
            else:
                due_datetime -= delta
        return due_datetime

    else:
        date_format = '%Y-%m-%d'
        due_datetime = datetime.strptime(duestring, date_format)
        return due_datetime

def clean_tags(tags):
    pattern = re.compile(r'\s*(\w+)')
    res = []
    for tag in tags:
        match = pattern.match(tag)
        if match is not None:
            res.append(match.group(1).lower())
    return res


def clean_foldername(foldername):
    return foldername.strip().lower()


def remove_common_elements(list1, list2, list3=None):
    if list3 is None:
        common_set = set(list1).intersection(list2)
    else:
        common_set = set(list1).intersection(list2).intersection(list3)
    list1_res = list(set(list1) - common_set)
    list2_res = list(set(list2) - common_set)
    list3_res = None
    if list3 is not None:
        list3_res = list(set(list3) - common_set)
    return (list1_res, list2_res, list3_res)
    
def generate_unique_code(length=10):
    code = ''
    for i in range(length):
        code += chr(random.randint(97, 122))
    return code
