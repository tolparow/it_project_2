from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q


class Chat(models.Model):
    host = models.ForeignKey(get_user_model(), related_name='hosts')
    peer = models.ForeignKey(get_user_model(), related_name='peers')

    def messages(self):
        return Message.objects \
            .filter(Q(sender=self.host, receiver=self.peer) | Q(sender=self.peer, receiver=self.host)) \
            .filter(decompressed=True).order_by('timestamp')

    def last_message(self):
        pass


class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), related_name='senders')
    receiver = models.ForeignKey(get_user_model(), related_name='receivers')

    text = models.TextField(max_length=1025)

    file = models.FileField(null=True, blank=True, default=None)

    encryption_method = models.CharField(max_length=17)
    compression_method = models.CharField(max_length=17)

    loss_rate = models.FloatField()
    compression_rate = models.FloatField()

    timestamp = models.DateTimeField(auto_now=True)

    decompressed = models.BooleanField(default=False)
    new = models.BooleanField(default=True)
