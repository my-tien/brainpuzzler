import cProfile
import mergelist_tools
from multiprocessing import Pool
import os
import re

from jobs.chunk import Chunk
from jobs.mergelist import Mergelist
from submission_validation import write_voted_mergelist

basedir = "set basedir"

Chunk.info_path = basedir +  "chunk_infos/"
mergelist_input_path = basedir + "mw_original_mergelists/"
mergelist_output_path = basedir + "mw_voted_respect_size_no_ecs/"

def vote_for_chunk(chunk_range):
    print("chunks", len(chunk_range))
    for chunk_number in chunk_range:
        chunk = Chunk(chunk_number)
        overlap_mergelists = []
        overlapping_chunks = chunk.get_overlapping_chunks()
        available_chunks = set(overlapping_chunks) & set(chunk_range)
        for chunk_no in available_chunks:
            mergelist = Mergelist(mergelist_input_path + "mergelist_{0}.txt".format(chunk_no))
            if mergelist is not None:
                overlap_mergelists.append((mergelist, chunk_no))
        print("chunk {0}: {1} overlaps\n".format(chunk_number, len(overlap_mergelists)))

        print("Creating majority vote mergelist for {0}".format(chunk_number))
        write_voted_mergelist(chunk_number, overlap_mergelists,
                              mergelist_output_path + "mergelist_{0}.txt".format(chunk_number),
                              {100: 1, 1000:  0.8, float("inf"): 0.5})
    return "finished!"


def create_mergelists():
    chunk_range = [num for num in range(2475) if os.path.isfile(mergelist_input_path + "mergelist_{0}.txt".format(num))]
    num_workers = 8
    part_len = len(chunk_range)/float(num_workers)
    workloads = [chunk_range[int(round(part_len * i)): int(round(part_len * (i + 1)))] for i in range(num_workers)]
    print(workloads)
    pool = Pool(processes=8)
    print(pool.map(vote_for_chunk, workloads))


def merge_mergelists():
    objects = []
    for mergelist_file in os.listdir(mergelist_output_path):
        if re.match('mergelist_[0-9]+.txt', mergelist_file):
            with open(mergelist_output_path + mergelist_file, 'r') as mergelist:
                print("mergelist ", mergelist_file)
                mergelist_string = mergelist.read()
                objects += mergelist_tools.objects_from_mergelist(mergelist_string)

    merged_objects = list(mergelist_tools.merge_objects(objects))
    subobj_positions = center_cube_mergelist()
    with open(mergelist_output_path + "mergelist.txt", 'w') as new_mergelist:
        new_mergelist.write(mergelist_tools.gen_mergelist_from_objects(merged_objects, subobj_positions))


def center_cube_mergelist():
    chunk_range = [num for num in range(2475)]
    subobj_positions = dict()
    for chunk_num in chunk_range:
        if os.path.isfile(Chunk.info_path + "chunk{0}_info.h5".format(chunk_num)):
            next_chunk = Chunk(chunk_num)
            ids = next_chunk.ids()
            for index, entry in enumerate(next_chunk.mass_centers()):
                subobj_positions[ids[index]] = entry
    return subobj_positions

def do():
    create_mergelists()
    merge_mergelists()
cProfile.run("do()")
