from django.db import models

# Create your models here.
class person(models.Model):
    name = models.CharField()
    
    
    def __str__(self):
        return self.name
    
class chatroom(models.Model):
    person1 = models.ForeignKey(person , on_delete=models.CASCADE , related_name="person1")
    person2 = models.ForeignKey(person , on_delete=models.CASCADE  , related_name="person2")
    owner = models.ForeignKey(person , on_delete=models.CASCADE , related_name="chatroom_owner" , null=True , blank=True
                              )
    
    class Meta:
        unique_together = ['person1', 'person2', 'owner']
    
    def __str__(self):
        return f"{self.owner} for {self.person1} and {self.person2}"
    #     return None
    
class main_chat(models.Model):
    sender = models.ForeignKey(person , on_delete=models.CASCADE , related_name="mainchatsender")
    owner_name = models.ForeignKey(person , on_delete=models.CASCADE , related_name="ownername" , null=True , blank=True)
    chat_room = models.ForeignKey(chatroom , on_delete=models.CASCADE , related_name="chat_owner")
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        
        return f"{self.sender} "
    