from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import hashlib
import os
import shutil
import tempfile

from jobs.models import *
import brainpuzzler.settings as settings

employer_key = '278b1668328e26d793352b3bd40ff35ae9996289d39c444dccdb45b7527f7698'


def index(request):
    context = {'greeting': 'Hello World!'}
    return render(request, 'jobs/index.html', context)


@csrf_exempt
def job(request, job_id, campaign_id, worker_id):
    """
    download a job in form of a .k.zip
    :param request: the http request
    :param job_id: the job's id specified in the url
    :return: http response or 404 if job with job_id does not exist
    """
    if request.method == 'GET':
        try:  # we need to edit the microjob.txt to containg the microworker's id and the campaign id
            # first, copy the job to temporary location
            job_basename = os.path.basename(Job.objects.get(pk=job_id).job_file.name)
            job_file = settings.MEDIA_ROOT + job_basename
            tmp_dir = tempfile.mkdtemp() + "/"  # mkdtemp does not include the trailing slash ...
            tmp_job = tmp_dir + job_basename
            shutil.copyfile(job_file, tmp_job)
            with open(tmp_dir + "microjob.txt", 'w') as microjob_file:  # add personal microjob.txt
                microjob_file.write('2\nhttp://brainpuzzler.org/jobs/job_{0}/camp_{1}/mw_{2}/'
                                    .format(job_id, campaign_id, worker_id))
            os.system("zip -j {0} {1}microjob.txt".format(tmp_job, tmp_dir))
            # read the new zip into memory to remove the temporary file
            with open(tmp_job, 'rb') as tmp_job_file:
                tmp_job_stream = tmp_job_file.read()
            shutil.rmtree(tmp_dir)
            response = HttpResponse(tmp_job_stream, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename={0}'.format(job_basename)
            return response
        except Job.DoesNotExist:
            return error_response(404, "Could not find job with ID {0}".format(job_id))

    elif request.method == 'POST':
        try:
            finished_job = Job.objects.get(pk=job_id)
            vcode = 'mw-' + hashlib.sha256("{0}{1}{2}".format(campaign_id, worker_id, employer_key)
                                           .encode('utf-8')).hexdigest()

            submit_file = request.FILES.get("submit", False)
            if not submit_file:
                return error_response(400, "No file uploaded.")
            submission = Submission(token=vcode, job=finished_job, submit_file=submit_file)
            submission.save()
            return HttpResponse("verification code: {0}".format(vcode))
        except ValueError:
            return error_response(400, "The request was not parsed successfully: {0)".format(request.body))
        except Job.DoesNotExist:
            return error_response(404, "Could not find job with ID {0}".format(job_id))


@csrf_exempt
def job_submit(request, job_id):
    if request.method == 'POST':
        try:
            finished_job = Job.objects.get(pk=job_id)
            submit_file = request.FILES.get("submit", False)
            if not submit_file:
                return error_response(400, "no file uploaded.")
            submission = Submission(token="none", job=finished_job, submit_file=submit_file)
            submission.save()
            return HttpResponse("Your job was successfully submitted.")
        except ValueError:
            return error_response(400, "The request was not parsed successfully: {0)".format(request.body))
        except Job.DoesNotExist:
            return error_response(404, "Could not find job with ID {0}".format(job_id))


def error_response(http_code, message):
    response = HttpResponse(status=http_code)
    response['error'] = message
    return response
