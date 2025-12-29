from django.contrib import admin
from . models import *

# Register your models here.


admin.site.register(person)
admin.site.register(chatroom)

@admin.register(main_chat)
class PostAdmin(admin.ModelAdmin):
    list_display = ('sender', 'chat_room', 'message' , 'time')

    def sender(self , obj):
        return obj.person.name
    
    def chat_room(self , obj):
        return f"{self.owner} owner of {obj.chatroom.person1} and {obj.chatroom.person2} "