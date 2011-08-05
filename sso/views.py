from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from cas_provider.forms import LoginForm
from cas_provider.utils import create_service_ticket

import re

#This overrides django-cas-provider's login routine
def login(request, template_name='cas/login.html', success_redirect='/accounts/'):
    
    #'service' GET var must be specified
    try:
        service = request.GET['service']

        #TODO: Try to auth user
        try:
            email = request.META['SSL_CLIENT_S_DN_Email']
            #Let's pull out the username part:
            r = re.match(r'(\w+)@mit.edu', email, re.IGNORECASE)
            #return HttpResponse(email)

            if email != 'scripts@mit.edu' and r:
                #Success!
                username = r.group(1)
                ticket = create_service_ticket(username, service)

                if service.find('?') == -1:
                    return redirect(service + '?ticket=' + ticket.ticket)
                return redirect(service + '&ticket=' + ticket.ticket)

        except KeyError:
            #If that key isn't found, then it means that we are not in SSL mode.
            #Redirect the user to port :444 (assuming this is 
            #http://username.scripts.mit.edu/)
            url = 'https://%s:%i%s' % (request.META['SERVER_NAME'], 444,
                                       request.get_full_path())
            return redirect(url)


    except KeyError:
        #TODO: Redirect to placeholder page explaining the service.
        #return redirect(success_redirect)
        return HttpResponse('service key must be defined!')
    
    return HttpResponse('error')
