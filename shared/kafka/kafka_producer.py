import asyncio
from typing import Any, Dict, Optional
from aiokafka import AIOKafkaProducer
from fastapi import HTTPException
from shared.logger.logger import logger
from shared.kafka.serializers import Serializer
from shared.kafka.kafka_konfig import kafka_settings

class KafkaProducer:
    def __init__(self, kafka_bootstrap_servers: str = kafka_settings.BOOTSTRAP_SERVERS):
        self.bootstrap_servers = kafka_bootstrap_servers
        self.producer: Optional[AIOKafkaProducer] = None
        self._lock = asyncio.Lock()

    async def initialize(self) -> None:
        if self.producer is None:
            async with self._lock:
                if self.producer is None:
                    self.producer = AIOKafkaProducer(
                        bootstrap_servers=self.bootstrap_servers,
                        value_serializer=Serializer.get_serializer()
                    )
                    await self.producer.start()
                    logger.info("Kafka producer initialized")

    async def close(self) -> None:
        if self.producer:
            await self.producer.stop()
            self.producer = None
            logger.info("Kafka producer closed")

    async def send_message(self, topic: str, message: Dict[str, Any], key: bytes = None) -> None:
        try:
            await self.initialize()
            await self.producer.send(topic, value=message, key=key)
            logger.debug(f"Sent message to {topic}: {message}")
        except Exception as e:
            logger.error(f"Failed to send message to {topic}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")
