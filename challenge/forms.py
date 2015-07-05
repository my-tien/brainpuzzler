__author__ = 'tieni'

from django import forms

class ChallengeSubmissionForm(forms.Form):
    challenger_name = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    mail_address = forms.EmailField(max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Your E-Mail'}))
    challenger_time = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Computation time (hh:mm:ss)'}))
    challenge_file = forms.FileField()
    challenge_file.help_text = "Upload a .k.zip file with segmentation data"
    challenge_file.label = "Submission file (*.k.zip)"