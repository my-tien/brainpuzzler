__author__ = 'tieni'


from jobs.models import *
from jobs.scripts.mw_communication import get_unrated_tasks, Task


mw_ids = ['d9e96698', 'd5cee551', '11efb79e', '089df202', 'abb744ad']


def run(*args):
    unrated = get_unrated_tasks()
    if unrated is None:
        print("No unrated tasks at the moment!")
        return

    good_tasks = [Task(good_task[0]) for good_task in unrated]

    if len(args) == 0:
        for task in good_tasks:
            if task.worker() in mw_ids:
                try:
                    submission = Submission.objects.filter(token=task.vcode())[0]
                    submission.state = Submission.ACCEPTED
                    task.rate(True, "")
                except IndexError:
                    print("Could not find submit for task {0}".format(task.id))
                    continue

        return
    # specific tasks passed
    numbers = [int(value) for value in args[:-1]]
    submits = Submission.objects.filter(job__chunk_number__in=numbers)
    tokens = [submit.token for submit in submits]
    good_tasks = [task for task in good_tasks if task.vcode() in tokens]
    for submit in submits:
        for good_task in good_tasks:
            good_vcode = good_task.vcode()
            if good_vcode == submit.token:
                print("I accept submit {0} from task {1}".format(submit, good_task.id))
                submit.state = Submission.ACCEPTED
                submit.save()
                comment = "" if len(args[-1]) == 0 else args[-1]
                good_task.rate(True, comment)