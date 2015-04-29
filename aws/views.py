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




import logging
import logging.handlers

logger = logging.getLogger()
fh = logging.FileHandler('/var/tmp/django.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.INFO)

region = ""



@login_required
def index(request):
    current_user = request.user
    us_id=current_user.id
    key=UserProfile.objects.get(id=us_id).awskey
    secret=UserProfile.objects.get(id=us_id).awssecret
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
    key=UserProfile.objects.get(id=us_id).awskey
    secret=UserProfile.objects.get(id=us_id).awssecret

    a=aws.get_instances.connect_all(key,secret)



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
    global logger
    global region
    region= region_name

    current_user = request.user
    us_id=current_user.id
    key=UserProfile.objects.get(id=us_id).awskey
    secret=UserProfile.objects.get(id=us_id).awssecret
    a=aws.get_instances.connect(key,secret,region_name)
    #logger.info(region_name)


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
        #logger.info(region)
        return render(request, 'aws/index1.html', context_dict)




@login_required
def profile(request):

    current_user = request.user
    if request.method == 'POST':
        print("profile post edildi")
        profile_form = UserProfileForm(data=request.POST)

        if profile_form.is_valid():

            awskey=request.POST.get('awskey')
            awssecret=request.POST.get('awssecret')
            us_id=request.POST.get('userid')

            b=UserProfile.objects.get(user_id=us_id)




            if 'awskey' and 'awssecret' in request.POST:
                #print(awskey,awssecret)
                profile.awskey = awskey
                profile.awssecret = awssecret

            # Now we save the UserProfile model instance.
            a=UserProfile.objects.filter(user_id=us_id).update(awskey=awskey,awssecret=awssecret)
            #print(awskey,awssecret)


            return HttpResponseRedirect('/aws/')
            #return render(request, 'aws/dashboard.html')
        else:
            #print("not valid")
            print(profile_form.errors)
    else:
        #print("get")
        us_id=current_user.id
        a=UserProfile.objects.get(id=us_id).awskey
        b=UserProfile.objects.get(id=us_id).awssecret
        #print(a,b,current_user,current_user.id)

        context_dict = {'awskey' : a,'awssecret' : b,}


        form = UserProfileForm()
        return render(request, 'aws/profile.html',context_dict)



    return render(request, 'aws/profile.html')

def about(request):
    context_dict = {
        'boldmessage': "I am bold font from the context",
        'today' : date.today()
    }
    #return HttpResponse("Rango says here is about page <a href='/rango/'>Index</a>")
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
    #global logger
    ins_region=region_name
    logger.info(region_name)
    if request.method == 'POST':

        form = AwsForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    if request.method == 'GET':
        #ua = request.META['HTTP_REFERER']
        #logger.info(ua)
        current_user = request.user
        us_id=current_user.id
        key=UserProfile.objects.get(id=us_id).awskey
        secret=UserProfile.objects.get(id=us_id).awssecret

        b=aws.get_instances.connect1(instance_id,key,secret,ins_region)
        c= Awsaction.objects.filter(ins_id=instance_id)
        #print(c.values())
        asd=""
        for value in c.values():
            asd=(value['days'])
            print(asd)






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
            #print(us_id,date,instance_id,selected_action,recur_enabled,week)
            awsaction = Awsaction(date=date,user_id=us_id,
                    ins_id=instance_id,
                    selected_action=selected_action,days=onur,recurring=recur_enabled,weeks=week)
            awsaction.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            #return HttpResponseRedirect('/aws/instance/%s' % instance_id)
        else:
            # The supplied form contained errors - just print them to the terminal.
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            #print(form.errors)
    else:
        logger.info("get yapildi")
        # If the request was not a POST, display the form to enter details.
        form = AwsForm()
        return render(request, 'aws/ins_detail.html', {'instance_id':instance_id,'form': form})

    return render(request, 'aws/ins_detail.html', {'instance_id':instance_id,'form': form})
    #return HttpResponse(instance_id)

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True
            return HttpResponseRedirect('/aws/')

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'aws/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):
    err_msg = None
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')


        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/aws/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            #print("Invalid login details: {0}, {1}".format(username, password))
            err_msg= 'Please check your username or password.'
            return render(request, 'aws/login.html', {'login': err_msg})
            #return HttpResponseRedirect("/aws/")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'aws/login.html', {})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/aws/login')

@login_required
def delete_task(request,pk):
    query = Awsaction.objects.get(pk=pk)

    #instance_id=query.object.filter(pk.ins_id)
    #print(instance_id)
    query.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #return HttpResponseRedirect('/aws/instance/%s' % query)


@login_required
def ins_action(request):

    current_user = request.user
    us_id=current_user.id
    key=UserProfile.objects.get(id=us_id).awskey
    secret=UserProfile.objects.get(id=us_id).awssecret

    if request.method == 'POST':

        logger.info(request)
        ins_region= request.POST['region_name']
        ins_id = request.POST['ins_id']
        ins_act = request.POST['ins_action']
        token = request.POST['csrfmiddlewaretoken']
        logger.info(region,ins_id,ins_act)
        #print(ins_act)
        a=aws.awsfunctions.power(key,secret,ins_id,ins_act,ins_region)

        if "You are not authorized to perform this operation." in a:
            a="You are not authorized to perform this operation"
            return HttpResponse(a)
            #return render(request, 'aws/ins_detail.html', context_dict)
            #return HttpResponse('/aws/instance/%s' % ins_id,context_dict)
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
    key=UserProfile.objects.get(id=us_id).awskey
    secret=UserProfile.objects.get(id=us_id).awssecret

    if request.method == 'POST':

        logger.info(request)
        ins_region= request.POST['region_name']
        ins_id = request.POST['ins_id']

        volume = request.POST['volume_name']
        token = request.POST['csrfmiddlewaretoken']


        a=aws.get_instances.vol(key,secret,ins_id,ins_region,volume)
        print(a)

        if "You are not authorized to perform this operation." in a:
            a="You are not authorized to perform this operation"
            return HttpResponse(a)
            #return render(request, 'aws/ins_detail.html', context_dict)
            #return HttpResponse('/aws/instance/%s' % ins_id,context_dict)
        elif "can not be" in a:
            return HttpResponse(a)
        else:
            context_dict = {'snap_list': a}
            #context_dict = {'instances' : b,'ins_actions' : c,'region_name':ins_region,'days':asd}
            return HttpResponse(a)
            #return render(request, 'aws/ins_detail.html', context_dict)



    else:
        print("get")

    #return HttpResponse(ins_id,ins_action)
