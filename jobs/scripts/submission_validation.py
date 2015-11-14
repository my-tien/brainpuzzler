__author__ = 'tieni'
import cProfile
import networkx as nx
import numpy
import os
from xml.dom import minidom

from jobs.chunk import Chunk
from jobs.mergelist import Mergelist, SegObject
min_secs_per_task = 4
max_split_requests = 10

from dataset_utils import knossosDataset

barrier_dataset = knossosDataset()
barrier_dataset.initialize_from_knossos_path("specify path to a dataset")

basedir = "set basedir"

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


def in_barrier(subobject_id, chunk, barrier_map):
    area = numpy.where(chunk.seg() == subobject_id)
    area2_isotrop = [elem/2 for elem in area[2]]
    num_voxels = len(area[0])
    if sum(barrier_map[area[0], area[1], area2_isotrop]) / num_voxels > .6:
        return True
    return False

def sub_obj_barrier_prob_dict(chunk, barrier_map):
    temp_dic = {}
    keys = numpy.unique(chunk.seg()) # significantly faster than iterating over chunk.ids()
    for k in keys:
        temp_dic[k] = [0, 0] # {subobj_id : [sum_probabilities, num_voxels]}

    length = [len(chunk.seg()), len(chunk.seg()[0]), len(chunk.seg()[0][0])]
    ranges = (range(0, length[0]), range(0, length[1]), range(0, length[2]))
    for x in ranges[0]:
        xseg = chunk.seg()[x]
        xbarrier = barrier_map[x]
        for y in ranges[1]:
            yseg = xseg[y]
            ybarrier = xbarrier[y]
            for z in ranges[2]:
                probability = temp_dic[yseg[z]]
                probability[0] += ybarrier[z / 2]
                probability[1] += 1

    result_dict = {}
    for key, value in temp_dic.items():
        result_dict[key] = value[0] / (value[1] * 255.)
    return result_dict

def write_voted_mergelist(chunk_number, mergelists, outputpath, size_vote_map=None, include_unmerged_subobjects=True):
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
    :param size_vote_map: Map of supervoxel size to required number of votes for merging.
                          Allowed values: "one", {n|n\xcf[0,1]}
                          If no map is specified, the vote boundary is always 50%
    """
    chunks = {chunk_number: Chunk(chunk_number)}
    barrier_map = barrier_dataset.from_cubes_to_matrix([140, 140, 69], chunks[chunk_number].coordinates(), type="raw")
    neighbor_sets = dict()

    for mergelist in mergelists:
        curr_chunk = Chunk(mergelist[1])
        with open(basedir + "neighbors/chunk_{0}.txt".format(curr_chunk.number), 'r') as neighbor_file:
            neighbor_set = set()
            for line in neighbor_file:
                neighbor_set.add(frozenset([int(elem) for elem in line.split()]))
        neighbor_sets[mergelist[1]] = neighbor_set

    if size_vote_map is None:
        size_vote_map = {float("inf"): 0.5}
    sorted_keys = sorted(size_vote_map.keys())

    merges = []
    barrier_probabilities = sub_obj_barrier_prob_dict(chunks[chunk_number], barrier_map)
    solos = set()
    for neighbor_pair in neighbor_sets[chunk_number]:  # majority vote for merging the neighbor pair
        neighbors = list(neighbor_pair)
        if barrier_probabilities[neighbors[0]] < 0.5 and barrier_probabilities[neighbors[1]] < 0.5:
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
                if key > chunks[chunk_number].size_of(neighbors[0]) or key > chunks[chunk_number].size_of(neighbors[1]):
                    votes_required = size_vote_map[key]
                    vote_boundary = 1 if votes_required == "one" else votes_required * overlaps
                    break
            try:
                if vote >= vote_boundary:
                    print("overlaps: {0}, votes: {1}".format(overlaps, vote))
                    merges.append(neighbors)
                    try:
                        solos.remove(neighbors[0])
                    except KeyError:
                        pass
                    try:
                        solos.remove(neighbors[1])
                    except KeyError:
                        pass
            except TypeError:
                print('Invalid (size: vote) map. Allowed values are "one" or {n|n\xcf[0,1]}')
                return

        elif barrier_probabilities[neighbors[0]] < 0.5:
            solos.add(neighbors[0])
        elif barrier_probabilities[neighbors[1]] < 0.5:
            solos.add(neighbors[1])

    merges = build_connected_components(merges)

    if include_unmerged_subobjects:
        merges += [set([solo]) for solo in solos]

    majority_mergelist = Mergelist()
    obj_id = 1
    for merge in merges:
        coord = chunks[chunk_number].mass_center_of(next(iter(merge)))
        majority_mergelist.seg_objects.append(SegObject(obj_id, 0, 1, coord, merge))
        obj_id += 1
    majority_mergelist.write(outputpath)