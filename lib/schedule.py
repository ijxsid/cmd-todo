from datetime import datetime, timedelta
from utils import DATE_FORMAT

class Schedule(object):

    def __init__(self, base, todos):
        self._base = base
        self.NAME = 'schedule'
        self._todos = todos

    def create_dynamic_folder_structure(self):

        schedule = self._base.get('/'+ self.NAME, None)
        now = datetime.now()
        today = datetime(now.year, now.month, now.day)
        if schedule is not None and schedule['UPDATED'] is not None:
            updated_time = datetime.strptime(schedule['UPDATED'], DATE_FORMAT)
            updated_day = datetime(updated_time.year, updated_time.month, updated_time.day)
            if today == updated_day:
                print "Not Going to Calculate."
                return schedule

        dynamic_folders = {'future': [], 'later_this_year': [],
                           'later_this_month': [], 'this_week': [],
                           'next_week': [], 'today': [], 'past_due': [],
                           'tommorrow': [], 'UPDATED': None}
        todos = self._todos
        for key in todos.keys():
            todo = todos[key]
            if 'due' in todo:

                duetime = datetime.strptime(todo['due'], DATE_FORMAT)

                if today.day == duetime.day and today.month == duetime.month and today.year == duetime.year:
                    dynamic_folders['today'].append(todo)
                    continue

                tmrw_end = today + timedelta(hours=48)
                tmrw_start =  today + timedelta(hours=24)
                if duetime > tmrw_start and duetime <= tmrw_end:
                    dynamic_folders['tommorrow'].append(todo)
                    continue
                delta_end_of_week = timedelta(hours = ((7 - today.weekday())*24))
                end_of_week = today + delta_end_of_week
                if duetime > tmrw_end and duetime <=  end_of_week:
                    dynamic_folders['this_week'].append(todo)
                    continue

                delta_end_of_next_week = timedelta(hours = ((14 - today.weekday())*24))
                end_of_next_week = today + delta_end_of_next_week
                if duetime > end_of_week and duetime <= end_of_next_week:
                    dynamic_folders['next_week'].append(todo)
                    continue

                if today > duetime:
                    dynamic_folders['past_due'].append(todo)
                    continue

                if today.year == duetime.year and today.month == duetime.month:
                    dynamic_folders['later_this_month'].append(todo)
                    continue

                if today.year == duetime.year:
                    dynamic_folders['later_this_year'].append(todo)
                    continue
                if today.year < duetime.year:
                    dynamic_folders['future'].append(todo)
                    continue

        dynamic_folders['UPDATED'] = datetime.now().strftime(DATE_FORMAT)
        self._base.put('/', self.NAME, dynamic_folders)
        return dynamic_folders
