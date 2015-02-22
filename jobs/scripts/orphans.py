__author__ = 'tieni'

import os

from brainpuzzler.settings import MEDIA_ROOT
from jobs.models import Submission
from jobs.scripts.mw_communication import get_tasks, get_task_vcode


def run(*args):
    if "submits" in args:
        counter = 0
        tasks = get_tasks()['tasks']
        vcodes = [get_task_vcode(task[0]) for task in tasks]

        for submit in Submission.objects.all():
            if submit.token not in vcodes:
                counter += 1
                print("Submission " + str(submit) + " is orphaned.")
                if "delete" in args:
                    submit.delete()
        print("{0} orphaned submissions.".format(counter))

    if "kzips" in args:
        counter = 0
        for filename in os.listdir(MEDIA_ROOT):
            if filename.startswith("segmentationJobsfinal_") and len(Submission.objects.filter(submit_file="./"+filename)) == 0:
                counter += 1
                print("kzip " + filename + " is orphaned.")
                if "delete" in args:
                    os.remove(MEDIA_ROOT + filename)
        print("{0} orphaned kzips.".format(counter))