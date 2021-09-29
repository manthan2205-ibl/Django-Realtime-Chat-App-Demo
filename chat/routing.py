from django.urls import path

from . import consumers

websocket_urlpatterns = [
  path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()), # Using asgi
  path('ws/<int:room_id>/<int:user_id>/', consumers.MessageConsumer.as_asgi()), # Using asgi

  
]