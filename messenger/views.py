from django.contrib.auth import get_user_model
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
import messenger.models as models
from django.urls import reverse


@csrf_exempt
def chats_view(request):
    user = request.user

    if user.is_authenticated:
        context = {
            'host_user': request.user,
            'chats': models.Chat.objects.filter(host=user),
            'users': get_user_model().objects.all(),
        }

        return TemplateResponse(request, 'www/messenger/main.html', context)
    return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def chat_view(request: WSGIRequest, peer_id):
    user = request.user

    try:
        peer = get_user_model().objects.get(pk=peer_id)
    except get_user_model().DoesNotExist:
        return HttpResponseForbidden()

    try:
        chat = models.Chat.objects.get(host=user, peer=peer)
    except models.Chat.DoesNotExist:
        chat = models.Chat(host=user, peer=peer)
        chat.save()

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
