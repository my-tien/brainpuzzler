__author__ = 'tieni'

import h5py
import numpy

info_path = "/home/knossos/chunk_infos/"


class Chunk:
    size = [140, 140, 138]

    def __init__(self, chunk_number):
        self.number = chunk_number
        self._seg = None
        self._ids = None
        self._mass_center = None
        self._sizes = None

    def read_seg(self):
        with h5py.File(info_path + "chunk{0}_values.h5".format(self.number), 'r') as values:
            self._seg = values['seg'].value

    def read_info(self):
        with h5py.File(info_path + "chunk{0}_info.h5".format(self.number), 'r') as info:
            self._mass_center = info['com'].value
            self._ids = info['ids'].value
            self._sizes = info['size'].value

    def seg(self):
        if self._seg is None:
            self.read_seg()
        return self._seg

    def ids(self):
        if self._ids is None:
            self.read_info()
        return self._ids

    def mass_center(self):
        if self._mass_center is None:
            self.read_info()
        return self._mass_center

    def sizes(self):
        if self._sizes is None:
            self.read_info()
        return self._sizes

    def index_of(self, voxel_id):
        return numpy.where(self.ids() == voxel_id)

    def size_of(self, voxel_id):
        index = self.index_of(voxel_id)
        return self.sizes()[index]

    def mass_center_of(self, voxel_id):
        index = self.index_of(voxel_id)
        return self.mass_center()[index]

    def get_supervoxel_neighbors(self):
        """
        Retrieves a list of all neighbor pairs in this chunk.
        E.g., if supervoxel 1 has neighbors 2, 3 and 4, the list would contain these sets:
        (1, 2), (1, 3), (1, 4)
        :return: a list of neighbor pairs as frozensets
        """
        neighbors = set()
        for z in range(138):
            for y in range(140):
                for x in range(140):
                    curr_id = self.seg()[x][y][z]
                    left = self.seg()[x-1][y][z] if x > 0 else curr_id
                    right = self.seg()[x+1][y][z] if x < self.size[0] - 1 else curr_id
                    top = self.seg()[x][y-1][z] if y > 0 else curr_id
                    bottom = self.seg()[x][y+1][z] if y < self.size[1] - 1 else curr_id
                    back = self.seg()[x][y][z-1] if z > 0 else curr_id
                    front = self.seg()[x][y][z+1] if z < self.size[2] - 1 else curr_id
                    if curr_id != left:
                        neighbors.add(frozenset([curr_id, left]))
                    if curr_id != right:
                        neighbors.add(frozenset([curr_id, right]))
                    if curr_id != top:
                        neighbors.add(frozenset([curr_id, top]))
                    if curr_id != bottom:
                        neighbors.add(frozenset([curr_id, bottom]))
                    if curr_id != back:
                        neighbors.add(frozenset([curr_id, back]))
                    if curr_id != front:
                        neighbors.add(frozenset([curr_id, front]))
        return neighbors

    def get_overlapping_chunks(self,):
        # 27 chunks (including itself) overlap this chunk
        # self, below and above
        overlaps = [self.number, self.number - 1, self.number + 1]
        # back, back below, back above
        overlaps += [self.number - 11, self.number - 11 - 1, self.number - 11 + 1]
        # front, front below, front above
        overlaps += [self.number + 11, self.number + 11 - 1, self.number + 11 + 1]
        # left, left below, left above
        overlaps += [self.number - 164, self.number - 164 - 1, self.number - 164 + 1]
        # right, right below, right above
        overlaps += [self.number + 164, self.number + 164 - 1, self.number + 164 + 1]
        # left back, left back below, left back above
        overlaps += [self.number - 164 - 11, self.number - 164 - 11 - 1, self.number - 164 - 11 + 1]
        # left front, left front below, left front above
        overlaps += [self.number - 164 + 11, self.number - 164 + 11 - 1, self.number - 164 + 11 + 1]
        # right back, right back below, right back above
        overlaps += [self.number + 164 - 11, self.number + 164 - 11 - 1, self.number + 164 - 11 + 1]
        # right front, right front below, right front above
        overlaps += [self.number + 164 + 11, self.number + 164 + 11 - 1, self.number + 164 + 11 + 1]
        return overlaps