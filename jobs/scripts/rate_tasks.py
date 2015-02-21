import os

from jobs.models import Submission
from brainpuzzler.settings import MEDIA_ROOT
from jobs.scripts.mergelist_validation import Chunk
from jobs.scripts.mw_communication import Campaign, get_task_vcode, get_task_worker


campaign_id = '2ebd1883a3f7'


def run():
    campaign = Campaign(campaign_id)
    unrated = campaign.get_unrated_tasks()
    if unrated is None:
        print("No unrated tasks at the moment!")
        return

    valids = []
    invalids = []
    for task in unrated:
        vcode = get_task_vcode(task[0])
        try:
            submission = Submission.objects.filter(token=vcode)[0]
            kzip_name = os.path.basename(submission.submit_file.name)
            chunk = Chunk(submission.job.chunk_number)
            valid = chunk.is_valid(MEDIA_ROOT + kzip_name)
            if valid:
                valids.append("I rate task {0} with {1} valid!".format(task[0], kzip_name))
                submission.state = Submission.ACCEPTED
                campaign.rate_task(task[0], True, "")
            else:
                invalids.append(("I rate task {0} with {1} invalid!".format(task[0], kzip_name)))
                submission.state = Submission.REJECTED
                campaign.rate_task(task[0], valid, "" if valid else "Your annotation seems to be incomplete.\n"
                                                                    "If you had problems with KNOSSOS, please message "
                                                                    "me at my-tien.nguyen@mpimf-heidelberg.mpg.de")
            submission.save()

        except IndexError:
            print("Could not find vcode {0} for task {1}".format(vcode, task[0]))
    print('\n'.join(valids))
    print('\n'.join(invalids))
    counter = float(len(valids) + len(invalids))
    print("I rated {0} tasks: {1} valid ({2:.2f}%) and {3} invalid ({4:.2f}%)!"
          .format(counter, len(valids), 100*len(valids)/counter, len(invalids), 100*len(invalids)/counter))