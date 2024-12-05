import logging
import inspect
from .utils import get_trace_id

class TraceIDAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        trace_id = get_trace_id()
        frame = inspect.currentframe()
        calling_frame = frame.f_back.f_back.f_back
        function_name = calling_frame.f_code.co_name
        return f"[trace_id: {trace_id}] [function: {function_name}] {msg}", kwargs

def get_logger(name: str = __name__) -> TraceIDAdapter:
    return TraceIDAdapter(logging.getLogger(name), {})
