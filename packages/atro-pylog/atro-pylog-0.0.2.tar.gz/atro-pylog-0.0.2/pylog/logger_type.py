from enum import Enum


class LoggerType(Enum):
    LOGURU = "Loguru"
    OPENTELEMETRY = "OpenTelemetry"


def str_to_logger_type(type: str) -> LoggerType:
    if type.lower() == "loguru":
        return LoggerType.LOGURU
    elif type.lower() == "opentelemetry":
        return LoggerType.OPENTELEMETRY
    else:
        raise Exception(f"Unknown logger type: {type}")
