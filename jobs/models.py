from django.db import models
import os
from zipfile import ZipFile

from brainpuzzler.settings import MEDIA_ROOT


def read_kzip_file(kzip, name):
    kzip_path = MEDIA_ROOT + os.path.basename(kzip)
    try:
        with ZipFile(kzip_path, 'r') as kzip, kzip.open(name, 'r') as content:
            return str(content.read(), 'utf-8')
    except IOError:
        print("Could not open " + kzip)


class Job(models.Model):
    chunk_number = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    job_file = models.FileField()

    def mergelist(self):
        return read_kzip_file(self.job_file.name, "mergelist.txt")

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
        return "Job " + str(self.token) + " of " + str(self.job.name) + ": " \
               + str(self.state) + ", rated " + str(self.rating)

    def mergelist(self):
        return read_kzip_file(self.submit_file.name, "mergelist.txt")

    def annotation(self):
        return read_kzip_file(self.submit_file.name, "annotation.xml")