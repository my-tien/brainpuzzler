from django.db import models
from django.db.models import Q
import os
import random
from zipfile import ZipFile, BadZipfile

from jobs.chunk import Chunk
from jobs.mergelist import Mergelist
from brainpuzzler.settings import MEDIA_ROOT

box_size = (1120, 1120, 419)


def job_exists(number):
    return len(list(Job.objects.filter(chunk_number=number))) != 0


def read_kzip_file(kzip, name):
    kzip_path = MEDIA_ROOT + os.path.basename(kzip)
    try:
        with ZipFile(kzip_path, 'r') as kzip_file, kzip_file.open(name, 'r') as content:
            return str(content.read(), 'utf-8')
    except IOError:
        print("Could not open " + kzip)
        return False
    except BadZipfile:
        print(kzip + " seems to be corrupted!")
        return False


class Job(models.Model):
    chunk_number = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    job_file = models.FileField()

    def is_open(self):
        return len(self.submission.filter(state__in=[Submission.CREATED, Submission.ACCEPTED])) == 0

    def mergelist(self):
        mergelist = Mergelist()
        mergelist.read(read_kzip_file(self.job_file.name, "mergelist.txt"))
        return mergelist

    def annotation(self):
        return read_kzip_file(self.job_file.name, "annotation.xml")

    def __str__(self):
        return "job " + str(self.name) + ": " + str(self.description)


class Submission(models.Model):
    CREATED = 'CR'
    ACCEPTED = 'AC'
    REJECTED = 'RJ'
    JobStates = (
        (CREATED, 'created'),
        (ACCEPTED, 'accepted'),
        (REJECTED, 'rejected')
    )

    token = models.CharField(max_length=100)
    submit_file = models.FileField()
    job = models.ForeignKey('Job', related_name="submission")
    state = models.CharField(choices=JobStates, max_length=2, default=CREATED)
    rating = models.IntegerField(max_length=1, blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Submission " + str(self.token) + " of " + str(self.job.name) + ": " \
               + str(self.state) + ", rated " + str(self.rating)

    def mergelist(self):
        mergelist = Mergelist()
        mergelist.read(read_kzip_file(self.submit_file.name, "mergelist.txt"))
        return mergelist

    def annotation(self):
        return read_kzip_file(self.submit_file.name, "annotation.xml")


def get_random_open_job():
    try:
        return Job.objects.filter(submission=None)[0]
    except IndexError:
        for job in Job.objects.all().exclude(chunk_number=-1):
            if job.is_open():
                return job


def get_open_neighbor_job(chunk_number):
    overlaps = Chunk(chunk_number).get_overlapping_chunks()
    neighbors = Job.objects.filter(Q(chunk_number__in=overlaps))
    for neighbor in neighbors:
        if neighbor.is_open():
            return neighbor