__author__ = 'tieni'

import numpy
from xml.dom import minidom

from jobs.chunk import Chunk

min_secs_per_task = 4
max_split_requests = 10


def num_split_requests(mergelist):
    count = 0
    for line in mergelist.split('\n'):
        if "Split request" in line:
            count += 1
    return count


def seconds_per_todo(annotation, num_todos):
    dom = minidom.parseString(annotation)
    time = float(dom.getElementsByTagName("time")[0].attributes["ms"].value)
    if num_todos > 0:
        return time / 1000 / num_todos


def number_todos(mergelist):
    return len([line for line in mergelist.split('\n')]) / 4


def are_merged(mergelist, id1, id2):
    id1 = str(id1)
    id2 = str(id2)
    for line in mergelist.split('\n'):
        if id1 in line and id2 in line:
            return True
    return False


def is_acceptable(submission):
    job_mergelist = submission.job.mergelist()
    annotation = submission.annotation()
    submit_mergelist = submission.mergelist()
    if not annotation or not submit_mergelist:
        return False

    secs_per_todo = seconds_per_todo(annotation, number_todos(job_mergelist))
    if secs_per_todo is None:
        print("No todos in {0}".format(submission))
        return True
    else:
        print("time per todo: {0:.2f}, split requests: {1}, {2}"
              .format(secs_per_todo, num_split_requests(submit_mergelist), submission))
        if secs_per_todo < min_secs_per_task or num_split_requests(submit_mergelist) > max_split_requests:
            return False
    return True


def has_0_time(submission):
    job_mergelist = submission.job.mergelist()
    annotation = submission.annotation()
    secs_per_todo = seconds_per_todo(annotation, number_todos(job_mergelist))
    if secs_per_todo == 0:
        return True
    return False


def write_mergelist(chunk, merges, path):
    with open(path + "mergelist_{0}.txt".format(chunk.number), 'w') as mergelist:
        counter = 1
        for group in merges:
            group = [str(obj_id) for obj_id in group]
            first_id = numpy.where(chunk.ids() == int(group[0]))
            coord = chunk.mass_center()[first_id][0]
            mergelist.write("{0} 0 1 {1}\n{2} {3} {4}\n\n\n".format(counter, ' '.join(group), coord[0], coord[1], coord[2]))
            counter += 1


def write_majority_vote_mergelist(chunk_number, mergelists):
    chunk = Chunk(chunk_number)
    neighbor_set = chunk.get_supervoxel_neighbors()
    merges = []
    for neighbor_pair in neighbor_set:
        neighbors = [neighbor for neighbor in neighbor_pair]
        vote = 0
        for mergelist in mergelists:
            vote += 1 if are_merged(mergelist, neighbors[0], neighbors[1]) else 0
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

    write_mergelist(chunk, merges, "/home/knossos/")