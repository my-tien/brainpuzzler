__author__ = 'tieni'

import cProfile
from os import path
from django.db.models import Q

from jobs.chunk import Chunk
from jobs.mergelist import Mergelist, SegObject
from jobs.models import job_exists, Job, Submission
from jobs.scripts.submission_validation import write_majority_vote_mergelist

info_path = "/home/knossos/chunk_infos/"
mergelist_path = "/home/knossos/complete_mergelists/"


def content():
    ids = [2474] #range(563, 2475) #[1002, 1203, 1400, 1025, 1233, 1418, 1050, 1280, 1130, 1330, 1177, 1380] #454
    chunk_range = [num for num in ids if job_exists(num)]
    overlap_list = []
    for chunk_number in chunk_range:
        # if path.exists("/home/knossos/mergelists/mergelist_{0}.txt"):
        #     continue
        chunk = Chunk(chunk_number)
        mergelists = []
        overlaps = chunk.get_overlapping_chunks()
        chunks = []
        available_submits = Submission.objects.filter(Q(job__chunk_number__in=overlaps), ~Q(state=Submission.REJECTED))
        for submission in available_submits:
            if submission.job.chunk_number not in chunks:
                mergelist = Mergelist(mergelist_path + "mergelist_{0}.txt".format(chunk_number))
                if mergelist is not None:
                    mergelists.append((mergelist, submission.job.chunk_number))
                    chunks.append(submission.job.chunk_number)
        print("chunk {0}: {1} overlaps\n".format(chunk_number, len(mergelists)))
        if len(mergelists) == 27:
            overlap_list.append("chunk {0}: {1} overlaps\n".format(chunk_number, len(mergelists)))

    # mergelists = [(submission.mergelist(), submission.job.chunk_number) for submission in Submission.objects.filter(state__in=[Submission.ACCEPTED, Submission.REJECTED])]
    # for mergelist in mergelists:
    #     if not path.exists("/home/knossos/complete_mergelists/mergelist_{0}.txt"):
    #         chunk = Chunk(mergelist[1])
    #         for sub_id in chunk.ids():
    #             if sub_id not in mergelist[0].seg_subobjects.keys():
    #                 mergelist[0].add_object(0, 1, chunk.mass_center_of(sub_id), [sub_id])
    #         mergelist[0].write("/home/knossos/complete_mergelists/mergelist_{0}.txt".format(mergelist[1]))
        print("Creating majority vote mergelist for {0}".format(chunk_number))
        write_majority_vote_mergelist(chunk_number, mergelists, True, "/home/knossos/mergelists_vote7/mergelist_{0}.txt".format(chunk_number))
    #
    # with open("/home/knossos/overlaps.txt", 'w') as overlaps_f:
    #     overlaps_f.writelines(overlap_list)


def run(*args):
    # cProfile.runctx("content()", globals(), locals())
    content()