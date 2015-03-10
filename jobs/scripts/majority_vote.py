__author__ = 'tieni'

from django.db.models import Q

from jobs.chunk import Chunk
from jobs.models import job_exists, Submission
from jobs.scripts.submission_validation import write_majority_vote_mergelist

info_path = "/home/knossos/chunk_infos/"


def run(*args):
    if len(args) == 0:
        return
    chunk_range = [num for num in range(0, 2475) if job_exists(num)] if "all" in args else [int(value) for value in args[:-1]]
    overlap_list = []
    for chunk_number in chunk_range:
        chunk = Chunk(chunk_number)
        mergelists = []
        overlaps = chunk.get_overlapping_chunks()
        chunks = []
        available_submits = Submission.objects.filter(Q(job__chunk_number__in=overlaps), ~Q(state=Submission.REJECTED))
        if len(available_submits) != 27:
            continue
        for submission in available_submits:
            if submission.job.chunk_number not in chunks:
                if submission.mergelist() is not None:
                    mergelists.append(submission.mergelist())
                    chunks.append(submission.job.chunk_number)
        overlap_list.append("chunk {0}: {1} overlaps\n".format(chunk_number, len(mergelists)))
        print("Creating majority vote mergelist for {0}".format(chunk_number))
        write_majority_vote_mergelist(chunk_number, mergelists)

    with open(args[-1], 'w') as overlaps_f:
        overlaps_f.writelines(overlap_list)