__author__ = 'tieni'

import numpy
import cProfile
from jobs.scripts.submission_validation import get_overlap_submissions


def run(*args):
    cProfile.runctx("get_overlap_submissions(1400)", globals(), locals())
    # get_overlap_submissions(1400)
