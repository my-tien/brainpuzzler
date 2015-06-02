__author__ = 'tieni'

import h5py
import math
import numpy

base_coords = [4840, 4712, 2630]
chunks_in_z = 11
chunks_in_xy = 15


class Chunk:
    width = 140
    depth = 138
    info_path = "/home/knossos/chunk_infos/"

    def __init__(self, chunk_number):
        self.number = chunk_number
        self._seg = None
        self._ids = None
        self._mass_center = None
        self._sizes = None

    def read_seg(self):
        with h5py.File(Chunk.info_path + "chunk{0}_values.h5".format(self.number), 'r') as values:
            self._seg = values['seg'].value

    def read_info(self):
        with h5py.File(Chunk.info_path + "chunk{0}_info.h5".format(self.number), 'r') as info:
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

    def mass_centers(self):
        if self._mass_center is None:
            self.read_info()
        return self._mass_center

    def sizes(self):
        if self._sizes is None:
            self.read_info()
        return self._sizes

    def index_of(self, voxel_id):
        index = numpy.where(self.ids() == voxel_id)
        return index if len(index[0]) > 0 else -1

    def size_of(self, voxel_id):
        index = self.index_of(voxel_id)

        return self.sizes()[index][0] if index != -1 else -1

    def mass_center_of(self, voxel_id):
        index = self.index_of(voxel_id)
        return self.mass_centers()[index][0]

    def coordinates(self):
        chunk_number = self.number + 1  # first chunk has number 0
        number_bars = math.ceil(chunk_number/chunks_in_z)
        x = math.ceil(number_bars/chunks_in_xy)
        x = 0 if x < 1 \
            else int(x/2)*140 if x % 2 == 1 \
            else x/2 * 140 - 70
        x += base_coords[0]

        y = number_bars % chunks_in_xy
        # 980 == int(chunks_in_xy/2)*140
        y = 980 if y == 0 \
            else 0 if y < 1 \
            else int(y/2) * 140 if y % 2 == 1 \
            else y/2*140 - 70
        y += base_coords[1]

        z = chunk_number % 11
        # 350 == int(chunks_in_z/2) * 70
        z = 350 if z == 0 \
            else 0 if z < 1 \
            else int(z/2)*70 if z % 2 == 1 \
            else z/2*70 - 35
        z += base_coords[2]

        return [int(x), int(y), int(z)]

    def get_supervoxel_neighbors(self):
        """
        Retrieves a list of all neighbor pairs in this chunk.
        E.g., if supervoxel 1 has neighbors 2, 3 and 4, the list would contain these sets:
        (1, 2), (1, 3), (1, 4)
        :return: a list of neighbor pairs as frozensets
        """
        neighbors = set()
        seg = self.seg()
        for x in range(self.width):
            x_pos = seg[x]
            for y in range(self.width):
                xy_pos = x_pos[y]
                for z in range(self.depth):
                    curr_id = xy_pos[z]
                    left = seg[x-1][y][z] if x > 0 else curr_id
                    right = seg[x+1][y][z] if x < self.width - 1 else curr_id
                    top = x_pos[y-1][z] if y > 0 else curr_id
                    bottom = x_pos[y+1][z] if y < self.width - 1 else curr_id
                    back = xy_pos[z-1] if z > 0 else curr_id
                    front = xy_pos[z+1] if z < self.depth - 1 else curr_id
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