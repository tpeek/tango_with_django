from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import UserProfile
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django import forms
from django.contrib.auth.models import User



# Make a new user or edit an existing one.
def register(request, username_url=None):
    context = RequestContext(request)

    # Tells register.html if registration has succeeded or not.
    registered = False

    # These keep track of user information in the case of an edit.
    oldUser = None
    oldPassword = None
    oldPicture = None

    # Find the user that is currently being edited.
    if username_url != None:
        users = UserProfile.objects.all() 
        for each_user in users:
            if each_user.getUsername() == username_url:
                oldUser = each_user
                oldPassword = oldUser.user.password
                oldPicture = oldUser.picture

    # If the user has submitted the form, process it.
    if request.method == 'POST':
        if oldUser:
            # Change the username of the old user so that vaidation works.
            oldUser.user.username = 'a' + oldUser.user.username
            oldUser.user.save()
            
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)


        # If the two forms are valid,
        if user_form.is_valid() and profile_form.is_valid():
            if oldUser:
                oldUser.user.delete()
                oldUser.delete()
            # then save the user's form data.
            user = user_form.save()

            # Password is hashed.
            if oldUser: # If this is an update to an existing user,
                if user.password != '*******': # and the password is updated, 
                    user.set_password(user.password)# change it.
                    user.save()
                elif user.password == '*******':# Otherwise,
                    user.password = oldPassword# set is as the old password.
                    user.save()
            else:
                user.set_password(user.password)
                user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            elif oldUser:
                profile.picture = oldPicture
            
            profile.save()

            # Registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors
            # Change the username back.
            if oldUser:
                oldUser.user.username = oldUser.user.username[1:]
                oldUser.user.save()

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        if oldUser:
            user_form = UserForm({'username':oldUser.user.username, 'email':oldUser.user.email, 'password':'*******'})
            profile_form = UserProfileForm({'first_name':oldUser.first_name, 'last_name':oldUser.last_name, 'website':oldUser.website, 'picture':oldUser.picture, })
        else:
            user_form = UserForm()
            profile_form = UserProfileForm()


    # Render the template depending on the context.
    return render_to_response(
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'username_url': username_url},
            context)


def user_login(request):
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                login(request, user)
                return HttpResponseRedirect('/rango/index/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    else:
        return render_to_response('rango/login.html', {}, context)


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    logout(request)

    # Take the client back to the homepage.
    return HttpResponseRedirect('/rango/')


# List all the users with links to their detail page.
def index(request):
    context = RequestContext(request)

    user_list = UserProfile.objects.all()
    context_dict = {'user_list': user_list}

    return render_to_response('rango/index.html', context_dict, context)


# Send client to about.html.
def about(request):
    context = RequestContext(request)

    return render_to_response('rango/about.html', context)


# Allows someone who is logged in to edit each user attribute.
@login_required
def editUser(request, username_url):
    context = RequestContext(request)
    users = UserProfile.objects.all()

    for each_user in users:
        if each_user.getUsername() == username_url:
            user = each_user

    context_dict = {'user': user, 'username_url': username_url}

    # Go render the response and return it to the client.
    return render_to_response('rango/user.html', context_dict, context)


# Allows someone who is logged in to delete a user.
@login_required
def deleteUser(request, username_url):
    context = RequestContext(request)
    userToDelete = UserProfile.objects.get(first_name=username_url)
    userToDelete.user.delete()
    userToDelete.delete()

    return render_to_response('rango/delete.html', {'username_url':username_url}, context)


# Send client to todo.html.
def todo(request):
    return render_to_response('rango/todo.html')
        
