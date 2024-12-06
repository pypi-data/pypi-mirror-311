name = "local"

# __init__.py
from reader import (
    vLLMPredict
)

from server import (
    start_single_model_server
)


__all__ = [
    "vLLMPredict",

    "start_single_model_server"
]