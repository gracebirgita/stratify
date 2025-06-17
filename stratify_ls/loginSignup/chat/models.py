from django.db import models
from django.conf import settings
# Create your models here.
# from django.db import models
# from django.contrib.auth.models import User

# from django.contrib.auth import get_user_model
# from django.db.models import Q
# from django.shortcuts import render


from django.contrib.auth.models import User

class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE, null=True, blank=True)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="received_messages", on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:20]}"

# User = get_user_model()

# # Create your models here.

# class ThreadManager(models.Manager):
#     def by_user(self, **kwargs):
#         user = kwargs.get('user')
#         lookup = Q(first_person=user) | Q(second_person=user)
#         qs = self.get_queryset().filter(lookup).distinct()
#         return qs
    
#     def create_thread(self, first_person, second_person):
#         if first_person == second_person:
#             raise ValueError("Users in a thread must be different.")
#         thread, created = self.get_or_create(first_person=first_person, second_person=second_person)
#         return thread


# class Thread(models.Model):
#     # first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
#     # second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
#     #                                  related_name='thread_second_person')
#     first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, 
#                                      related_name='thread_first_person')
#     second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
#                                      related_name='thread_second_person')


#     updated = models.DateTimeField(auto_now=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     objects = ThreadManager()
#     class Meta:
#         unique_together = ['first_person', 'second_person']


# class ChatMessage(models.Model):
#     # thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
#     thread = models.ForeignKey(Thread, null=True, on_delete=models.CASCADE, related_name='chatmessage_thread')

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

# def chat_view(request):
#     threads = Thread.objects.filter(Q(first_person=request.user) | Q(second_person=request.user))
#     print(threads)  # Debugging
#     return render(request, 'chat/templates/messages.html', {'Threads': threads})