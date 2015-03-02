import os

from jobs.models import Submission
from jobs.scripts.submission_validation import is_acceptable, has_0_time
from jobs.scripts.mw_communication import get_task_vcode, get_task_worker, get_unrated_tasks, rate_task


campaign_id = '2ebd1883a3f7'
mw_ids = ['d9e96698', 'd5cee551', '11efb79e', '089df202', 'abb744ad']


def run(*args):
    unrated = get_unrated_tasks()
    if unrated is None:
        print("No unrated tasks at the moment!")
        return

    acceptables = []
    rejects = []
    rejects_kzips = []
    for task in unrated:
        vcode = get_task_vcode(task[0])
        try:
            submission = Submission.objects.filter(token=vcode)[0]
            worker_id = get_task_worker(task[0])
            if "accept-known-mws" in args:
                if worker_id in mw_ids:
                    submission.state = Submission.ACCEPTED
                    rate_task(task[0], True, "")
            elif "zero-time" in args:
                if has_0_time(submission):
                    print("Zero time in {0} from worker {1}".format(submission, worker_id))
                    if "apply-all" in args:
                        submission.state = Submission.REJECTED
                        submission.save()
                        rate_task(task[0], False, "Your submission does not contain any work.\n"
                                                  "If you had problems with KNOSSOS, please message "
                                                  "me at my-tien.nguyen@mpimf-heidelberg.mpg.de")

            else:
                kzip_name = os.path.basename(submission.submit_file.name)
                acceptable = is_acceptable(submission)
                if acceptable:
                    acceptables.append("I rate task {0} with {1} valid, from {2}!".format(task[0], kzip_name, worker_id))
                    if "apply-accepted" in args or "apply-all" in args:
                        submission.state = Submission.ACCEPTED
                        rate_task(task[0], True, "")
                else:
                    rejects.append(("I rate task {0} with {1} invalid, from {2}!".format(task[0], kzip_name, worker_id)))
                    if "apply-all" in args:
                        submission.state = Submission.REJECTED
                        rate_task(task[0], False, "Your annotation seems to be incomplete.\n"
                                                  "If you had problems with KNOSSOS, please message "
                                                  "me at my-tien.nguyen@mpimf-heidelberg.mpg.de")
                    if "print-kzips":
                        rejects_kzips.append(kzip_name)
                submission.save()

        except IndexError:
            print("Could not find vcode {0} for task {1}".format(vcode, task[0]))

    if len(acceptables) > 0 or len(rejects) > 0:
        print('\n'.join(acceptables))
        print('\n'.join(rejects))
        if len(rejects_kzips) > 0:
            print(','.join(rejects_kzips))
        counter = float(len(acceptables) + len(rejects))
        print("I rated {0} tasks: {1} valid ({2:.1f}%) and {3} invalid ({4:.1f}%)!"
              .format(int(counter), len(acceptables), 100*len(acceptables)/counter, len(rejects), 100*len(rejects)/counter))