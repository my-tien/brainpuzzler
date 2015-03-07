__author__ = 'tieni'


from jobs.models import *
from jobs.scripts.mw_communication import Task


def run(*args):
    if len(args) == 0:
        print('Usage: reject_tasks --script-args=task_id ... [task_id] "comment"')
    bad_tasks = [Task(int(value)) for value in args[:-1]]
    for task in bad_tasks:
        comment = "Your submission contains too many errors.\n"\
                  "If you had problems with KNOSSOS, please message "\
                  "me at my-tien.nguyen@mpimf-heidelberg.mpg.de" if len(args[-1]) == 0 else args[-1]
        task.rate(False, comment)
    for submit in Submission.objects.filter(token__in=[task.vcode() for task in bad_tasks]):
        submit.state = Submission.REJECTED
        submit.save()