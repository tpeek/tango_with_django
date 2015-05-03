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



def register(request, username_url=None):
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    oldUser = None
    oldPassword = None
    oldPicture = None

    users = UserProfile.objects.all() 
    for each_user in users:
        if each_user.getUsername() == username_url:
            oldUser = each_user
            oldPassword = oldUser.user.password
            oldPicture = oldUser.picture

    if request.method == 'POST':
        if oldUser:
            oldUser.user.username = 'a' + oldUser.user.username
            oldUser.user.save()
            
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)


        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            if oldUser:
                oldUser.user.delete()
                oldUser.delete()
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
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
              

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            elif oldUser:
                profile.picture = oldPicture
            

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors
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
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

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
                return HttpResponseRedirect('/rango/index/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('rango/login.html', {}, context)


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')


def decode_url(category_name_url):
    return category_name_url.replace('_', ' ')

#@login_required


def index(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    user_list = UserProfile.objects.all()
    #user_list = UserProfile.objects[:]
    context_dict = {'user_list': user_list,}# 'users': user_list}

    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
    #for category in category_list:

    # Render the response and send it back!
    return render_to_response('rango/index.html', context_dict, context)

def about(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('rango/about.html', context_dict, context)



def editUser(request, username_url):
    context = RequestContext(request)
    users = UserProfile.objects.all()

    for each_user in users:
        if each_user.getUsername() == username_url:
            user = each_user

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'user': user, 'username_url': username_url}

    # Go render the response and return it to the client.
    return render_to_response('rango/user.html', context_dict, context)


def deleteUser(request, username_url):
    context = RequestContext(request)
    userToDelete = UserProfile.objects.get(first_name=username_url)
    userToDelete.user.delete()
    userToDelete.delete()
    

    return render_to_response('rango/delete.html', {'username_url':username_url}, context)


    
        
