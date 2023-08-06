from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import StructField, StructType, StringType
import pyspark.sql.functions as F
from pyspark.sql.window import Window
import argparse
from cs.dwh_streaming.share.cc_dwh_streaming_pkg.py_utils import cs_to_list, get_table_batch_records


class KeyValue(argparse.Action):
    """
    Custom action class for argument parsing that takes a list of
    key-value pairs and stores them as a dictionary.
    """

    def __call__(self, parser, namespace,
                 values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            # split it into key and value
            key, value = value.split('=')
            # assign into dictionary
            getattr(namespace, self.dest)[key] = value


def get_cmd_vars(args: dict) -> dict:
    """
    Parses command line arguments into a dictionary.
    """
    parser = argparse.ArgumentParser()
    for arg in args['required']:
        parser.add_argument(f"--{arg}", required=True)
    for arg in args['optional']:
        parser.add_argument(f"--{arg}")
    parser.add_argument("--kwargs", nargs='*', action=KeyValue)
    args = parser.parse_args()
    args_dict = vars(args)
    if args.kwargs:
        for key in args.kwargs:
            args_dict.setdefault(key, args.kwargs[key])
    args_dict.pop('kwargs', None)
    return args_dict


def get_message_schema(cluster: str = 'answers') -> StructType:
    """
    Returns the schema for the CDC message as StructType object.
    """
    if cluster == 'answers' or cluster == 'answers_dev':
        payload_schema = [
            StructField("before", StringType()),
            StructField("after", StringType()),
            StructField("source", StringType()),
            StructField("op", StringType()),
            StructField("ts_ms", StringType()),
            StructField("transaction", StringType())
        ]

    else:
        payload_schema = [
            StructField("data", StringType()),
            StructField("source", StringType())
        ]
    message_schema = (
        StructType([
            StructField("schema", StringType()),
            StructField("payload", StructType(payload_schema))
        ]))
    return message_schema


def get_kafka_config(cluster_api_key_var: str, cluster_api_secret_var: str, kafka_host_var: str,
                     kafka_server_var: str) -> dict:
    """
    Returns a dictionary containing Kafka configuration settings.
    """
    cluster_api_key = cluster_api_key_var
    cluster_api_secret = cluster_api_secret_var
    kafka_host = kafka_host_var
    kafka_server = kafka_server_var
    kafka_config = {
        "kafka_sasl_jaas_config": f'org.apache.kafka.common.security.plain.PlainLoginModule required username="{cluster_api_key}" password="{cluster_api_secret}";',
        "kafka.sasl.mechanism": "PLAIN",
        "kafka.security.protocol": "SASL_SSL",
        "kafka_bootstrap_servers": f"{kafka_host}:{kafka_server}",
        "client.dns.lookup": "use_all_dns_ips",
        "minPartitions": 300
    }
    return kafka_config


def generate_topics_dict(topic_entities: dict) -> dict:
    """
    Given a dictionary of entities' topics, generates a new dictionary mapping each entity to a corresponding topic name.
    """
    topics_dict = {
        entity: f"cdc.cc-dwh-{topic_entities[entity]['entity_name']}.answers.wix_connect.{topic_entities[entity]['entity_table']}.binlog"
        for entity in topic_entities}
    return topics_dict


def parsed_raw_messages(df: DataFrame, cluster: str = 'answers') -> DataFrame:
    """
    Parses DataFrame of raw messages from a Kafka topic using a predefined schema and returns a DataFrame.
    """
    schema = get_message_schema(cluster)
    parsed_df = df \
        .selectExpr("cast (value as STRING) as jsonData", "cast(key as STRING) as kafka_key", "topic as kafka_topic",
                    "partition as kafka_partition", "offset as kafka_offset", "timestamp as kafka_timestamp",
                    "timestampType as kafka_timestampType") \
        .select(F.from_json("jsonData", schema).alias("message"),
                F.current_timestamp().alias("process_timestamp"), "kafka_key", "kafka_topic",
                "kafka_partition", "kafka_offset", "kafka_timestamp", "kafka_timestampType")
    if cluster == 'answers' or cluster == 'answers_dev':
        parsed_df = parsed_df.select("message.payload.before", "message.payload.after", "process_timestamp",
                                     "kafka_key", "kafka_topic", "kafka_partition", "kafka_offset", "kafka_timestamp",
                                     "kafka_timestampType")
    else:
        parsed_df = parsed_df.select("message.payload.data", "process_timestamp", "kafka_key", "kafka_topic",
                                     "kafka_partition", "kafka_offset", "kafka_timestamp", "kafka_timestampType")
    return parsed_df


def writeStreamforeachBatch(batch_df, batch_id, spark, query_runner, catalog, schema, stream_table, full_table):
    """
    Writes a batch of data from a streaming DataFrame to two presto tables.
    """
    batch_df = batch_df.withColumn('batch_id', F.lit(batch_id)) \
        .select("before", "after", "batch_id", "process_timestamp",
                "kafka_key", "kafka_topic", "kafka_partition",
                "kafka_offset", "kafka_timestamp", "kafka_timestampType")
    batch_df.persist()
    spark.catalog.dropGlobalTempView("stream_temp")
    batch_df.createGlobalTempView("stream_temp")
    storing_tables = [f'{full_table}', f'{stream_table}']
    for table in storing_tables:
        if table == '':
            continue
        print(f"#### storing data in {catalog}.{schema}.{table} #####")  # TODO: logging
        query_runner.sql(
            f"""INSERT INTO {catalog}.{schema}.{table}
                    SELECT *
                    FROM global_temp.stream_temp""")  # TODO: consider ParquetTableStorer/df.write instead
    batch_df.unpersist()


def process_batch_wrapper(offsets_per_trigger: int, **kwargs) -> None:
    """
    Wrapper for writeStreamforeachBatch func
    that also check if we fetched less than the max offset and stopping the stream
    """
    writeStreamforeachBatch(**kwargs)
    res = get_table_batch_records(kwargs["catalog"], kwargs["schema"], kwargs["full_table"])
    try:
        num_of_records = res[0][1]
    except IndexError:
        num_of_records = 0
    if num_of_records > (offsets_per_trigger / 2):
        print(f'#### found {num_of_records} records, continuing ####')
    else:
        raise Exception(f'#### found {num_of_records} records, ending the stream ####')


def prepared_stream_df(stream_df: DataFrame) -> DataFrame:
    """
    prepares a given streaming DataFrame of CDC records,by selecting specific columns
    and generating a "record_type" column based on the before and after values.
    returns the prepared DataFrame.
    """
    stream_df_prep = stream_df \
        .select('before', 'after', 'kafka_timestamp', 'kafka_offset',
                F.lit(F.when((F.col('before').isNotNull() & F.col('after').isNotNull()), 'updated')
                      .when((F.col('before').isNotNull() & F.col('after').isNull()), 'deleted')
                      .when((F.col('after').isNotNull() & F.col('before').isNull()), 'created')
                      .otherwise('non-cdc')).alias('record_type')) \
        .filter(F.col('record_type') != 'non-cdc') \
        .select('record_type',
                F.lit(
                    F.when(((F.col('record_type') == 'updated') | (F.col('record_type') == 'created')), F.col('after'))
                    .otherwise(F.col('before'))).alias('payload')
                , F.lit(
            F.when(((F.col('record_type') == 'updated') | (F.col('record_type') == 'created')), F.col('before'))
            .otherwise(F.col('after'))).alias('prev_payload')
                , F.lit(F.when((F.col('record_type') == 'deleted'), 1)
                        .otherwise(0)).alias('is_hard_deleted')
                , 'kafka_timestamp', 'kafka_offset'
                )
    return stream_df_prep


def generate_payload_expr(payload_columns: list) -> list:
    """
    Given a list of column names, generates a list of JSON expressions used to extract values from a payload column.
    """
    payload_expr = [F.get_json_object('payload', f'$.{column}').alias(f'{column}') for column in payload_columns]
    return payload_expr


def generate_coalesce_expr(coalesce_columns: dict) -> list:
    """
    Given a dictionary mapping coalesce column names to a new columns, generates a list of
    expressions that coalesce each column and its alternative(s) into a new column with the given column name.
    """
    coalesce_expr = [F.coalesce(*[F.col(column) for column in cs_to_list(columns)])
                         .alias(coalesce_columns[columns]) for columns in coalesce_columns]
    return coalesce_expr


def generate_nested_expr(nested_columns: dict) -> list:
    """
    Given a dictionary mapping column names to a list of sub-column names, generates a nested list of expressions used
    to extract values from a JSON column.
    """
    nested_expr = [[F.get_json_object(column, f'$.{sub_column}').alias(f'{nested_columns[column][sub_column]}')
                    for sub_column in nested_columns[column]] for column in nested_columns]
    return nested_expr


def generate_casting_item(column: str, cast_to: str, cast_from: str = 'string'):
    """
    Given a column name, target type, and (optionally) source type, generates an expression used to cast the column
    to the target type.
    """
    if cast_to == 'timestamp':
        return F.to_timestamp(F.col(column) / 1000).alias(column)  # TODO: other types
    if cast_to == 'array<string>':
        return F.from_json(F.col(column), cast_to).alias(column)
    if cast_to == 'boolean':
        return F.col(column).cast("boolean").alias(column)


def generate_casting_list(df_columns: list, casting_column: dict) -> list:
    """
    Generates a list of PySpark expressions for casting the columns of a DataFrame based on a dictionary mapping column
    names to target data types.
    """
    casting_expr = [(generate_casting_item(df_col, casting_column[df_col])
                     if df_col in casting_column.keys() else F.col(df_col)) for df_col in df_columns]
    return casting_expr


def df_raw_to_slowly(raw_df: DataFrame, key_col: str = 'id', order_by_col: str = 'last_update_date') -> DataFrame:
    """
    Given a raw DataFrame, key columns and the order-by columns, transforms a raw dataframe into a slowly changing
    dimension (SCD) Type 2 dataframe. It adds a "rev_in_batch" column that contains the revision number for each record,
    based on the order of the specified key columns and the specified order-by columns (descending),
    as well as the Kafka timestamp and offset. The function returns the transformed dataframe.
    """
    key_col_list, order_by_col_list = cs_to_list(key_col), cs_to_list(order_by_col)
    key_expr = [F.col(key) for key in key_col_list]
    order_by_expr = [F.col(order_key).desc() for order_key in order_by_col_list + ['kafka_timestamp', 'kafka_offset']]
    partition = Window.partitionBy(key_expr).orderBy(order_by_expr)
    slowly_df = raw_df \
        .withColumn('rev_in_batch', F.row_number().over(partition))
    return slowly_df


def df_slowly_to_latest(slowly_df: DataFrame) -> DataFrame:
    """
    Filters out all but the latest revision of each record in a slowly changing dimension (SCD) dataframe
    and returns the filtered dataframe.
    """
    latest_df = slowly_df.filter(F.col('rev_in_batch') == 1) \
        .select([df_col for df_col in slowly_df.columns if df_col != 'rev_in_batch'])
    return latest_df

# common TODO: 1.consider ParquetTableStorer vs. spark.sql commands
#              2. df.repartition('device_type').sortWithinPartitions('device_type') when writing the tables
