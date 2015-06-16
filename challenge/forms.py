__author__ = 'tieni'

from django import forms

class ChallengeSubmissionForm(forms.Form):
    challenger_name = forms.CharField(max_length=100)
    mail_address = forms.EmailField(max_length=100)
    challenge_file = forms.FileField()
    challenge_file.help_text = "Upload a .k.zip file with segmentation data"
    challenge_file.label = "Submission file (*.k.zip)"

