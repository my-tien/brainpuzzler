import os

from jobs.models import Submission
from scripts.mergelist_validation import Chunk
from scripts.mw_communication import Campaign, get_task_vcode


campaign_id = '2ebd1883a3f7'


def run():
    campaign = Campaign(campaign_id)
    unrated = campaign.get_unrated_tasks()
    if unrated is None:
        print("No unrated tasks at the moment!")

    for task in unrated:
        vcode = get_task_vcode(task[0])
        try:
            submission = Submission.objects.filter(token=vcode)[0]
            kzip_path = os.path.basename(submission.submit_file.name)
            chunk = Chunk(submission.job.chunk_number)
            valid = chunk.is_valid(kzip_path)
            campaign.rate_task(task[0], valid, "" if valid else "Your annotation seems to be incomplete.\n"
                                                                "(If you think this is an error, "
                                                                "message me at my-tien.nguyen@mpimf-heidelberg.mpg.de)")

        except IndexError:
            print("Could not find vcode {0} for task {1}".format(vcode, task[0]))