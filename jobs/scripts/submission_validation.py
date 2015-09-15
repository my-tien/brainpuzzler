__author__ = 'tieni'

import networkx as nx
import numpy
import os
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


def build_connected_components(objects):
    G = nx.Graph()
    for obj in objects:
        first = obj.pop()
        while obj:
            G.add_edge(first, obj.pop())
    return list(nx.connected_components(G))


def write_voted_mergelist_respect_voxelsize(chunk_number, mergelists, outputpath, size_vote_map):
    """
    Write a unified mergelist from all available mergelists to this chunk.

    Unification is done through three steps:
     1. Gather all existing supervoxel neighbor pairs in the chunk.
     2. Test for each neighbor pair if it should be merged through majority vote with all available mergelists.
        Required votes depend on the size of each supervoxel as specified in size_vote_map.
     3. Move resulting merge pairs into their respective connected components.

    :param chunk_number: The chunk for which to generate a majority voted mergelist
    :param mergelists: The input mergelists
    :param outputpath: Absolute output path for majority vote mergelist
    :param size_vote_map: Map of supervoxel size to required number of votes for merging. Allowed values: "one", {n|nϵ[0,1]}
    """
    chunks = {chunk_number: Chunk(chunk_number)}
    neighbor_sets = {}
    for mergelist in mergelists:
        with open("/home/tieni/brainpuzzler/data/neighbors/chunk_{0}.txt".format(mergelist[1]), 'r') as neighbor_file:
            neighbor_set = set()
            for line in neighbor_file:
                neighbor_set.add(frozenset([int(value) for value in line.split()]))
        neighbor_sets[mergelist[1]] = neighbor_set

    sorted_keys = sorted(size_vote_map.keys())
    merges = []
    for neighbor_pair in neighbor_sets[chunk_number]:  # majority vote for merging the neighbor pair
        neighbors = list(neighbor_pair)
        vote = 0
        overlaps = 0
        for mergelist in mergelists:
            if neighbor_pair in neighbor_sets[mergelist[1]]:
                ids1 = mergelist[0].contained_in(neighbors[0])
                ids2 = mergelist[0].contained_in(neighbors[1])
                overlaps += 1
                vote += 1 if len(ids1 & ids2) > 0 else 0  # only mergelists containing both objects can participate
        # determine minimum votes required based on size of smaller supervoxel
        vote_boundary = 1
        for key in sorted_keys:
            if key > neighbors[0] or key > neighbors[1]:
                votes_required = size_vote_map[key]
                vote_boundary = 1 if votes_required == "one" else votes_required * overlaps
                break
        try:
            if vote >= vote_boundary:
                print("overlaps: {0}, votes: {1}".format(overlaps, vote))
                merges.append(neighbors)
        except TypeError:
            print('Invalid (size: vote) map. Allowed values are "one" or {n|nϵ[0,1]}')
            return

    merges = build_connected_components(merges)

    for obj_id in chunks[chunk_number].ids():
        existent = False
        for group in merges:
            if obj_id in group:
                existent = True
                break
        if not existent:
            merges.append([obj_id])

    majority_mergelist = Mergelist()
    obj_id = 1
    for merge in merges:
        coord = chunks[chunk_number].mass_center_of(merge[0])
        majority_mergelist.seg_objects.append(SegObject(obj_id, 0, 1, coord, merge))
        obj_id += 1
    majority_mergelist.write(outputpath)


def write_majority_vote_mergelist(chunk_number, mergelists, outputpath, min_vote=0):
    """
    Write a unified mergelist from all available mergelists to this chunk.

    Unification is done through three steps:
     1. Gather all existing supervoxel neighbor pairs in the chunk.
     2. Test for each neighbor pair if it should be merged through majority vote with all available mergelists.
     3. Move resulting merge pairs into their respective connected components.

    :param chunk_number: The chunk for which to generate a majority voted mergelist
    :param mergelists: the input mergelists
    :param outputpath: absolute output path for majority vote mergelist
    :param min_vote: minimum number of votes to accept a pair of supervoxels to merge
    """
    chunks = {chunk_number: Chunk(chunk_number)}
    neighbor_sets = {}
    for mergelist in mergelists:
        with open("/home/tieni/brainpuzzler/data/neighbors/chunk_{0}.txt".format(mergelist[1]), 'r') as neighbor_file:
            neighbor_set = set()
            for line in neighbor_file:
                neighbor_set.add(frozenset([int(value) for value in line.split()]))
        neighbor_sets[mergelist[1]] = neighbor_set

    merges = []
    for neighbor_pair in neighbor_sets[chunk_number]:  # majority vote for merging the neighbor pair
        neighbors = list(neighbor_pair)
        vote = 0
        overlaps = 0
        for mergelist in mergelists:
            if neighbor_pair in neighbor_sets[mergelist[1]]:
                ids1 = mergelist[0].contained_in(neighbors[0])
                ids2 = mergelist[0].contained_in(neighbors[1])
                overlaps += 1
                vote += 1 if len(ids1 & ids2) > 0 else 0  # only mergelists containing both objects can participate
        if vote > max(min_vote, overlaps/2):
            print("overlaps: {0}, votes: {1}".format(overlaps, vote))
            merges.append(neighbors)

    merges = build_connected_components(merges)

    for obj_id in chunks[chunk_number].ids():
        existent = False
        for group in merges:
            if obj_id in group:
                existent = True
                break
        if not existent:
            merges.append([obj_id])

    majority_mergelist = Mergelist()
    obj_id = 1
    for merge in merges:
        coord = chunks[chunk_number].mass_center_of(merge[0])
        majority_mergelist.seg_objects.append(SegObject(obj_id, 0, 1, coord, merge))
        obj_id += 1
    majority_mergelist.write(outputpath)