import logging

from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource

from pylog.logger import Logger


class OpenTelemetryLogger(Logger):
    def __init__(self, service_name: str | None = None, service_instance_id: str | None = None):
        self.logger_provider = LoggerProvider(
            resource=Resource.create(
                {
                    "service.name": service_name or "",
                    "service.instance.id": service_instance_id or "",
                },
            ),
        )
        set_logger_provider(self.logger_provider)

        self.exporter = OTLPLogExporter(insecure=True)
        self.logger_provider.add_log_record_processor(BatchLogRecordProcessor(self.exporter))
        self.handler = LoggingHandler(level=logging.NOTSET, logger_provider=self.logger_provider)

        # Attach OTLP handler to root logger
        logging.getLogger().addHandler(self.handler)
        self.logger = logging.getLogger(__name__)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)

    def shutdown(self):
        self.logger_provider.shutdown()
