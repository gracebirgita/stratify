from django.shortcuts import render
# from chat.models import Thread
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Q

from .models import ChatMessage

from datetime import datetime
from django.utils import timezone

# def messages_page(request):
#     return render(request, 'messages.html')

User = get_user_model()

@login_required
def messages_page(request, room_name):
    search_query = request.GET.get('search', '')
    users = User.objects.exclude(id=request.user.id)
    chats = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver__username=room_name)) |
        (Q(receiver=request.user) & Q(sender__username=room_name))
    )

    if search_query:
        chats = chats.filter(Q(content__icontains=search_query))

    chats = chats.order_by('timestamp')
    user_last_messages = []

    for user in users:
        last_message = ChatMessage.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) |
            (Q(receiver=request.user) & Q(sender=user))
        ).order_by('-timestamp').first()

        user_last_messages.append({
            'user': user,
            'last_message': last_message
        })

    # Sort user_last_messages by the timestamp of the last_message in descending order
    user_last_messages.sort(
        key=lambda x: x['last_message'].timestamp if x['last_message'] else timezone.make_aware(datetime.min),
        reverse=True
    )
    
    # Get the User object for the current chat partner (room_name)
    try:
        chat_partner = User.objects.get(username=room_name)
    except User.DoesNotExist:
        chat_partner = None

    chat_partner_last_message = None
    if chat_partner:
        chat_partner_last_message = ChatMessage.objects.filter(
            (Q(sender=request.user) & Q(receiver=chat_partner)) |
            (Q(receiver=request.user) & Q(sender=chat_partner))
        ).order_by('-timestamp').first()
    
    #limit users shown to only 20
    user_last_messages = user_last_messages[:10] 

    return render(request, 'messaging.html', {
        'room_name': room_name,
        'chats': chats,
        'users': users,
        'user_last_messages': user_last_messages,
        'search_query': search_query,
        'chat_partner_last_message': chat_partner_last_message,
    })
    
# def messages_page(request, room_name):
#     # Ambil semua thread/user yang pernah chat dengan user ini
#     threads = Thread.objects.by_user(user=request.user)
#     user_last_messages = []
#     for thread in threads:
#         last_message = thread.chatmessage_thread.last()
#         other_user = thread.second_person if thread.first_person == request.user else thread.first_person
#         user_last_messages.append({
#             'user': other_user,
#             'last_message': last_message,
#         })

#     # Ambil semua pesan di room ini
#     chats = ChatMessage.objects.filter(thread__first_person__username=room_name) | \
#             ChatMessage.objects.filter(thread__second_person__username=room_name)

#     return render(request, 'chat/messages.html', {
#         'user_last_messages': user_last_messages,
#         'room_name': room_name,
#         'chats': chats,
#         'slug': room_name,
#         'search_query': request.GET.get('search', ''),
#     })

# Create your views here.

# User = get_user_model()

# # return messages page
# def messages_page(request):
#     print("Messages page is rendered")
#     threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
#     context = {
#         'Threads': threads
#     }
#     return render(request, 'messages.html', context)

# @login_required

#     query = request.GET.get('q', '')  # Ambil query dari parameter GET
#     if query:
#         users = User.objects.filter(
#             Q(username__icontains=query) | Q(email__icontains=query)
#         ).values('id', 'username', 'email')  # Ambil data user yang cocok
#         return JsonResponse(list(users), safe=False)
#     return JsonResponse([], safe=False)

# @login_required
# def get_messages(request):
#     user_id = request.GET.get('user_id')
#     if user_id:
#         # Find the thread between the logged-in user and the selected user
#         thread = Thread.objects.filter(
#             (Q(first_person=request.user) & Q(second_person_id=user_id)) |
#             (Q(first_person_id=user_id) & Q(second_person=request.user))
#         ).first()

#         if thread:
#             messages = thread.chatmessage_thread.all().order_by('timestamp').values(
#                 'message', 'timestamp', 'user_id'
#             )
#             return JsonResponse({'messages': list(messages)}, safe=False)

#     return JsonResponse({'messages': []}, safe=False)