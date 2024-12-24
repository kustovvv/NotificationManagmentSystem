from uuid import uuid4
import asyncio
from fastapi import HTTPException

from shared.kafka.kafka_consumer import KafkaConsumer
from shared.kafka.kafka_producer import KafkaProducer
from shared.kafka.kafka_konfig import kafka_settings


class ProductServiceClient:
    def __init__(self):
        self.kafka_producer = KafkaProducer()

    async def get_product_data(self, user_id, product_id):
        correlation_id = str(uuid4())
        message = {'correlation_id': correlation_id, 'user_id': str(user_id), 'product_id': product_id}
        consumer = KafkaConsumer(group_id=f"order-service-{correlation_id}")
        try:
            await self.kafka_producer.send_message(kafka_settings.PRODUCT_PRICE_REQUEST_TOPIC, message)
            return await self._wait_for_response(consumer, correlation_id)
        finally:
            await consumer.close()

    async def _wait_for_response(self, consumer, correlation_id):
        try:
            filter_func = lambda msg: msg.get('correlation_id') == correlation_id
            async for response in consumer.consume_messages(kafka_settings.PRODUCT_PRICE_RESPONSE_TOPIC, filter_func):
                if 'error' in response:
                    raise HTTPException(status_code=response.status_code, detail=response.get('error', 'Unknown error'))
                return response.get('data', {})
        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail="Timeout waiting for product data")

    async def cleanup(self):
        await self.kafka_producer.close()
