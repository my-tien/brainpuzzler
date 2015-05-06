__author__ = 'tieni'

from os import listdir

from jobs.chunk import Chunk
from jobs.mergelist import Mergelist
from jobs.plotter import save_histogram

control_path = "/home/knossos/control_lists/"
test_path = "/home/knossos/mergelists/"


def run(*args):
    if len(args) != 1:
        print("Usage: compare_submits --script-args=chunk_number|all")
        return
    files = [name for name in listdir(control_path)] if "all" in args else ["mergelist_{0}.txt".format(args[0])]
    relative_errors = []
    for name in files:
        number = int(name.split('_')[1][:-4])
        control_list = Mergelist(control_path + name)
        mergelist = Mergelist(test_path + name)
        chunk = Chunk(number)
        control_sizes = {}
        abs_errors = {}
        for seg_obj in [seg_object for seg_object in control_list.seg_objects if "neuron" in seg_object.comment]:
            # retrieve correct size for each neuron
            control_sizes[seg_obj.id] = 0
            for supervoxel in seg_obj.supervoxels:
                if chunk.index_of(supervoxel) == -1:
                    continue
                control_sizes[seg_obj.id] += chunk.size_of(supervoxel)

            # compare with most similar object in test-mergelist
            max_intersect_size = 0
            similar_object = None
            for test_obj in mergelist.seg_objects:
                intersection = seg_obj.supervoxels & test_obj.supervoxels
                intersect_size = 0
                for supervoxel in intersection:
                    intersect_size += chunk.size_of(supervoxel)
                if intersect_size > max_intersect_size:
                    max_intersect_size = intersect_size
                    similar_object = test_obj
            difference = (seg_obj.supervoxels ^ similar_object.supervoxels) - (seg_obj.supervoxels & similar_object.supervoxels)
            error = 0
            for supervoxel in difference:
                error += chunk.size_of(supervoxel)
            try:
                if error < abs_errors[seg_obj.id][0]:
                    abs_errors[seg_obj.id] = (error, similar_object.id)
            except KeyError:
                abs_errors[seg_obj.id] = (error, similar_object.id) if error < control_sizes[seg_obj.id] else (control_sizes[seg_obj.id], similar_object.id)

        rel_errors = {}
        for obj_id, error in abs_errors.items():
            # if error[1] == 10: print("ERROR: {0}, control {1}".format(error[0], control_sizes[obj_id]))
            rel_errors[obj_id] = error[0] / control_sizes[obj_id]
        for obj_id, rel_error in rel_errors.items():
            print("{0}: {1:.2f} error with obj {2}".format(obj_id, rel_error, abs_errors[obj_id][1]))
        total_error = sum([error[0] for error in abs_errors.values()])
        total_size = sum(control_sizes.values())
        relative_errors.append(total_error/total_size)
        print("chunk {0}: total error of {1:.2f} ({2}/{3})".format(number, total_error/total_size, total_error, total_size))
        print("relative errors: {0}".format(relative_errors))
    save_histogram(list(relative_errors), [0.01*x for x in range(0, 10)], "error in percent", "number of submits", "errors.png", False)
