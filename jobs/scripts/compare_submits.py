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

    abs_errors = {}
    for seg_obj in mergelist.seg_objects:
        test_voxels = seg_obj.supervoxels
        max_intersects = 0
        max_id = -1
        for control_obj in control_list.seg_objects:
            intersection = len(set(control_obj.supervoxels) & test_voxels)
            if intersection > max_intersects:
                max_intersects = intersection
                max_id = control_obj.id
        control_voxels = control_list.seg_objects[max_id].supervoxels
        difference = (test_voxels ^ control_voxels) - (test_voxels & control_voxels)
        abs_errors[max_id] = 0
        for supervoxel in difference:
            abs_errors[max_id] += chunk.size_of(supervoxel)

    rel_errors = {}
    for obj_id, error in abs_errors.items():
        rel_errors[obj_id] = error / control_sizes[obj_id]

    for obj_id, rel_error in rel_errors.items():
        print("{0}: {1:.2f)% error".format(obj_id, rel_error))
    total_error = sum(abs_errors.values())
    total_size = sum(control_sizes.values())
    print("total error: {0:2.f} ({1}/{2})".format(total_error/total_size, total_error, total_size))
