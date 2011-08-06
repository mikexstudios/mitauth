from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from mitauth.models import ServiceTicket

import re

def login(request):
    service = request.GET.get('service', False)
    if not service:
        #TODO: Redirect to placeholder page explaining the service.
        #return redirect(success_redirect)
        return HttpResponse("ERROR: 'service' key must be defined!")

    #First, check that we are using SSL on the specific port 444. If not, then
    #redirect to port 444:
    #if not request.META.get('SSL_SESSION_ID', False):
    if int(request.META['SERVER_PORT']) != 444:
        #Redirect the user to port :444 (assuming this is 
        #http://username.scripts.mit.edu/)
        url = 'https://%s:%i%s' % (request.META['SERVER_NAME'], 444,
                                   request.get_full_path())
        return redirect(url)

    #Auth user using personal certificates using method described on page:
    #http://scripts.mit.edu/faq/15/can-i-authenticate-clients-using-mit-certificates
    email = request.META.get('SSL_CLIENT_S_DN_Email', False)
    if not email:
        #TODO: Show error page that redirects back to original url but without
        #      ticket parameter.
        return HttpResponse('ERROR: SSL certificate email not found!')

    #Pull out the username part. If the user SSL certificate was not supplied, 
    #then it gives a generic email like scripts@mit.edu. So we specifically
    #check for that.
    r = re.match(r'(\w+)@mit.edu', email, re.IGNORECASE)
    if email != 'scripts@mit.edu' and r:
        #Success! Now create a service ticket and redirect back to calling app.
        username = r.group(1)

        st = ServiceTicket(username = username, service = service)
        st.generate_ticket()
        st.save()

        new_or_append = '&' #default is append to query string
        if service.find('?') == -1:
            new_or_append = '?'

        return redirect(service + new_or_append + 'ticket=' + st.ticket)

    #Catch-all error
    return HttpResponse('ERROR')


def validate(request):
    service = request.GET.get('service', False) #required by spec
    ticket = request.GET.get('ticket', False)
    if service and ticket_string:
        try:
            ticket = ServiceTicket.objects.get(ticket = ticket)
            #TODO: Verify that provided service matches the service entered
            #in the ticket.
            username = ticket.username
            ticket.delete()
            return HttpResponse("yes\n%s\n" % username)
        except ServiceTicket.DoesNotExist:
            pass
    return HttpResponse("no\n\n")

