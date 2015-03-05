__author__ = 'tieni'


from jobs.models import *
from jobs.scripts.mw_communication import get_unrated_tasks, Task


def run(*args):
    if len(args) == 0:
        return
    number_range = args[:-1] if len(args) > 1 else args
    numbers = [int(value) for value in number_range]
    submits = Submission.objects.filter(job__chunk_number__in=numbers)
    tokens = [submit.token for submit in submits]
    unrated = get_unrated_tasks()
    reject_tasks = [Task(bad_task[0]) for bad_task in unrated]
    reject_tasks = [bad_task for bad_task in reject_tasks if bad_task.vcode() in tokens]
    for submit in submits:
        for reject_task in reject_tasks:
            reject_vcode = reject_task.vcode()
            if reject_vcode == submit.token:
                print("I reject submit {0} from task {1}".format(submit, reject_task.id))
                submit.state = Submission.REJECTED
                submit.save()
                comment = "Your submission does not contain any work.\n"\
                          "If you had problems with KNOSSOS, please message "\
                          "me at my-tien.nguyen@mpimf-heidelberg.mpg.de" if len(args[-1]) == 0 else args[-1]
                reject_task.rate(False, comment)