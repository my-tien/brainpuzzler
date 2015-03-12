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
        neighbor1 = neighbor_pair.pop()
        neighbor2 = neighbor_pair.pop()
        vote = 0
        overlaps = 0
        for mergelist in mergelists:
            ids1 = mergelist.contained_in(neighbor1)
            ids2 = mergelist.contained_in(neighbor2)
            if len(ids1) > 0 and len(ids2) > 0:  # only mergelists containing both objects can participate
                overlaps += 1
                vote += 1 if len(set(ids1).intersection(ids2)) > 0 else 0
        if vote > overlaps/2:
            merges.append({neighbor1, neighbor2})
    # move merge pairs into their respective connected components
    indices_to_del = []  # remembers all visited pairs
    for index, pair1 in enumerate(merges):
        if index in indices_to_del:
            continue
        for index2, pair2 in enumerate(merges):
            if index2 in indices_to_del or index2 == index:
                continue
            if len(pair2.intersection(merges[index])) != 0:  # if one neighbor in component, add the other too
                merges[index] = merges[index].union(pair2)
                indices_to_del.append(index2)

    # now remove all pairs that have been moved to a component
    indices_to_del.sort()
    for index in indices_to_del[::-1]:
        merges.pop(index)

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
    index = 1
    for merge in merges:
        coord = chunk.mass_centers()[chunk.index_of(merge[0])][0]
        majority_mergelist.seg_objects.append(SegObject(index, 0, 1, coord, merge))
        index += 1
    majority_mergelist.write(path)