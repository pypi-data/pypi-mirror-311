from pyspark.sql import DataFrame
from mx_stream_core.infrastructure.spark import spark
from .base import BaseDataSource
from mx_stream_core.infrastructure.delta import get_delta_path

class SparkDeltaDataSource(BaseDataSource):
    def __init__(self, table_name: str, schema, delta_path) -> None:
        self.schema = schema
        self.table_name = table_name
        self.delta_path = delta_path

    def get(self) -> DataFrame:
        try:
            if self.table_name:
                return spark.read.format('delta').load(get_dims_delta_path(self.table_name))
            return spark.read.format('delta').load(self.delta_path)
        except Exception as e:
            return spark.createDataFrame(data=[], schema=self.schema)
