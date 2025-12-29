from confluent_kafka import Producer, Consumer
import threading
import json
from kfkapp2.models import person, chatroom, main_chat



sender1, _ = person.objects.get_or_create(name="person-1")
sender2, _ = person.objects.get_or_create(name="person-2")

chatroom1, _ = chatroom.objects.get_or_create(
    person1=sender1,
    person2=sender2,
    owner=sender1
)






def sender_func(message):
    producer = Producer({
        "bootstrap.servers": "localhost:9092"
    })

    msg_data = {
        "sender": "person-1",
        "message": message
    }

    producer.produce(
        "chat_p1_to_p2",
        json.dumps(msg_data).encode("utf-8")
    )

    main_chat.objects.create(
        sender=sender1,
        owner_name=sender1,
        chat_room=chatroom1,
        message=message
    )

    producer.flush()


def consumer_func():
    consumer = Consumer({
        "bootstrap.servers": "localhost:9092",
        "group.id": "sender2data",
        "auto.offset.reset": "latest",
    })

    consumer.subscribe(["chat_p2_to_p1"])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print(msg.error())
                continue

            data = json.loads(msg.value().decode("utf-8"))

            main_chat.objects.create(
                sender=sender2,
                owner_name=sender1,
                chat_room=chatroom1,
                message=data["message"]
            )

    finally:
        consumer.close()


def start_chat(message):
    
    


    
        
    t = threading.Thread(
                target=consumer_func,
                daemon=True
            )
    t.start()
            

    
    sender_thread = threading.Thread(
        target=sender_func,
        args=(message,),
        daemon=True
    )
    sender_thread.start()
