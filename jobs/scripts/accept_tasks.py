__author__ = 'tieni'


from jobs.models import *
from jobs.scripts.mw_communication import get_unrated_tasks, get_task_vcode, rate_task


def run(*args):
    if len(args) == 0:
        return
    numbers = [int(value) for value in args[:-1]]
    submits = Submission.objects.filter(job__chunk_number__in=numbers)
    tokens = [submit.token for submit in submits]
    unrated = get_unrated_tasks()
    good_tasks = [good_task for good_task in unrated if get_task_vcode(good_task[0]) in tokens]
    for submit in submits:
        for good_task in good_tasks:
            good_vcode = get_task_vcode(good_task[0])
            if good_vcode == submit.token:
                print("I accept submit {0} from task {1}".format(submit, good_task[0]))
                submit.state = Submission.ACCEPTED
                submit.save()
                comment = "" if len(args[-1]) == 0 else args[-1]
                rate_task(good_task[0], True, comment)