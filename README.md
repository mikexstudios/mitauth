mitauth
=======
http://github.com/mikexstudios/mitauth
by Michael Huynh (mike@mikexstudios.com)

Purpose:
-------

A very simple app that acts as a central authentication service (CAS) provider
for MIT SIPB's scripts.mit.edu service. As seen on page:

http://scripts.mit.edu/faq/15/can-i-authenticate-clients-using-mit-certificates

it is possible to use authenticate visitors on the *.scripts.mit.edu domain by
using MIT certificates. This app enables 3rd party applications to authenticate
MIT users.


How it works:
------------

1.  User clicks a login link on your website. The login link sends the user to:
        http://thisapp.scripts.mit.edu/login?service=http://yourapp/login-callback

2.  On that page, the user is redirected to the SSL version:
        https://thisapp.scripts.mit.edu:444/login?service=http://yourapp/login-callback
    and the user is prompted for his/her MIT SSL certificate.

3.  The app authenticates the user by looking for the 'SSL_CLIENT_S_DN_Email' 
    environment variable set by Apache webserver.

4.  The app then redirects the user back to your app's login callback along with
    a unique ticket string:
        http://yourapp/login-callback?ticket=ST-yHWJICjm7kT2DSahUYbXErPZcdelM
    (Note: If authentication was not successful, then no ticket is returned.)

5.  Your app then calls this app with the ticket to verify that the user was 
    indeed authenticated:
        http://thisapp.scripts.mit.edu/validate?ticket=ST-yHWJICjm7kT2DSahUYbXErPZcdelM&service=http://yourapp/login-callback
    The service returns:
        yes
        [username]
    If authentication was successful. If not, the service returns:
        no

All of this follows the standard CAS Protocol v1.0:
http://www.jasig.org/cas/protocol


Tested:
------

Django 1.4 (trunk)


TODO
====

- Implement cron command to clean up expired tickets.
