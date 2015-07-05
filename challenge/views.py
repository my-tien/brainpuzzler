from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from brainpuzzler.settings import MEDIA_ROOT
from challenge.forms import ChallengeSubmissionForm

def index(request):
    if request.method == 'POST':
        form = ChallengeSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            handle_submission(request)
            return HttpResponseRedirect(reverse('challenge.views.index'))
    else:
        form = ChallengeSubmissionForm()
    return render_to_response('challenge/index.html',
                              {'action': reverse('challenge.views.index'),
                               'challenge_submissions': None,
                               'form': form},
                              context_instance=RequestContext(request))


def handle_submission(submission):
    submit_file = submission.FILES['challenge_file']
    curr_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    filename = "{0}_{1}_{2}".format(submission.POST['challenger_name'], curr_time, submit_file.name)
    with open(MEDIA_ROOT + 'knossos-challenge/submissions.txt', 'a') as submission_list:
        submission_list.write(submission.POST['challenger_name'] + '\t'
                              + submission.POST['mail_address'] + '\t'
                              + submission.POST['challenger_time'] + '\t'
                              + filename + '\n')

    with open(MEDIA_ROOT + 'knossos-challenge/' + filename, 'wb+') as new_submit:
        for chunk in submit_file.chunks():
            new_submit.write(chunk)
