import cProfile
import os

from jobs.chunk import Chunk
from jobs.mergelist import Mergelist
import submission_validation

basedir = "set basedir"
Chunk.info_path = basedir + "chunk_infos/"
mergelist_path = basedir + "hk_original_mergelists/"


def content():
    chunk_range = [num for num in range(2475) if os.path.isfile(mergelist_path + "mergelist_{0}.txt".format(num))]

    for chunk_number in chunk_range:
        chunk = Chunk(chunk_number)
        overlap_mergelists = []
        overlapping_chunks = chunk.get_overlapping_chunks()
        available_chunks = set(overlapping_chunks) & set(chunk_range)
        for chunk_no in available_chunks:
            mergelist = Mergelist(mergelist_path + "mergelist_{0}.txt".format(chunk_no))
            if mergelist is not None:
                overlap_mergelists.append((mergelist, chunk_no))
        print("chunk {0}: {1} overlaps\n".format(chunk_number, len(overlap_mergelists)))

        print("Creating majority vote mergelist for {0}".format(chunk_number))
        submission_validation.write_voted_mergelist(chunk_number, overlap_mergelists,
                              basedir + "hk_voted_respect_size/mergelist_{0}.txt".format(chunk_number),
                              {100: 1, 10000: 0.5, float("inf"): "one"})


cProfile.runctx("content()", globals(), locals())