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
        try:
            return Message.objects \
                .filter(Q(sender=self.host, receiver=self.peer) | Q(sender=self.peer, receiver=self.host)) \
                .filter(decompressed=True).order_by('-timestamp')[0]
        except:
            return None

    def __str__(self):
        return str(self.host) + ' ' + str(self.peer)


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

    def time(self):
        return self.timestamp.time()

    def save(self, *args, **kwargs):
        try:
            chat_1 = Chat.objects.get(host=self.sender, peer=self.receiver)
        except:
            chat_1 = Chat(host=self.sender, peer=self.receiver)
            chat_1.save()

        try:
            chat_2 = Chat.objects.get(host=self.receiver, peer=self.sender)
        except:
            chat_2 = Chat(host=self.receiver, peer=self.sender)
            chat_2.save()

        super(Message, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.sender) + ' -> ' + str(self.receiver) + ' at ' + str(self.timestamp)
