__author__ = 'tieni'

import os
from zipfile import ZipFile

from jobs.models import Submission
from brainpuzzler.settings import MEDIA_ROOT


def todolist_is_unhandled(kzip_path):
    """
    Checks if the specified mergelist contains a todo list, that has not been handled at all.
    This is the case if each object has exactly one subobject, meaning that no merges have been performed.
    :param kzip_path: absolute path of mergelist.txt
    :return: true if  todo list has not been handled, false otherwise
    """
    try:
        with ZipFile(kzip_path, 'r') as kzip, kzip.open("mergelist.txt", 'r') as todolist:
                for line in todolist:
                    line = str(line, encoding='utf-8')
                    if len(line.split()[3:]) > 1:
                        return False
                return True
    except IOError:
        print(kzip_path + " could not be opened.")
        return True
    except KeyError:
        print("mergelist.txt was not found in " + kzip_path)
        return True


def get_invalid_submissions(folder, basename):
    """
    lists all invalid submissions (submissions with unhandled todolists) inside specified folder starting with 'basename'
    :param folder: the folder in which to search for unchanged todolists
    :param basename: name to filter for, e.g. basename == "finished" means we search for "finished*"
    :return: list of invalid submissions
    """
    invalid_submissions = []
    for file in os.listdir(folder):
        if file.startswith(basename) and todolist_is_unhandled(folder + file):
            try:
                invalid_submissions.append(Submission.objects.filter(submit_file="./" + file)[0])
            except IndexError:
                continue
    return invalid_submissions


def run(*args):
    submissions = get_invalid_submissions(MEDIA_ROOT, "segmentationJobsfinal_")
    if len(submissions) == 0:
        print("There are no invalid submissions in this folder.")
        return

    tokens = [submission.token for submission in submissions]
    tokens.sort()
    print('\n'.join(tokens))

    if "delete" in args:
        for submission in submissions:
            submission.delete()
            os.remove(MEDIA_ROOT + os.path.basename(submission.submit_file.name))  # filefield never deletes backend storage