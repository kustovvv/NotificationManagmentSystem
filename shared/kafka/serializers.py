import json
from typing import Any, Callable

def json_serializer(data: Any) -> bytes:
    return json.dumps(data).encode('utf-8')

def json_deserializer(data: bytes) -> Any:
    return json.loads(data.decode('utf-8'))

class Serializer:
    @staticmethod
    def get_serializer() -> Callable[[Any], bytes]:
        return json_serializer
    
    @staticmethod
    def get_deserializer() -> Callable[[bytes], Any]:
        return json_deserializer
