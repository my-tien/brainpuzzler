from django.contrib import admin
from jobs.models import *


class JobAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'job_file')


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('token', 'job', 'submit_file', 'state', 'rating', 'upload_date')

admin.site.register(Job, JobAdmin)
admin.site.register(Submission, SubmissionAdmin)
