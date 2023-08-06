import os

from pylog.logger import Logger
from pylog.logger_type import LoggerType, str_to_logger_type
from pylog.loguru import LoguruLogger
from pylog.opentelemetry import OpenTelemetryLogger


def get_logger(type: LoggerType | str | None = None, service_name: str | None = None, service_instance_id: str | None = None) -> Logger:
    if type is None:
        type = os.getenv("ENV_VARIABLE_NAME", default=LoggerType.LOGURU)
    if isinstance(type, str):
        type = str_to_logger_type(type)

    match type:
        case LoggerType.LOGURU:
            return LoguruLogger()
        case LoggerType.OPENTELEMETRY:
            return OpenTelemetryLogger(service_name=service_name, service_instance_id=service_instance_id)
        case _:
            raise Exception(f"Unknown logger type: {type}")
