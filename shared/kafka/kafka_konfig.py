from pydantic_settings import BaseSettings

class KafkaSettings(BaseSettings):
    BOOTSTRAP_SERVERS: str = "kafka:9092"
    RESPONSE_TIMEOUT: float = 5.0
    DEFAULT_GROUP_ID: str = "default_group"

    ORDER_NOTIFICATION_TOPIC: str = 'order-notification'

    class Config:
        env_prefix = 'KAFKA_'

kafka_settings = KafkaSettings()
