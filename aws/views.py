from __future__ import unicode_literals
from django.shortcuts import render
from datetime import date
from aws.models import Awsaction,UserProfile,User
from aws.forms import AwsForm,UserForm, UserProfileForm, User
import aws.get_instances,aws.awsfunctions
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout




region = ""



@login_required
def index(request):
    current_user = request.user
    us_id=current_user.id
    key=UserProfile.objects.get(user_id=us_id).awskey
    secret=UserProfile.objects.get(user_id=us_id).awssecret
    a=aws.get_instances.connect(key,secret)
    if a=="AWS was not able to validate the provided access credentials":
        context_dict = {'hata':a}
        return render(request, 'aws/index1.html', context_dict)
    elif not key or not secret:
        context_dict = {'hata': "Please check your aws key and secret in your Account"}
        return render(request, 'aws/profile.html', context_dict)
    elif type(a)==list:
        context_dict = {'instances': a}
        return render(request, 'aws/index1.html', context_dict)


@login_required
def dashboard(request):
    current_user = request.user
    us_id=current_user.id
    key=UserProfile.objects.get(user_id=us_id).awskey
    secret=UserProfile.objects.get(user_id=us_id).awssecret
    if key:
        a=aws.get_instances.connect_all(key,secret)
    else:
        context_dict = {'hata': "Please check your aws key and secret in your Account"}
        return render(request, 'aws/profile.html', context_dict)
    if a=="AWS was not able to validate the provided access credentials":

        context_dict = {'hata':a}

        return render(request, 'aws/index1.html', context_dict)
    elif not key or not secret:
        context_dict = {'hata': "Please check your aws key and secret in your Account"}
        return render(request, 'aws/profile.html', context_dict)
    elif type(a)==list:
        context_dict = {'instances': a}
        return render(request, 'aws/dashboard.html', context_dict)

@login_required
def region_detail(request, region_name):
    global region
    region= region_name
    current_user = request.user
    us_id=current_user.id
    key=UserProfile.objects.get(user_id=us_id).awskey
    secret=UserProfile.objects.get(user_id=us_id).awssecret
    a=aws.get_instances.connect(key,secret,region_name)
    if a=="AWS was not able to validate the provided access credentials":
        context_dict = {'hata':a}
        return render(request, 'aws/index1.html', context_dict)
    elif not key or not secret:
        context_dict = {'hata': "Please check your aws key and secret in your Account"}
        return render(request, 'aws/profile.html', context_dict)
    elif type(a)==list:
        context_dict = {'instances': a,'region':region}
        #logger.info(region)
        return render(request, 'aws/index1.html', context_dict)
    else:
        context_dict = {'instances': a,'region':region}
        return render(request, 'aws/index1.html', context_dict)

@login_required
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST)
        if profile_form.is_valid():
            awskey=request.POST.get('awskey')
            awssecret=request.POST.get('awssecret')
            us_id=request.POST.get('userid')
            b=UserProfile.objects.get(user_id=us_id)
            if 'awskey' and 'awssecret' in request.POST:
                profile.awskey = awskey
                profile.awssecret = awssecret
            a=UserProfile.objects.filter(user_id=us_id).update(awskey=awskey,awssecret=awssecret)
            return HttpResponseRedirect('/aws/')
        else:
            print(profile_form.errors)
    else:
        us_id=request.user
        a=UserProfile.objects.get(user_id=us_id).awskey
        b=UserProfile.objects.get(user_id=us_id).awssecret
        context_dict = {'awskey' : a,'awssecret' : b,}
        form = UserProfileForm()
        return render(request, 'aws/profile.html',context_dict)
    return render(request, 'aws/profile.html')

def about(request):
    context_dict = {
        'boldmessage': "I am bold font from the context",
        'today' : date.today()
    }
    return render(request, 'aws/about.html',context_dict)

def admin(request):
    context_dict = {
        'boldmessage': "I am bold font from the context",
        'today' : date.today()
    }
    #return HttpResponse("Rango says here is about page <a href='/rango/'>Index</a>")
    return render(request, 'aws/admin.html',context_dict)

def contact(request):
    return HttpResponse("<a href='/aws/'>Index</a>")

def deneme(request):
    context_dict = {
        'boldmessage': "I am bold font from the context",
        'today' : date.today()
    }
    return render(request, 'aws/deneme.html',context_dict)

@login_required
def instance(request,instance_id,region_name):
    ins_region=region_name
    if request.method == 'POST':
        form = AwsForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    if request.method == 'GET':
        current_user = request.user
        us_id=current_user.id
        key=UserProfile.objects.get(user_id=us_id).awskey
        secret=UserProfile.objects.get(user_id=us_id).awssecret
        b=aws.get_instances.connect1(instance_id,key,secret,ins_region)
        c= Awsaction.objects.filter(ins_id=instance_id)
        asd=""
        for value in c.values():
            asd=(value['days'])
        context_dict = {'instances' : b,'ins_actions' : c,'region_name':ins_region,'days':asd}
        form = AwsForm()
    return render(request, 'aws/ins_detail.html', {'instance_id':instance_id,'form': form, 'instances':context_dict['instances'],'ins_actions':context_dict['ins_actions'],'region_name':context_dict['region_name'],'days':context_dict['days'],})

@login_required
def action(request):
    if request.method == 'POST':
        hede={}
        hede=dict(request.POST)
        onur=""
        for key in hede:
            if 'on' in hede[key]:
                print(key)
                if key!='recurring':
                    onur=onur+','+key
        onur=onur[1:]
        form = AwsForm(request.POST)
        if form.is_valid():
            us_id=request.POST.get('userid')
            date=request.POST.get('date')
            instance_id=request.POST.get('instance_id')
            selected_action=request.POST.get('selected_action')
            recur = request.POST.get('recurring')
            week = request.POST.get('week')
            if recur:
                recur_enabled=True
            else:
                recur_enabled=False
            awsaction = Awsaction(date=date,user_id=us_id,
                    ins_id=instance_id,
                    selected_action=selected_action,days=onur,recurring=recur_enabled,weeks=week)
            awsaction.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        logger.info("get yapildi")
        form = AwsForm()
        return render(request, 'aws/ins_detail.html', {'instance_id':instance_id,'form': form})
    return render(request, 'aws/ins_detail.html', {'instance_id':instance_id,'form': form})

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            current_user = profile.user
            us_id=current_user.id
            a=UserProfile.objects.filter(user_id=us_id).update(awskey='demo',awssecret='demo')
            registered = True
            return HttpResponseRedirect('/aws/')
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,'aws/register1.html',{'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )
def user_login(request):
    err_msg = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/aws/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            err_msg= 'Please check your username or password.'
            return render(request, 'aws/login1.html', {'login': err_msg})
    else:
        return render(request, 'aws/login1.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/aws/login')

@login_required
def delete_task(request,pk):
    query = Awsaction.objects.get(pk=pk)
    query.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def ins_action(request):
    current_user = request.user
    us_id=current_user.id
    key=UserProfile.objects.get(user_id=us_id).awskey
    secret=UserProfile.objects.get(user_id=us_id).awssecret
    if request.method == 'POST':
        ins_region= request.POST['region_name']
        ins_id = request.POST['ins_id']
        ins_act = request.POST['ins_action']
        token = request.POST['csrfmiddlewaretoken']
        a=aws.awsfunctions.power(key,secret,ins_id,ins_act,ins_region)
        if "You are not authorized to perform this operation." in a:
            a="You are not authorized to perform this operation"
            return HttpResponse(a)
        elif "can not be" in a:
            return HttpResponse(a)
        else:
            return HttpResponse(a)
    else:
        print("get")

@login_required
def vol(request):
    current_user = request.user
    us_id=current_user.id
    key=UserProfile.objects.get(user_id=us_id).awskey
    secret=UserProfile.objects.get(user_id=us_id).awssecret
    if request.method == 'POST':
        ins_region= request.POST['region_name']
        ins_id = request.POST['ins_id']
        volume = request.POST['volume_name']
        token = request.POST['csrfmiddlewaretoken']
        a=aws.get_instances.vol(key,secret,ins_id,ins_region,volume)
        if "You are not authorized to perform this operation." in a:
            a="You are not authorized to perform this operation"
            return HttpResponse(a)
            #return render(request, 'aws/ins_detail.html', context_dict)
            #return HttpResponse('/aws/instance/%s' % ins_id,context_dict)
        elif "can not be" in a:
            return HttpResponse(a)
        else:
            context_dict = {'snap_list': a}
            return HttpResponse(a)
    else:
        print("get")
