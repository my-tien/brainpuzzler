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

def vote_for_chunk(work_list, chunk_list, mergelist_input_paths, mergelist_output_path):
    print("worker {0} has {1} items in work_list".format(os.getpid(), len(work_list)))
    for idx, chunk_number in enumerate(work_list):
        chunk = Chunk(chunk_number)
        overlap_mergelists = dict()
        overlapping_chunks = chunk.get_overlapping_chunks()
        available_chunks = set(overlapping_chunks) & set(chunk_list)
        num_overlapping_mergelists = 0
        for chunk_no in available_chunks:
            for mergelist_input_path in mergelist_input_paths:
                mergelist = Mergelist(mergelist_input_path + "mergelist_{0}.txt".format(chunk_no))
                if mergelist is not None:
                    num_overlapping_mergelists += 1
                    try:
                        overlap_mergelists[chunk_no].append(mergelist)
                    except KeyError:
                        overlap_mergelists[chunk_no] = [mergelist]
        print("worker {0} .. chunk {1} has {2} overlaps\n".format(os.getpid(), chunk_number, num_overlapping_mergelists))

        print("worker {0}.. Creating majority vote mergelist for {1} ({2}%)".format(os.getpid(), chunk_number, idx/len(work_list)))
        write_voted_mergelist(chunk_number, overlap_mergelists,
                              mergelist_output_path + "mergelist_{0}.txt".format(chunk_number),
                              {100: 1, 1000:  0.8, float("inf"): 0.5})
    return "worker {0} finished!".format(os.getpid())


def create_mergelists(mergelist_input_paths, mergelist_output_path):
    chunk_range = [num for num in range(2475) if os.path.isfile(mergelist_input_paths[0] + "mergelist_{0}.txt".format(num))]
    num_workers = 8
    part_len = len(chunk_range)/float(num_workers)
    workloads = [(chunk_range[int(round(part_len * i)): int(round(part_len * (i + 1)))], chunk_range, mergelist_input_paths, mergelist_output_path) for i in range(num_workers)]
    print(workloads)
    with Pool(processes=8) as pool:
        print(pool.starmap(vote_for_chunk, workloads))


def merge_mergelists(mergelist_output_path):
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


def results(input_paths, output_path):
    create_mergelists(input_paths, output_path)
    # merge_mergelists(output_path)

# cProfile.runctx('results([basedir + "hk_original_mergelists/"], basedir + "hk_voted_respect_size_no_ecs/")', globals(), locals())
# cProfile.runctx('results([basedir + "mw_original_mergelists/"], basedir + "mw_voted_respect_size_no_ecs/")', globals(), locals())
# cProfile.runctx('results([basedir + "mw_original_mergelists/", basedir + "hk_original_mergelists/"], basedir + "mw_hk_voted_respect_size_no_ecs/")', globals(), locals())
chunk_range = [num for num in range(2475) if os.path.isfile(basedir + "mw_original_mergelists/mergelist_{0}.txt".format(num))]
# vote_for_chunk([1340], chunk_range, [basedir + "mw_original_mergelists/", basedir + "hk_original_mergelists/"], basedir + "mw_hk_voted_respect_size_no_ecs/")
vote_for_chunk([1340], chunk_range, [basedir + "hk_original_mergelists/"], basedir + "mw_hk_voted_respect_size_no_ecs/")
