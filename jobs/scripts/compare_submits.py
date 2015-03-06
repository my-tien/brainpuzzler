__author__ = 'tieni'
from jobs.chunk import Chunk
from jobs.mergelist import Mergelist


def run(*args):
    mergelist = Mergelist("/home/knossos/mergelist_1109.txt")
    chunk = Chunk(1109)
    sizes = {}
    for seg_obj in mergelist.seg_objects:
        sizes[seg_obj.id] = 0
        for supervoxel in seg_obj.supervoxels:
            sizes[seg_obj.id] += chunk.size_of(supervoxel)

