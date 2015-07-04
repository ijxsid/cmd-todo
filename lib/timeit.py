from datetime import datetime
from utils import MOVE_CURSOR_UP
import time, sys

class Timer(object):

    def __init__(self, status=False, time_taken='0:00:00'):
        self._start = datetime.now()
        self._done_status = status
        self._time_taken = time_taken

    def stop(self):
        end_time = self._get_time_elapsed()
        end_time = self._add_time(self._time_taken, end_time)
        done = self._done_status
        donestring = 'Y' if done else 'N'
        task_done = raw_input("Is this task done? (Y/n):(prev: "+ donestring +" ) ").strip()
        if task_done and (task_done[0] in 'Yy'):
            done = True
        elif task_done and (task_done[0] in 'Nn'):
            done = False
        else:
            print "Not a valid answer, so not changing the status of the task."

        return (end_time, done)

    def print_elapsed(self):
        try:
            time_elapsed_string = ''
            while True:
                time_elapsed_string = self._add_time(self._time_taken, self._get_time_elapsed())
                print('{}'.format(time_elapsed_string))
                sys.stdout.write(MOVE_CURSOR_UP)
                time.sleep(1)
        except KeyboardInterrupt:
            return self.stop()

    def _get_time_elapsed(self, now=None):
        if now == None:
            now = datetime.now()
        delta = now - self._start
        hours = (delta.days * 24) + (delta.seconds/3600)
        minutes = (delta.seconds%3600)/60
        seconds = delta.seconds%60
        minutes = '0' + str(minutes) if minutes < 10 else str(minutes)
        seconds = '0' + str(seconds) if seconds < 10 else str(seconds)

        return '{hours}:{minutes}:{seconds}'.format(hours=hours, minutes=minutes,
                                                  seconds=seconds)

    def _add_time(self, time1, time2):
        time1 = map(int, time1.split(':'))
        time2 = map(int, time2.split(':'))
        time_total = [0, 0, 0]
        time_total[2] = time1[2] + time2[2]
        if time_total[2] > 59:
            time_total[1] = time_total[2]/60
            time_total[2] = time_total[2]%60
        if time_total[2] < 10:
            time_total[2] = str(0) + str(time_total[2])
        time_total[1] += time1[1] + time2[1]
        if time_total[1] > 59:
            time_total[0] = time_total[1]/60
            time_total[1] = time_total[1]%60
        if time_total[1] < 10:
            time_total[1] = str(0) + str(time_total[1])
        time_total[0] += time1[0] + time2[0]
        time_total = map(str, time_total)
        return ':'.join(time_total)
