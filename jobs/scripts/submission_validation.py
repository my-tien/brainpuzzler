__author__ = 'tieni'

import h5py
from xml.dom import minidom

from jobs.models import Submission, get_overlapping_jobs

info_path = "/home/knossos/chunk_infos/"
box_size = (1120, 1120, 419)
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


def get_neighbors(chunk_number):
    """
    :param chunk_number:
    :return:
    """
    with h5py.File(info_path + "chunk{0}_values.h5".format(chunk_number), 'r') as chunk_file:
        seg = chunk_file['seg'].value
        neighbors = set()
        for z in range(138):
            for y in range(140):
                for x in range(140):
                    curr_id = seg[x][y][z]
                    left = seg[x-1][y][z] if x > 0 else curr_id
                    right = seg[x+1][y][z] if x < 139 else curr_id
                    top = seg[x][y-1][z] if y > 0 else curr_id
                    bottom = seg[x][y+1][z] if y < 139 else curr_id
                    back = seg[x][y][z-1] if z > 0 else curr_id
                    front = seg[x][y][z+1] if z < 137 else curr_id
                    if curr_id != left:
                        neighbors.add(frozenset([curr_id, left]))
                    if curr_id != right:
                        neighbors.add(frozenset([curr_id, right]))
                    if curr_id != top:
                        neighbors.add(frozenset([curr_id, top]))
                    if curr_id != bottom:
                        neighbors.add(frozenset([curr_id, bottom]))
                    if curr_id != back:
                        neighbors.add(frozenset([curr_id, back]))
                    if curr_id != front:
                        neighbors.add(frozenset([curr_id, front]))
        return neighbors


def get_overlap_submissions(chunk_number):
    overlaps = get_overlapping_jobs(chunk_number)
    mergelists = []
    for submission in Submission.objects.filter(job__chunk_number__in=overlaps):
        mergelists.append(submission.mergelist())

    neighbor_set = get_neighbors(chunk_number)
    merges = []
    for neighbor_pair in neighbor_set:
        neighbors = [neighbor for neighbor in neighbor_pair]
        vote = 0
        for mergelist in mergelists:
            vote += 1 if are_merged(mergelist, neighbors[0], neighbors[1]) else 0
        print("vote: {0}".format(vote))
        if vote > 2:
            merges.append(neighbors)
    print(merges)


# class Chunk:
#     info_path = "/home/knossos/chunk_infos/"
#     correct_merges = []
#     with open(info_path + "correct_merges.txt", 'r') as merges_file:
#         for line in merges_file:
#             correct_merges.append(line.split())
#         correct_merges = [list(map(int, group)) for group in correct_merges]
#
#     def __init__(self, chunk_id):
#         self.chunk_id = chunk_id
#
#         with h5py.File(Chunk.info_path + "chunk{0}_info.h5".format(chunk_id), 'r') as chunk_file:
#             self.ids = chunk_file['ids'].value
#         self.correct_merges = \
#             [[subobj_id for subobj_id in group if subobj_id in self.ids] for group in Chunk.correct_merges]
#         self.correct_merges = [group for group in self.correct_merges if len(group) > 1]
#
#     def is_valid(self, kzip_path):
#         try:
#             with ZipFile(kzip_path, 'r') as kzip, kzip.open("mergelist.txt", 'r') as mergelist:
#                 if num_split_requests(mergelist) >= 10:
#                     return False
#                 if len(self.correct_merges) == 0:
#                     return True
#                 merges = get_merged_groups(mergelist)
#                 for correct_merge in self.correct_merges:
#                     for merge in merges:
#                         if len(set(merge).intersection(correct_merge)) >= 1:
#                             return True
#             return False
#         except IOError:
#             print("IOError opening kzip: " + kzip_path)
#             return False
#
#
#
#
#
# def get_merged_groups(mergelist):
#     merges = []
#     for line in mergelist:
#         line = str(line)[:-3]  # bytes to string and trim trailing newline
#         subobjects = line.split()[3:]
#         if len(subobjects) > 1:
#             merges.append(subobjects)
#
#     for group_index in range(len(merges)):
#         for object_id in merges[group_index]:
#             for group_index2 in range(len(merges)):
#                 if group_index != group_index2 and object_id in merges[group_index2]:
#                     merges[group_index] = list(set(merges[group_index]).union(merges[group_index2]))
#                     merges[group_index2] = []
#     merges = [group for group in merges if len(group) != 0]
#     merges = [list(map(int, group)) for group in merges]
#     return merges