from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
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


def chat_view(request, chat_id):
    user = request.user
    if user.is_authenticated:
        context = {
            'host_user': request.user,
            'chat': models.Chat.objects.get(pk=chat_id),
        }

        return TemplateResponse(request, 'www/messenger/chat.html', context)
    return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def ajax_changes_view(request):
    pass