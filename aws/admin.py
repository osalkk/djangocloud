from django.contrib import admin
from aws.models import UserProfile,User
from aws.models import Awsaction
# Register your models here.


class AwsactionAdmin(admin.ModelAdmin):
    list_display = ('ins_id', 'selected_action', 'date')
    #pass

admin.site.register(Awsaction,AwsactionAdmin)
admin.site.register(UserProfile)


