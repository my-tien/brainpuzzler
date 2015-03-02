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
    reject_tasks = [bad_task for bad_task in unrated if get_task_vcode(bad_task[0]) in tokens]
    for submit in submits:
        for reject_task in reject_tasks:
            reject_vcode = get_task_vcode(reject_task[0])
            if reject_vcode == submit.token:
                print("I reject submit {0} from task {1}".format(submit, reject_task[0]))
                submit.state = Submission.REJECTED
                submit.save()
                comment = "Your submission does not contain any work.\n"\
                          "If you had problems with KNOSSOS, please message "\
                          "me at my-tien.nguyen@mpimf-heidelberg.mpg.de" if len(args[-1]) == 0 else args[-1]
                rate_task(reject_task[0], False, comment)