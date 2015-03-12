__author__ = 'tieni'

import numpy
from xml.dom import minidom

from jobs.chunk import Chunk
from jobs.mergelist import Mergelist, SegObject

min_secs_per_task = 4
max_split_requests = 10


def time(annotation):
    dom = minidom.parseString(annotation)
    return float(dom.getElementsByTagName("time")[0].attributes["ms"].value)


def is_acceptable(submission):
    job_mergelist = submission.job.mergelist()
    annotation = submission.annotation()
    submit_mergelist = submission.mergelist()
    if not annotation or not submit_mergelist:
        return False

    secs_per_todo = time(annotation) / 1000 / job_mergelist.number_todos()
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
    xml_time = time(annotation)
    secs_per_todo = xml_time / 1000 / job_mergelist.number_todos()
    if secs_per_todo == 0:
        return True
    return False


def write_majority_vote_mergelist(chunk_number, mergelists, include_solos, path):
    """
    Write a unified mergelist from all available mergelists to this chunk.

    Unification is done through three steps:
     1. Gather all existing supervoxel neighbor pairs in the chunk.
     2. Test for each neighbor pair if it should be merged through majority vote with all available mergelists.
     3. Move resulting merge pairs into their respective connected components.

    :param chunk_number: The chunk receiving a mergelist
    :param mergelists: the input mergelists
    :param path: absolute output path for majority vote mergelist
    """
    chunk = Chunk(chunk_number)
    neighbor_set = chunk.get_supervoxel_neighbors()
    merges = []
    for neighbor_pair in neighbor_set:  # majority vote for merging the neighbor pair
        neighbors = [neighbor for neighbor in neighbor_pair]
        vote = 0
        overlaps = 0
        for mergelist in mergelists:
            ids1 = mergelist.contained_in(neighbors[0])
            ids2 = mergelist.contained_in(neighbors[1])
            if len(ids1) > 0 and len(ids2) > 0:  # only mergelists containing both objects can participate
                overlaps += 1
                vote += 1 if len(ids1 & ids2) > 0 else 0
        if vote > overlaps/2:
            merges.append(neighbors)

    # move merge pairs into their respective connected components
    indices_to_skip = []  # remembers all visited pairs
    for index, pair1 in enumerate(merges):
        if index in indices_to_skip:
            continue
        connected = [pair1[0], pair1[1]]
        for index2, pair2 in enumerate(merges):
            if pair2 == pair1 or index2 in indices_to_skip:
                continue
            if len([val for val in pair2 if val in connected]) != 0:  # if one neighbor in component, add the other too
                connected += pair2
                indices_to_skip.append(index2)
        pair1 += connected

    merges = [set(group) for group in merges]
    if include_solos:  # add all unmerged subobjects too
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
    for index, merge in enumerate(merges):
        if index in indices_to_skip:
            continue
        coord = chunk.mass_centers()[chunk.index_of(merge[0])][0]
        majority_mergelist.seg_objects.append(SegObject(index, 0, 1, coord, merge))
    majority_mergelist.write(path)