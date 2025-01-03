from pydantic_settings import BaseSettings

class KafkaSettings(BaseSettings):
    BOOTSTRAP_SERVERS: str = "kafka:9092"
    RESPONSE_TIMEOUT: float = 5.0
    DEFAULT_GROUP_ID: str = "default_group"

    PRODUCT_PRICE_REQUEST_TOPIC: str = 'product-price-request'
    PRODUCT_PRICE_RESPONSE_TOPIC: str = 'product-price-response'

    class Config:
        env_prefix = 'KAFKA_'

kafka_settings = KafkaSettings()
