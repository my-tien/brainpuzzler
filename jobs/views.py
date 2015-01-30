from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

import hashlib
from io import BytesIO
import zipfile

from jobs.models import *
import brainpuzzler.settings as settings

employer_key = '278b1668328e26d793352b3bd40ff35ae9996289d39c444dccdb45b7527f7698'

@csrf_exempt
def job(request, job_id, campaign_id, worker_id):
    """
    download a job in form of a .k.zip
    :param request: the http request
    :param job_id: the job's id specified in the url
    :return: http response or 404 if job with job_id does not exist
    """
    if request.method == 'GET':
        try:
            submit_path = "http://localhost:8000/jobs/job_1/camp_2/mw_3/"
            requested_job = Job.objects.get(pk=job_id)
            job_archive = requested_job.job_file.name.split('/')[-1][:-6]
            job_for_download = "{0}_{1}_{2}.k.zip".format(job_archive, campaign_id, worker_id)
            id_card = '{0}\n{1}\n{2}\n{3}'.format(job_id, submit_path, campaign_id, worker_id)

            job_content = BytesIO()
            with zipfile.ZipFile(job_content, 'w') as download_archive, \
                    zipfile.ZipFile(settings.MEDIA_ROOT + requested_job.job_file.name) as job_orig:
                # add microjob tag containing job id, submit path, campaign id and microworker id
                annotation = job_orig.read("annotation.xml")
                download_archive.writestr("annotation.xml", annotation)
                download_archive.writestr("microjob.txt", id_card)

            response = HttpResponse(job_content.getvalue(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=%s' % job_for_download
            return response
        except Job.DoesNotExist:
            return HttpResponse("Could not find job with ID %i" % job_id, status=404)

    elif request.method == 'POST':
        try:
            finished_job = Job.objects.get(pk=job_id)
            vcode = 'mw-' + hashlib.sha256("{0}{1}{2}".format(campaign_id, worker_id, employer_key)
                                           .encode('utf-8')).hexdigest()

            submit_file = request.FILES.get("submit", False)
            if not submit_file:
                return HttpResponse("No file uploaded.", status=400)
            submission = Submission(token=vcode, job=finished_job, submit_file=submit_file)
            submission.save()
            return HttpResponse(vcode)
        except ValueError:
            return HttpResponse("The request was not parsed successfully: %s" % request.body, status=400)
        except Job.DoesNotExist:
            return HttpResponse("Could not find job with ID %i" % job_id, status=404)




