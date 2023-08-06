"""s3-delta target class."""

from __future__ import annotations

import os

from deltalake import write_deltalake
import pyarrow as pa
import pyarrow.parquet as pq
from singer_sdk import typing as th
from singer_sdk.target_base import Target

from target_s3_delta.sinks import (
    S3DeltaSink,
    TEMP_DATA_DIRECTORY,
)


def read_parquet_generator(file_paths):
    for file_path in file_paths:
        # Read the Parquet file
        table = pq.read_table(file_path)

        # Convert the Table to a single RecordBatch and yield it
        record_batch = pa.RecordBatch.from_pandas(table.to_pandas())
        yield record_batch


class TargetS3Delta(Target):
    """Sample target for s3-delta."""

    name = "target-s3-delta"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "s3_path",
            th.StringType,
            description="The s3 path to the target output file",
            required=True,
        ),
        th.Property("aws_access_key_id", th.StringType, required=True),
        th.Property(
            "aws_secret_access_key",
            th.StringType,
            required=True,
        ),
        th.Property("aws_region", th.StringType, default="us-east-1"),
    ).to_dict()

    default_sink_class = S3DeltaSink

    def _process_endofpipe(self):
        storage_options = {
            "AWS_ACCESS_KEY_ID": self.config.get("aws_access_key_id"),
            "AWS_SECRET_ACCESS_KEY": self.config.get("aws_secret_access_key"),
            "REGION": self.config.get("aws_region"),
            "AWS_S3_ALLOW_UNSAFE_RENAME": "true",
        }

        path = self.config.get("s3_path")

        files = os.listdir(TEMP_DATA_DIRECTORY)
        absolute_files = [f"{TEMP_DATA_DIRECTORY}{file}" for file in files]

        data = read_parquet_generator(absolute_files)
        schema = pq.read_table(absolute_files[0]).schema

        write_deltalake(
            path,
            data,
            schema=schema,
            storage_options=storage_options,
            mode="overwrite",
            overwrite_schema=True,
        )

        self.logger.info(f"Transaction has created.")
