import facebook
from django.conf import settings
from django.shortcuts import reverse
from urllib.parse import urlencode
from django.contrib.auth import login
from django.contrib import messages


app_id = settings.FACEBOOK_KEY
app_secret = settings.FACEBOOK_SECRET


def get_graph(access_token=""):
    """Get App Graph Object

    returns a graph object containing an app token from the registered facebook app
    """

    graph = facebook.GraphAPI(version='2.10')
    graph.access_token = access_token or graph.get_app_access_token(app_id, app_secret)
    return graph


# save graph object to scope
graph = get_graph()


def page_graph(page_token):
    """Page Graph

    return graph object from the page token
    """

    graph = facebook.GraphAPI(page_token)
    return graph


def canv_url(request):
    """Return Canvas URL

    Generates the canvas_url used by facebook to redirect after auth
    """

    # Check whether the last call was secure and use its protocol
    if request.is_secure():
        return 'https://' + request.get_host() + reverse('fb_login:facebook_login_response')
    else:
        return 'http://' + request.get_host() + reverse('fb_login:facebook_login_response')


def auth_url(request):
    """Auth URL

    Returns the facebook auth url using the current app's domain
    """

    canvas_url = canv_url(request)

    # Permissions set by user. Default is none
    perms = settings.FACEBOOK_PERMISSIONS

    url = "https://www.facebook.com/dialog/oauth?"

    # Payload
    kvps = {'client_id': app_id, 'redirect_uri': canvas_url}

    # Format permissions if needed
    if perms:
        kvps['scope'] = ",".join(perms)

    # Return the url
    return url + urlencode(kvps)


def debug_token(token):
    """Debug Token

    Returns debug string from token
    """

    return graph.debug_access_token(token, app_id, app_secret)


def login_successful(code, request):
    """Login Successful

    Process successful login by creating or updating an user using Facebook's response
    """

    canvas_url = canv_url(request)

    # Get token info from user
    token_info = graph.get_access_token_from_code(code, canvas_url, app_id, app_secret)

    # Extract token from token info
    access_token = token_info['access_token']

    # Token may never expire, so set its expire time to something big if needed
    try:
        token_expires = token_info['expires']
    except:
        token_expires = 9999999

    # Debug the token, as per documentation
    debug = debug_token(access_token)['data']

    # Get the user's scope ID from debug data
    social_id = debug['user_id']

    # Get some user info like name and url
    extra_data = graph.get_object(str(social_id) + '/?fields=name,first_name,link,permissions')
    name = extra_data['name']
    first_name = extra_data['first_name']
    link = extra_data['link']

    # THIS IS BAD, CREATE OBJECTS FOR PERMISSIONS TO ALLOW FASTER QUERIES
    scope = {}
    for perm in extra_data['permissions']['data']:
        scope[perm['permission']] = True

    scope = str(scope)

    # Call FacebookUser's method to create or update based on social_id, that returns an facebookuser object
    from .models import FacebookUser
    new = FacebookUser.create_or_update(social_id, access_token, token_expires, first_name, name, link, scope)

    # Try to login the user
    if new.user.is_active:
        login(request, new.user)
        messages.add_message(request, messages.SUCCESS, 'Olá, ' + first_name + '!')
    else:
        messages.add_message(request, messages.ERROR, 'Essa conta foi desativada!')

    return request


def login_canceled(request):

    # If the user has canceled the login process, or something else happened, do nothing and display error message
    messages.add_message(request, messages.ERROR, 'Oops! Algo de errado aconteceu!')

    return request
