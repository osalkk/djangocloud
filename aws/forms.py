__author__ = 'onur'
from django import forms
from aws.models import Awsaction,UserProfile,User
from django.contrib.admin.widgets import AdminDateWidget

class AwsForm(forms.ModelForm):
    action_list = (
                    ('Start','Start'),
                    ('Stop','Stop'),
                    ('Reboot','Reboot'),
                    ('Create AMI','Create AMI')
    )

    selected_action = forms.ChoiceField(choices=action_list,widget=forms.Select)
    date= forms.DateTimeInput()
    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Awsaction
        fields = ('date',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):

    #awskey=forms.CharField(max_length=128, label="Please enter the category name.",required=True)
    #awssecret=forms.CharField(max_length=128, label="secret",required=True)

    class Meta:
        model = UserProfile
        fields = ('awskey','awssecret',)