from django.db import models
from accounts.models import User


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_sender")
    message = models.TextField()
    chat = models.ForeignKey("Chat", on_delete=models.CASCADE, related_name="message_chat")
    date = models.DateTimeField()


class Chat(models.Model):
    createdDate = models.DateTimeField()
    lastMessage = models.DateTimeField()


class ChatUser(models.Model):
    chat = models.ForeignKey("Chat", on_delete=models.CASCADE, related_name="user_chat")
