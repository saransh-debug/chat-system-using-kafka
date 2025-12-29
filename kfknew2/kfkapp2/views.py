from django.shortcuts import render, redirect
from kfkapp2.models import main_chat
from kfkapp2.producer import start_chat
from kfkapp2.consumer import start_chat_p2


def person1(request):
    
    if request.method == "POST":
        inputval = request.POST.get("person1input", "").strip()

        if inputval:
            start_chat(inputval)

    
        return redirect("person1")

    
    msg = (
        main_chat.objects
        .filter(owner_name__name="person-1")
        .order_by("-time")[:50]   
    )

    data_msg = [
        {
            "message": i.message,
            "sender": i.sender
        }
        for i in reversed(msg) if i.message
    ]

    return render(
        request,
        "person1.html",
        {"msg_data": data_msg}
    )


def person2(request):
    
    if request.method == "POST":
        inputval = request.POST.get("person2input", "").strip()

        if inputval:
            start_chat_p2(inputval)

       
        return redirect("person2")

    msg = (
        main_chat.objects
        .filter(owner_name__name="person-2")
        .order_by("-time")[:50]
    )

    data_msg = [
        {
            "message": i.message,
            "sender": i.sender
        }
        for i in reversed(msg) if i.message
    ]

    return render(
        request,
        "person2.html",
        {"msg_data": data_msg}
    )
