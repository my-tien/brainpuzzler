__author__ = 'tieni'

import os
from zipfile import ZipFile
from brainpuzzler.settings import MEDIA_ROOT


def todolist_is_unhandled(kzip_path):
    """
    Checks if the specified mergelist contains a todo list, that has not been handled at all.
    This is the case if each object has exactly one subobject, meaning that no merges have been performed.
    :param kzip_path: absolute path of mergelist.txt
    :return: true if  todo list has not been handled, false otherwise
    """
    with ZipFile(kzip_path, 'r') as kzip, kzip.open("mergelist.txt", 'r') as todolist:
            for line in todolist:
                line = str(line, encoding='utf-8')
                if len(line.split()[3:]) > 1:
                    return False
            return True


def get_unhandled_todolists(folder, basename):
    """
    lists all unhandled todolists inside specified folder starting with 'basename'
    :param folder: the folder in which to search for unchanged todolists
    :param basename: name to filter for, e.g. basename == "finished" means we search for "finished*"
    :return: .k.zip filename list of unchanged todolists without folder path
    """
    unchanged_todolists = []
    for file in os.listdir(folder):
        if file.startswith(basename) and todolist_is_unhandled(folder + file):
            unchanged_todolists.append(file)
    return unchanged_todolists


def run(*args):
    file_list = get_unhandled_todolists(MEDIA_ROOT, "segmentationJobsfinal_")
    if len(file_list) == 0:
        print("There are no unhandled todolists in this folder.")
        return

    file_list.sort()
    print('\n'.join(file_list))

    if "delete" in args:
        for name in file_list:
            os.remove(MEDIA_ROOT + name)