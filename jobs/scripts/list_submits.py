__author__ = 'Tieni'

import os

from jobs.models import Submission
from jobs.mw_communication import get_tasks_from


def run(*args):
    if len(args) == 0:
        print("Usage: list_submits --script-args=[mw_id] [mw_id] ...")
        return
    for mw_id in args:
        submit_files = []
        result = [task for task in get_tasks_from(mw_id) if task["task_rating"] == "NOTRATED"]
        for task in result:
            vcode = task["proof"][0]
            try:
                submit = Submission.objects.filter(token=vcode)[0]
                submit_files.append(os.path.basename(submit.submit_file.name))
            except IndexError:
                print("Could not find submission for vcode: " + vcode)
                continue
        print("submissions from worker " + mw_id + ":")
        print(','.join(submit_files))
        print("task ids:")
        print(' '.join([task["task_id"] for task in result]))