from trace_logger.logging_adapter import get_logger
from trace_logger.utils import set_trace_id, get_trace_id

def test_logger_with_trace_id():
    set_trace_id("12345")
    logger = get_logger("test_logger")
    logger.info("Test log")
    assert "12345" in get_trace_id()
