import json
from channels.generic.websocket import WebsocketConsumer
import time



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        # Send an initial message to the client
        self.send(text_data=json.dumps({
            'original_message': None,  
            'response_message': 'How may I help you?'
        }))
    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.save_message(message)

        # Check if we need to send a predefined response
        response_message = self.send_response(message)
        
        # If no prede  fined response, get recent messages
        if not response_message:
            response_message = self.get_recent_messages()

        # Send the response back to the WebSocket
        self.send(text_data=json.dumps({
            'original_message': message,
            'response_message': response_message
        }))

    def save_message(self, message):
        from myapp.models import Message
        Message.objects.create(message=message)

    # def get_recent_messages(self):
    #     from chat.models import ChatMessage
    #     recent_messages = ChatMessage.objects.order_by('-timestamp')[:10]
    #     return "\n".join([f"{msg.message}" for msg in recent_messages])

    def send_response(self, message):
        if message.lower() == "hi":
            options = [
                "Hello, select any 1 option:",
                "1. Account Balance",
                "2. Talk to Customer Care",
                "3. Help with Services"
            ]
            return "\n".join(options)
        elif message == "1":
            return "Your account balance is $1,000."
        elif message == "2":
            return "Connecting you to customer care..."
        elif message == "3":
            return "Please specify the service you need help with."
        else:
            return "Invalid option. Please type 'hi' to start over."
