__author__ = 'Tieni'

import cProfile
from multiprocessing import Pool
import numpy
import os

from chunk import Chunk
from DatasetUtils import knossosDataset
from mergelist import Mergelist


def copy_coords(supervoxels, index, new_id, seg):
    new_seg = numpy.empty_like(seg)
    while index < len(supervoxels):
        indices = numpy.where(seg == supervoxels[index])
        x_coords = indices[0]
        y_coords = indices[1]
        z_coords = [z_coord/2 for z_coord in indices[2]]
        for i in range(len(indices[0])):
            new_seg[x_coords[i]][y_coords[i]][z_coords[i]] = new_id
        index += 8
    return new_seg


def apply_object(objects, index, new_id, seg):
    new_seg = numpy.empty_like(seg)
    num_objects = 0
    while index < len(objects):
        num_objects += 1
        for sub_obj in objects[index].supervoxels:
            indices = numpy.where(seg == sub_obj)
            x_coords = indices[0]
            y_coords = indices[1]
            z_coords = [round(z_coord/2) for z_coord in indices[2]]
            for i in range(len(indices[0])):
                new_seg[x_coords[i]][y_coords[i]][z_coords[i]] = new_id + index
        index += 8
    return new_seg


def apply_mergelist(mergelist_path, output_kzip, chunk_number, new_id, k_dataset):
    print("chunk {0}, new ID {1}".format(chunk_number, new_id))
    objects = Mergelist(mergelist_path).seg_objects
    chunk = Chunk(chunk_number)
    seg = chunk.seg()
    new_seg = numpy.empty_like(seg)
    # for obj in objects:
    #     for sub_obj in obj.supervoxels:
    #         indices = numpy.where(seg == sub_obj)
    #         x_coords = indices[0]
    #         y_coords = indices[1]
    #         z_coords = [z_coord/2 for z_coord in indices[2]]
    #         for i in range(len(indices[0])):
    #             new_seg[x_coords[i]][y_coords[i]][z_coords[i]] = new_id
    #     new_id += 1
    with Pool(processes=8) as p:
        results = p.starmap(apply_object, [(objects, 0, new_id, seg), (objects, 1, new_id, seg),
                                           (objects, 2, new_id, seg), (objects, 3, new_id, seg),
                                           (objects, 4, new_id, seg), (objects, 5, new_id, seg),
                                           (objects, 6, new_id, seg), (objects, 7, new_id, seg)])
        for i in range(len(results)):
            zeros = (new_seg == 0).astype(int)
            new_seg += zeros * results[i]
    print(chunk.coordinates())
    k_dataset.from_matrix_to_cubes(chunk.coordinates(), mags=1, data=new_seg, kzip_path=output_kzip)
    return new_id + len(objects)

if __name__ == '__main__':
    Chunk.info_path = "C:/Users/Tieni/Knossos/chunk_infos/"
    mergelist_path = "C:/Users/Tieni/Knossos/mergelists_majority_vote/"
    next_id = 1
    k_dataset = knossosDataset()
    k_dataset.initialize_from_knossos_path("E:/j0126_cubed/", fixed_mag=1)

    for name in os.listdir(mergelist_path):
        chunk_number = int(name[10:-4])
        next_id = apply_mergelist(mergelist_path + name,
                                  "C:/Users/Tieni/Knossos/kzips_applied_mergelists/chunk_{0}.k.zip".format(chunk_number),
                                  chunk_number, next_id, k_dataset)

    # cProfile.runctx('apply_mergelist(mergelist_path + "mergelist_974.txt", "C:/Users/Tieni/Knossos/kzips_applied_mergelists/chunk_974.k.zip", 974, 1, k_dataset)', globals(), locals())