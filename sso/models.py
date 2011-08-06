from django.db import models

from random import SystemRandom
import string #for letters and digits

class ServiceTicket(models.Model):
    username = models.CharField(max_length=8) #MIT's max username length is 8
    service = models.URLField(verify_exists=False)
    ticket = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s (%s) - %s" % (self.username, self.service, self.created)

    def generate_ticket(self):
        r = ''.join(SystemRandom().sample(string.ascii_letters + string.digits, 29))
        self.ticket = 'ST-%s' % r #total ticket length = 29 + 3 = 32
        self.save()
