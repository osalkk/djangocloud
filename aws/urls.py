from django.conf.urls import patterns, url
from aws import views

urlpatterns = patterns('',
                url(r'^$', views.dashboard, name='dashboard'),
                url(r'^dashboard/$', views.dashboard, name='dashboard'),
                url(r'^about',views.about,name='about'),
                url(r'^admin',views.admin,name='admin'),
                url(r'^deneme',views.deneme,name='deneme'),
                url(r'^region/(?P<region_name>[a-z0-9-]+)/$', views.region_detail, name='region'),
                url(r"^instance/(?P<region_name>[a-z0-9-]+)/(?P<instance_id>[\w\-]{10})/$", views.instance,name='instance' ),
                url(r'^register/$', views.register, name='register'),
                url(r'^login/$', views.user_login, name='login'),
                url(r'^logout/$', views.user_logout, name='logout'),
                url(r'^ins_action/$', views.ins_action, name='ins_action'),
                url(r'^vol/$', views.vol, name='vol'),
                url(r'^profile/$', views.profile, name='profile'),
                url(r'^delete/(?P<pk>\d+)', views.delete_task, name='deletePost'),
                url(r'^action/$', views.action, name='action'))
