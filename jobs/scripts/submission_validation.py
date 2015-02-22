__author__ = 'tieni'

import os
from xml.dom import minidom
from zipfile import ZipFile

from brainpuzzler.settings import MEDIA_ROOT


min_secs_per_task = 4
max_split_requests = 10


def num_split_requests(mergelist):
    count = 0
    for line in mergelist:
        if "Split request" in str(line, 'utf-8'):
            count += 1
    return count


def seconds_per_todo(annotation, num_todos):
    dom = minidom.parseString(str(annotation.read(), 'utf-8'))
    time = float(dom.getElementsByTagName("time")[0].attributes["ms"].value)
    return time / 1000 / num_todos


def number_todos(mergelist):
    return len([str(line, 'utf-8') for line in mergelist]) / 4


def is_valid(submission):
    submission_path = MEDIA_ROOT + os.path.basename(submission.submit_file.name)
    job_path = MEDIA_ROOT + os.path.basename(submission.job.job_file.name)
    try:
        with ZipFile(job_path, 'r') as job, job.open("mergelist.txt", 'r') as job_mergelist, \
                ZipFile(submission_path, 'r') as submit, \
                submit.open("annotation.xml", 'r') as annotation, submit.open("mergelist.txt", 'r') as submit_mergelist:
            secs_per_todo = seconds_per_todo(annotation, number_todos(job_mergelist))
            print("time per todo: {0}, split requests: {1}".format(secs_per_todo, num_split_requests(submit_mergelist)))
            if secs_per_todo < min_secs_per_task or num_split_requests(submit_mergelist) > max_split_requests:
                return False
            return True
    except IOError:
        print("Failed to find all relevant files for submission " + str(submission))

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