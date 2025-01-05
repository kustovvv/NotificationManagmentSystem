from uuid import uuid4
import asyncio
from fastapi import HTTPException
import datetime

from shared.kafka.kafka_consumer import KafkaConsumer
from shared.kafka.kafka_producer import KafkaProducer
from shared.kafka.kafka_konfig import kafka_settings

class OrderNotificationProducer:
    def __init__(self):
        self.kafka_producer = KafkaProducer()

    async def send_order_notification(self, user_id: str, order_data: dict):
        message = {'user_id': str(user_id), 
                   'order_data': order_data,
                   'timestamp': datetime.utcnow().isoformat()
                   }
        
        await self.kafka_producer.send_message(kafka_settings.ORDER_NOTIFICATION_TOPIC, message)

    async def cleanup(self):
        await self.kafka_producer.close()


class OrderNotificationConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(group_id="telegram-notification-service")

    async def process_notifications(self):
        async for message in self.consumer.consume_messages(kafka_settings.ORDER_NOTIFICATION_TOPIC):
            await self.send_telegram_notification(message)

    async def cleanup(self):
        await self.consumer.close()
