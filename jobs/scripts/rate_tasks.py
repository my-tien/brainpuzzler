import os

from jobs.models import Submission
from jobs.scripts.submission_validation import is_acceptable
from jobs.scripts.mw_communication import get_task_vcode, get_unrated_tasks, rate_task


campaign_id = '2ebd1883a3f7'


def run(*args):
    unrated = get_unrated_tasks()
    if unrated is None:
        print("No unrated tasks at the moment!")
        return

    acceptables = []
    rejects = []
    for task in unrated:
        vcode = get_task_vcode(task[0])
        try:
            submission = Submission.objects.filter(token=vcode)[0]
            kzip_name = os.path.basename(submission.submit_file.name)
            acceptable = is_acceptable(submission)
            if acceptable:
                acceptables.append("I rate task {0} with {1} valid!".format(task[0], kzip_name))
                if "apply" in args:
                    submission.state = Submission.ACCEPTED
                    rate_task(task[0], True, "")
            else:
                rejects.append(("I rate task {0} with {1} invalid!".format(task[0], kzip_name)))
                if "apply" in args:
                    submission.state = Submission.REJECTED
                    rate_task(task[0], False, "Your annotation seems to be incomplete.\n"
                                              "If you had problems with KNOSSOS, please message "
                                              "me at my-tien.nguyen@mpimf-heidelberg.mpg.de")
            submission.save()

        except IndexError:
            print("Could not find vcode {0} for task {1}".format(vcode, task[0]))
    print('\n'.join(acceptables))
    print('\n'.join(rejects))
    counter = float(len(acceptables) + len(rejects))
    print("I rated {0} tasks: {1} valid ({2:.1f}%) and {3} invalid ({4:.1f}%)!"
          .format(int(counter), len(acceptables), 100*len(acceptables)/counter, len(rejects), 100*len(rejects)/counter))