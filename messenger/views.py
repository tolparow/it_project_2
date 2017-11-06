from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
import messenger.models as models
from django.urls import reverse


def messages_view(request):
    user = request.user
    if user.is_authenticated:
        context = {
            'host_user': request.user,
            'chats': models.Chat.objects.filter(host=user),
        }

        return TemplateResponse(request, 'www/messenger/main.html', context)
    return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def chat_view(request: WSGIRequest, chat_id):
    user = request.user
    chat = models.Chat.objects.get(pk=chat_id)

    if chat.host != user:
        return HttpResponseForbidden()

    if user.is_authenticated:

        context = {
            'host_user': request.user,
            'chat': chat,
        }

        if request.is_ajax():
            msg_text = request.POST.get('message')
            if msg_text is None:
                return TemplateResponse(request, 'www/blocks/chat-messages.html', context)

            msg = models.Message(
                sender=user,
                receiver=chat.peer,
                text=msg_text,
                encryption_method='no',
                compression_method='no',
                loss_rate=0,
                compression_rate=0,
                decompressed=True,
            )
            msg.save()
            return HttpResponse('ok')

        return TemplateResponse(request, 'www/messenger/chat.html', context)
    return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def ajax_changes_view(request):
    pass
