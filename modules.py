from flask_sqlalchemy import SQLAlchemy
import json
from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "ACb4cb2c2e75790193dfdb1fdb2ac97c4e"
# Your Auth Token from twilio.com/console
auth_token  = "bab1a1e16508bfa5629290ed3381befc"
client = Client(account_sid, auth_token)

db = SQLAlchemy()

class Queue:

    def __init__(self):
        self._queue = [{"name": "German", "phone": 56972994374}, {"name": "Paola", "phone": 56972994374}, {"name": "Nicole", "phone": 56972994374}]
        # depending on the _mode, the queue has to behave like a FIFO or LIFO
        self._mode = 'LIFO'

    def enqueue(self, item):
        if self._mode == 'FIFO':
            self._queue.append(item)
            message = client.messages.create(
                to="+{}".format(item["phone"]), 
                from_="+12079001504",
                body="Has sido agregado a la fila! Tienes {} personas por delante".format(len(self._queue)-1))
        elif self.mode == 'LIFO':
            self._queue.append(item)
            message = client.messages.create(
                to="+{}".format(item["phone"]), 
                from_="+12079001504",
                body="Has sido agregado a la fila! Por favor espera tu turno, pronto serás atendido")
                
    def dequeue(self):
        queue = self._queue
        if self._mode == 'FIFO':
             message = client.messages.create(
                to="+{}".format(queue[0]["phone"]), 
                from_="+12079001504",
                body="Hola {}, es tu turno! Gracias por esperar!".format(queue[0]["name"]))
             queue.pop(0)

        elif self._mode == 'LIFO':
            message = client.messages.create(
                to="+{}".format(queue[(len(self._queue) - 1)]["phone"]), 
                from_="+12079001504",
                body="Hola {}, es tu turno! Gracias por esperar!".format(queue[(len(self._queue) - 1)]["name"]))
            queue.pop((len(self._queue) - 1))

    def get_queue(self):
        return self._queue
    def size(self):
        return len(self._queue) 