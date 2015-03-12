__author__ = 'tieni'

import cProfile

from django.db.models import Q

from jobs.chunk import Chunk
from jobs.models import job_exists, Submission
from jobs.scripts.submission_validation import write_majority_vote_mergelist

info_path = "/home/knossos/chunk_infos/"


def content():
    chunk_range = [num for num in range(1475, 1476) if job_exists(num)]
    print(chunk_range)
    overlap_list = []
    for chunk_number in chunk_range:
        chunk = Chunk(chunk_number)
        mergelists = []
        overlaps = chunk.get_overlapping_chunks()
        chunks = []
        available_submits = Submission.objects.filter(Q(job__chunk_number__in=overlaps), ~Q(state=Submission.REJECTED))
        for submission in available_submits:
            if submission.job.chunk_number not in chunks:
                mergelist = submission.mergelist()
                if mergelist is not None:
                    mergelists.append(mergelist)
                    chunks.append(submission.job.chunk_number)
        overlap_list.append("chunk {0}: {1} overlaps\n".format(chunk_number, len(mergelists)))
        print("Creating majority vote mergelist for {0}".format(chunk_number))
        write_majority_vote_mergelist(chunk_number, mergelists, True, "/home/knossos/mergelists/mergelist_{0}.txt".format(chunk_number))

    with open("/home/knossos/overlaps.txt", 'w') as overlaps_f:
        overlaps_f.writelines(overlap_list)


def run(*args):
    cProfile.runctx("content()", globals(), locals())
