
from django.contrib import admin
from django.urls import path
from kfkapp2.views import person1 , person2
urlpatterns = [
    path('' , person1 , name="person1"),
    path('person2/' , person2 , name="person2"),
    
    path('admin/', admin.site.urls),
]
