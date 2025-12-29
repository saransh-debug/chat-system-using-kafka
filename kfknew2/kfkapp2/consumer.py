from confluent_kafka import Producer, Consumer
import threading
import json
from kfkapp2.models import person, chatroom, main_chat



sender1, _ = person.objects.get_or_create(name="person-1")
sender2, _ = person.objects.get_or_create(name="person-2")

chatroom2, _ = chatroom.objects.get_or_create(
    person1=sender1,
    person2=sender2,
    owner=sender2
)




def sender_func_p2(message):
    
    producer = Producer({
        "bootstrap.servers": "localhost:9092"
    })

    msg_data = {
        "name": "person-2",
        "message": message
    }

    producer.produce(
        "chat_p2_to_p1",
        json.dumps(msg_data).encode("utf-8")
    )

    main_chat.objects.create(
        sender=sender2,
        owner_name=sender2,
        chat_room=chatroom2,
        message=message
    )

    producer.flush()


def consumer_func_p2():
    
    consumer = Consumer({
        "bootstrap.servers": "localhost:9092",
        "group.id": "sender1data",
        "auto.offset.reset": "latest",
    })

    consumer.subscribe(["chat_p1_to_p2"])

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
                sender=sender1,
                owner_name=sender2,
                chat_room=chatroom2,
                message=data["message"]
            )

    finally:
        consumer.close()


def start_chat_p2(message):
    

    
    t = threading.Thread(
                target=consumer_func_p2,
                daemon=True
            )
    t.start()
            

    
    sender_thread = threading.Thread(
        target=sender_func_p2,
        args=(message,),
        daemon=True
    )
    sender_thread.start()
