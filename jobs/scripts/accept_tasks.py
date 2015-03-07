__author__ = 'tieni'


from jobs.models import *
from jobs.scripts.mw_communication import get_tasks_from, Task


mw_ids = ['d9e96698', 'd5cee551', '11efb79e', '089df202', 'abb744ad']


def run(*args):
    if len(args) == 0:
        for mw_id in mw_ids:
            good_tasks = [task for task in get_tasks_from(mw_id) if task["task_rating"] == "NOTRATED"]
            for task in good_tasks:
                task.rate(True, "")
            for submit in Submission.objects.filter(token__in=[task["proof"][0] for task in good_tasks]):
                submit.state = Submission.ACCEPTED
                submit.save()
        return
    # task ids listed
    good_tasks = [Task(int(value)) for value in args[:-1]]
    for task in good_tasks:
        task.rate(True, "" if len(args[-1]) == 0 else args[-1])
    for submit in Submission.objects.filter(token__in=[task.vcode() for task in good_tasks]):
        submit.state = Submission.ACCEPTED
        submit.save()