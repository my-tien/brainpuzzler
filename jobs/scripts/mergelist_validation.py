__author__ = 'tieni'

import h5py
from zipfile import ZipFile


class Chunk:
    info_path = "/home/knossos/chunk_infos/"
    correct_merges = []
    with open(info_path + "correct_merges.txt", 'r') as merges_file:
        for line in merges_file:
            correct_merges.append(line.split())

    def __init__(self, chunk_id):
        self.chunk_id = chunk_id

        with h5py.File(Chunk.info_path + "chunk{0}_info.h5".format(chunk_id), 'r') as chunk_file:
            self.ids = chunk_file['ids'].value

        self.correct_merges = \
            [[subobj_id for subobj_id in group if subobj_id in self.ids] for group in Chunk.correct_merges]

    def is_valid(self, kzip_path):
        try:
            with ZipFile(kzip_path, 'r') as kzip, kzip.open("mergelist.txt", 'r') as mergelist:
                merges = get_merged_groups(mergelist)
                for correct_merge in self.correct_merges:
                    for merge in merges:
                        if len(set(merge).intersection(correct_merge)) > 1:
                            return True
            return False
        except IOError:
            print("IOError opening kzip: " + kzip_path)
            return False


def get_merged_groups(mergelist):
    merges = []
    for line in mergelist:
        subobjects = line.split()[3:]
        if len(subobjects) > 1:
            merges.append(subobjects)

    for group_index in range(len(merges)):
        for object_id in merges[group_index]:
            for group_index2 in range(len(merges)):
                if group_index != group_index2 and object_id in merges[group_index2]:
                    merges[group_index] = list(set(merges[group_index]).union(merges[group_index2]))
                    merges[group_index2] = []
    merges = [group for group in merges if len(group) != 0]
    return merges