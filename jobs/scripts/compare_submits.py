__author__ = 'tieni'
from jobs.chunk import Chunk
from jobs.mergelist import Mergelist


def run(*args):
    if len(args) != 2:
        print("Usage: compare_submits --script-args=control_mergelist mergelist")
        return

    control_list = Mergelist(args[0])
    mergelist = Mergelist(args[1])
    chunk = Chunk(1109)
    control_sizes = {}
    for seg_obj in control_list.seg_objects:
        control_sizes[seg_obj.id] = 0
        for supervoxel in seg_obj.supervoxels:
            control_sizes[seg_obj.id] += chunk.size_of(supervoxel)

    abs_error = {}
    for seg_obj in mergelist.seg_objects:
        control_voxels = control_list.seg_objects[seg_obj.id].supervoxels
        test_voxels = seg_obj.supervoxels
        difference = (test_voxels ^ control_voxels) - (test_voxels & control_voxels)
        abs_error[seg_obj.id] = 0
        for supervoxel in difference:
            abs_error[seg_obj.id] += chunk.size_of(supervoxel)

    rel_error = {}
    for obj_id, error in abs_error.items():
        rel_error[obj_id] = error / control_sizes[obj_id]
