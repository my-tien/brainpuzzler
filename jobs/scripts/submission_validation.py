__author__ = 'tieni'

import numpy
from xml.dom import minidom

from jobs.chunk import Chunk
from jobs.mergelist import Mergelist, SegObject

min_secs_per_task = 4
max_split_requests = 10


def seconds_per_todo(annotation, num_todos):
    dom = minidom.parseString(annotation)
    time = float(dom.getElementsByTagName("time")[0].attributes["ms"].value)
    if num_todos > 0:
        return time / 1000 / num_todos


def is_acceptable(submission):
    job_mergelist = submission.job.mergelist()
    annotation = submission.annotation()
    submit_mergelist = submission.mergelist()
    if not annotation or not submit_mergelist:
        return False

    secs_per_todo = seconds_per_todo(annotation, job_mergelist.number_todos())
    if secs_per_todo is None:
        print("No todos in {0}".format(submission))
        return True
    else:
        split_requests = submit_mergelist.count_comment("Split request")
        print("time per todo: {0:.2f}, split requests: {1}, {2}"
              .format(secs_per_todo, split_requests, submission))
        if secs_per_todo < min_secs_per_task or split_requests > max_split_requests:
            return False
    return True


def has_0_time(submission):
    job_mergelist = submission.job.mergelist()
    annotation = submission.annotation()
    secs_per_todo = seconds_per_todo(annotation, job_mergelist.number_todos())
    if secs_per_todo == 0:
        return True
    return False


def write_majority_vote_mergelist(chunk_number, mergelists):
    chunk = Chunk(chunk_number)
    neighbor_set = chunk.get_supervoxel_neighbors()
    merges = []
    for neighbor_pair in neighbor_set:
        neighbors = [neighbor for neighbor in neighbor_pair]
        vote = 0
        for mergelist in mergelists:
            vote += 1 if mergelist.are_merged(neighbors[0], neighbors[1]) else 0
        if vote > 2:
            merges.append(neighbors)

    indices_to_del = []
    for index, neighbor_pair in enumerate(merges):
        if index in indices_to_del:
            continue
        connected = [neighbor_pair[0], neighbor_pair[1]]
        for index2, neighbor_pair2 in enumerate(merges):
            if neighbor_pair == neighbor_pair2 or index2 in indices_to_del:
                continue
            if len([val for val in neighbor_pair2 if val in connected]) != 0:
                connected += neighbor_pair2
                indices_to_del.append(index2)
        neighbor_pair += connected

    indices_to_del.sort()
    for index in indices_to_del[::-1]:
        merges.pop(index)
    merges = [set(merged_neighbor) for merged_neighbor in merges]

    for obj_id in chunk.ids():
        existent = False
        for group in merges:
            if obj_id in group:
                existent = True
                break
        if not existent:
            merges.append({obj_id})

    merges = [list(merger) for merger in merges]
    majority_mergelist = Mergelist()
    index = 1
    for merge in merges:
        coord = chunk.mass_centers()[merge[0]]
        majority_mergelist.seg_objects.append(SegObject(index, 0, 1, coord, merge))
        index += 1
    majority_mergelist.write("/home/knossos/mergelist_{0}.txt".format(chunk_number))