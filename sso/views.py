from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from cas_provider.forms import LoginForm
from cas_provider.utils import create_service_ticket

import re

#This overrides django-cas-provider's login routine
def login(request, template_name='cas/login.html', success_redirect='/accounts/'):
    
    service = request.GET.get('service', False)
    if not service:
        #TODO: Redirect to placeholder page explaining the service.
        #return redirect(success_redirect)
        return HttpResponse("ERROR: 'service' key must be defined!")

    #First, check that we are using SSL. If not, then redirect to SSL page
    if not request.META.get('SSL_SESSION_ID', False):
        #Redirect the user to port :444 (assuming this is 
        #http://username.scripts.mit.edu/)
        url = 'https://%s:%i%s' % (request.META['SERVER_NAME'], 444,
                                   request.get_full_path())
        return redirect(url)

    #Auth user using personal certificates using method described on page:
    #http://scripts.mit.edu/faq/15/can-i-authenticate-clients-using-mit-certificates
    email = request.META.get('SSL_CLIENT_S_DN_Email', False)
    if not email:
        return HttpResponse('ERROR: SSL certificate email not found!')

    #Pull out the username part. If the user SSL certificate was not supplied, 
    #then it gives a generic email like scripts@mit.edu. So we specifically
    #check for that.
    r = re.match(r'(\w+)@mit.edu', email, re.IGNORECASE)
    if email != 'scripts@mit.edu' and r:
        #Success! Now create a service ticket and redirect back to calling app.
        username = r.group(1)
        ticket = create_service_ticket(username, service)

        new_or_append = '&' #default is append to query string
        if service.find('?') == -1:
            new_or_append = '?'

        return redirect(service + new_or_append + 'ticket=' + ticket.ticket)

    #Catch-all error
    return HttpResponse('ERROR')
