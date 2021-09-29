from re import T
from django.db import models


# Create your models here.


class Message(models.Model):
  username = models.CharField(max_length=255)
  room = models.CharField(max_length=255)
  content = models.TextField()
  date_added = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ('date_added',)



class User(models.Model):
  username = models.CharField(max_length=255)
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)

  is_delete = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
  
  def __str__(self):
        return str(self.username) + '  ' + str(self.id)


class Room(models.Model):
  user = models.ForeignKey(User, related_name="room_user", on_delete=models.CASCADE)
  room_name = models.CharField(max_length=255, null=True, blank=True)

  is_delete = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

  def __str__(self):
    return str(self.room_name) + '  ' + str(self.id)


class Participants(models.Model):
  room = models.ForeignKey(Room, related_name="participants_room", on_delete=models.CASCADE)
  users = models.ManyToManyField(User, related_name="participants_user", blank=True)

  is_delete = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

  def __str__(self):
    return str(self.room) + '  ' + str(self.id)


class Messages(models.Model):
  room = models.ForeignKey(Room, related_name="message_room", on_delete=models.CASCADE)
  user = models.ForeignKey(User, related_name="messages_user", on_delete=models.CASCADE)
  message = models.TextField(null=True, blank=True)
  file = models.FileField(null=True, blank=True)

  is_delete = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

  def __str__(self):
    return str(self.room) + '  ' + str(self.id)