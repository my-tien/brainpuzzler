__author__ = 'tieni'
from jobs.chunk import Chunk
from jobs.mergelist import Mergelist

control_path = "/home/knossos/conventional_submits/mergelists/mergelist_"
test_path = "/home/knossos/mergelists/mergelist_"


def run(*args):
    if len(args) != 1:
        print("Usage: compare_submits --script-args=chunk_number")
        return

    control_list = Mergelist(control_path + args[0] + ".txt")
    mergelist = Mergelist(test_path + args[0] + ".txt")
    chunk = Chunk(int(args[0]))
    control_sizes = {}
    for seg_obj in control_list.seg_objects:
        control_sizes[seg_obj.id] = 0
        for supervoxel in seg_obj.supervoxels:
            control_sizes[seg_obj.id] += chunk.size_of(supervoxel)
    abs_errors = {}
    for seg_obj in [seg_object for seg_object in mergelist.seg_objects if "ecs" not in seg_object.comment]:
        test_voxels = seg_obj.supervoxels
        max_intersects = 0
        matching_object = None
        for control_obj in control_list.seg_objects:
            intersection = len(set(control_obj.supervoxels) & test_voxels)
            if intersection > max_intersects:
                max_intersects = intersection
                matching_object = control_obj
        if matching_object is None:
            continue
        if matching_object.id == 4:
            print("matching control object: {0}, len: {1}, test object: {2}, test len {3}, max intersects: {4}".format(matching_object.id, len(matching_object.supervoxels), seg_obj.id, len(seg_obj.supervoxels), max_intersects))
        control_voxels = matching_object.supervoxels
        difference = (test_voxels ^ control_voxels) - (test_voxels & control_voxels)
        if matching_object.id == 4:
            print("difference: {0}".format(len(difference)))
        abs_errors[matching_object.id] = 0
        for supervoxel in difference:
            if matching_object.id == 4:
                print("supervoxel {0}, size: {1}".format(supervoxel, chunk.size_of(supervoxel)))
            abs_errors[matching_object.id] += chunk.size_of(supervoxel)

    print("actual size: {0}".format(control_sizes[4]))
    rel_errors = {}
    for obj_id, error in abs_errors.items():
        rel_errors[obj_id] = error / control_sizes[obj_id]
    print(rel_errors)
    for obj_id, rel_error in rel_errors.items():
        print("{0}: {1:.2f}% error".format(obj_id, rel_error))
    total_error = sum(abs_errors.values())
    total_size = sum(control_sizes.values())
    print("total error: {0:.2f}% ({1}/{2})".format(total_error/total_size, total_error, total_size))
