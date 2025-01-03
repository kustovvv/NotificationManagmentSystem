import asyncio
from typing import Any, Optional
from uuid import uuid4
from aiokafka import AIOKafkaConsumer
from fastapi import HTTPException
from shared.logger.logger import logger
from shared.kafka.serializers import Serializer
from shared.kafka.kafka_konfig import kafka_settings


class KafkaConsumer:
    def __init__(self, kafka_bootstrap_servers: str = kafka_settings.BOOTSTRAP_SERVERS, group_id: str = None):
        self.bootstrap_servers = kafka_bootstrap_servers
        self.group_id = group_id or f"{kafka_settings.DEFAULT_GROUP_ID}-{uuid4()}"
        self.consumer: Optional[AIOKafkaConsumer] = None

    async def consume_messages(self, topic: str, timeout: float = kafka_settings.RESPONSE_TIMEOUT, filter_func = None):
        try:
            await self.initialize(topic)

            async with asyncio.timeout(timeout):
                async for message in self.consumer:
                    data = message.value
                    if filter_func is None or filter_func(data):
                        yield data

        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail="Timeout waiting for message")
        
        except Exception as e:
            logger.error(f"Error consuming messages from {topic}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to consume messages: {str(e)}")

    async def initialize(self, topic: str) -> None:
        if not self.consumer:
            self.consumer = AIOKafkaConsumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                value_deserializer=Serializer.get_deserializer()
            )
            await self.consumer.start()
            logger.info(f"Kafka consumer initialized for topic {topic}")
    
    async def close(self) -> None:
        if self.consumer:
            await self.consumer.stop()
            self.consumer = None
            logger.info("Kafka consumer closed")
