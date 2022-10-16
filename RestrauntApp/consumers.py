import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class NewOrderConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['id']
        self.room_group_name = 'id_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,self.channel_name
        )
        self.accept()
        print(self.room_group_name)

    def disconnect(self, close_code):
        print("I am disconnected")

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json['content']
        print(content)
        self.send(text_data=json.dumps({
            'order_id': content
        }))
        
    def new_order(self, event):
        data = event
        self.send(text_data=json.dumps({'payload':data}))

class OrderConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = 'id_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,self.channel_name
        )
        self.accept()
      

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        pass
        
    def order_status(self, event):
        data = event
        self.send(text_data=json.dumps({'payload':data}))