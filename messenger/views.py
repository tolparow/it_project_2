from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
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


# def chat_view(request, peer_id):
#     user = request.user
#     if user.is_authenticated:
#         context = {
#             'host_user': request.user,
#             'chat': models.Chat.objects.get(host=user, peer=peer_id),
#         }
#
#         return TemplateResponse(request, 'www/messenger/chat.html', context)
#     return HttpResponseRedirect(reverse('login'))


# Only for testing
def chat_view(request):
    return TemplateResponse(request, 'www/messenger/chat.html')
