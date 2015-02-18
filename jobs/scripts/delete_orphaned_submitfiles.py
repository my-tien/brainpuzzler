__author__ = 'knossos'


import os

from brainpuzzler.settings import MEDIA_ROOT
from jobs.models import Submission


def run():
    counter = 0
    for filename in os.listdir(MEDIA_ROOT):
        if filename.startswith("segmentationJobsfinal_") and len(Submission.objects.filter(submit_file="./"+filename)) == 0:
            counter += 1
            print("Deleting file: " + filename)
            os.remove(MEDIA_ROOT + filename)
    print("Deleted {0} files.".format(counter))