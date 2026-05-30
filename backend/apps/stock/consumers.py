"""WebSocket consumer for real-time stock updates."""
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'stock_updates'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        warehouse_id = data.get('warehouse_id')
        if warehouse_id:
            group = f'stock_warehouse_{warehouse_id}'
            await self.channel_layer.group_add(group, self.channel_name)

    async def stock_changed(self, event):
        await self.send(text_data=json.dumps({'type':'stock_changed','data':event.get('data')}))

    async def safety_stock_alert(self, event):
        await self.send(text_data=json.dumps({'type':'safety_stock_alert','data':event.get('data')}))
