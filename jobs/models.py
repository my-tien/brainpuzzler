from django.db import models


class Job(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    job_file = models.FileField()

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
    job = models.ForeignKey('Job')
    state = models.CharField(choices=JobStates, max_length=2, default=CREATED)
    rating = models.IntegerField(max_length=1, blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Job " + str(self.token) + " of " + str(self.job.name) + ": " \
               + str(self.state) + ", rated " + str(self.rating)