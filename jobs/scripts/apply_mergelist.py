__author__ = 'Tieni'

import cProfile
from multiprocessing import Pool
import numpy
from os import listdir
import pyximport; pyximport.install(setup_args={"include_dirs": numpy.get_include()})
import apply_new_ids
from chunk import Chunk
from DatasetUtils import knossosDataset
from mergelist import Mergelist

def map_subobj_ids(mergelist, base_id):
    """
    Maps subobjects of different objects to a new unique ID

    :param mergelist: the mergelist containing object - subobject relations
    :param base_id: the first ID to use
    :return: a dictionary {subobject ID : new unique ID}
    """
    id_map = {}
    for obj in mergelist.seg_objects:
        for subobj in obj.supervoxels:
            id_map[subobj] = base_id
        base_id += 1
    return id_map

def apply_mergelist(mergelist, output_kzip, chunk_number, new_id, k_dataset):
    print("chunk {0}, new ID {1}".format(chunk_number, new_id))
    chunk = Chunk(chunk_number)
    print(chunk.coordinates())
    id_map = map_subobj_ids(mergelist, new_id)
    new_seg = apply_new_ids.execute(id_map, chunk.seg())
    print("writing kzip")
    k_dataset.from_matrix_to_cubes(chunk.coordinates(), mags=1, data=new_seg, kzip_path=output_kzip)


Chunk.info_path = "/home/tieni/brainpuzzler/data/chunk_infos/"
mergelist_path = "/home/tieni/brainpuzzler/data/hk_majority_voted/"
k_dataset = knossosDataset()
k_dataset.initialize_from_knossos_path("/run/media/tieni/My-Tien/j0126_cubed/", fixed_mag=1)

# define work to be done by each worker
def process(work_list):
    for entry in work_list:
        print("processing entry", entry)
        chunk_number = entry[   1]
        coords = Chunk(chunk_number).coordinates()
        kzip_output_path = \
            "/home/tieni/brainpuzzler/data/mw_kzips_applied_mergelists/chunk_{0}_{1}_{2}_{3}.k.zip"\
            .format(chunk_number, coords[0], coords[1], coords[2])
        mergelist = Mergelist(mergelist_path + entry[0])
        apply_mergelist(mergelist, kzip_output_path, chunk_number, entry[2], k_dataset)
        print("finished with entry", entry)
    return "yeah, I am finished!"

def process_chunks():
    # Prepare data for multithreading the processing of the chunks.
    # Each worker needs a mergelist, its corresponding chunk number and the next free ID.
    # The next free ID is the cumulative number of objects in the previous chunks + 1
    print("preparing work list")
    total_work = []
    prev_max_id = 0
    mergelist_files = listdir(mergelist_path)
    for name in mergelist_files:
        mergelist = Mergelist(mergelist_path + name)
        total_work.append((name, int(name[10:-4]), prev_max_id + 1))
        prev_max_id += len(mergelist.seg_objects)
    # partition work for the workers
    print("partitioning work")
    num_workers = 4
    part_len = len(total_work)/float(num_workers)
    workloads = [total_work[int(round(part_len * i)): int(round(part_len * (i + 1)))] for i in range(num_workers)]
    print(workloads)
    with Pool(processes=num_workers) as pool:
        result = pool.map(process, [workloads[0], workloads[1], workloads[2], workloads[3]])
        print(result)

if __name__ == '__main__':
    # kzip_output_path = "/home/tieni/brainpuzzler/data/hk_kzips_applied_mergelists/chunk_{0}_{1}_{2}_{3}.k.zip".format(0, 4840, 4712, 2630)
    cProfile.runctx('process_chunks()', globals(), locals())
    # process_chunks()