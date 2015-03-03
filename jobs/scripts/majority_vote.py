__author__ = 'tieni'

import cProfile
from jobs.models import Submission
from jobs.scripts.submission_validation import *

info_path = "/home/knossos/chunk_infos/"


def run(*args):
    if len(args) == 0:
        return
    chunk_range = range(0, 2475) if "all" in args else [int(value) for value in args]
    for chunk_number in chunk_range:
        mergelists = []
        overlaps = get_overlapping_jobs(chunk_number)
        for submission in Submission.objects.filter(job__chunk_number__in=overlaps):
            mergelists.append(submission.mergelist())
        if "all" in args and len(mergelists) < 20:
            continue
        print("Creating majority vote mergelist for {0}".format(chunk_number))
        write_majority_vote_mergelist(chunk_number, mergelists)

