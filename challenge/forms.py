__author__ = 'tieni'

from django import forms
from django.utils.translation import ugettext as _

TASK_UPLOAD_FILE_TYPES = ['application/zip']
TASK_UPLOAD_FILE_MAX_SIZE = 5242880

class ChallengeSubmissionForm(forms.Form):
    challenger_name = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    mail_address = forms.EmailField(max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Your E-Mail'}))
    challenger_time = forms.DurationField(
        widget=forms.TextInput(attrs={'placeholder': 'DD HH:MM:SS'}))
    challenge_file = forms.FileField()
    challenge_file.help_text = "Upload a .k.zip file with segmentation data"
    challenge_file.label = "Submission file (*.k.zip)"

    def clean(self):
        file = self.cleaned_data['challenge_file']
        print("______")
        print(file)

        try:
            if file:
                file_type = file.content_type

                if len(file.name.split('.')) == 1:
                    raise forms.ValidationError(_('File type is not supported'))

                if file_type in TASK_UPLOAD_FILE_TYPES:
                    if file._size > TASK_UPLOAD_FILE_MAX_SIZE:
                        raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.TASK_UPLOAD_FILE_MAX_SIZE), filesizeformat(file._size)))
                else:
                    raise forms.ValidationError(_('File type is not supported'))
        except AttributeError:
            pass

        return file

