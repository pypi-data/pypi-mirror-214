import json
import os
from pathlib import Path


def get_json_config(config_file_name: str) -> dict:
    """
    Given a configuration file's name, read it's JSON and returns it as a dictionary.
    """
    PATH = (Path(__file__) / "../").resolve()
    file_name = os.path.join(PATH, config_file_name)
    with open(file_name) as f:
        json_config = json.loads(f.read())
    return json_config


def cs_to_list(cs_list: str = "") -> list:
    """
    converts a comma-separated string into a list of values.
    """
    if cs_list == "":
        return []
    return cs_list.replace(" ", "").split(",")


def transform_to_exclude_cs(include_cs_list: str = "", config_file_name: str = "config_hourly.json") -> list:
    """
    convert the include entities list to the exclude entities list,
    by specifying all the elements that not include in the include entities list
    """
    include_list = cs_to_list(include_cs_list)
    all_entities_list = list(get_json_config(config_file_name).keys())
    exclude_list = [entity for entity in all_entities_list if entity not in include_list]
    exclude_cs = ','.join(exclude_list)
    return exclude_cs


def get_interval_name(dag_id: str) -> str:
    """
    returns a string indicating the interval of a DAG based on its ID.
    """
    interval = 'daily' if dag_id == 'cs-cdc-to-dwh-daily' else 'hourly'
    return interval


def get_config_file_name(entity: str) -> str:
    """
    returns a string indicating the config file name that includes the given entity.
    """
    if entity in get_json_config('config_daily.json').keys():
        config_file_name = 'config_daily.json'
    elif entity in get_json_config('config_hourly.json').keys():
        config_file_name = 'config_hourly.json'
    else:
        raise ValueError(f'#### Configuration file containing the given entity ("{entity}") is not found')
    return config_file_name


def get_user_config(dag_run, ti) -> dict:
    """
    Parses a JSON string containing user input configuration, validate it, enrich it, push all the keys as Xcoms,
    and returns a dict contains the enriched user input and cluster secrets.
    """
    from airflow.models import Variable
    from airflow.exceptions import AirflowFailException

    user_config = dag_run.conf
    # validate user input
    if not user_config:
        raise AirflowFailException("#### No user input configuration although is required ####")
    for inp in ['process', 'entity', 'cluster', 'recovery_start_ts', 'recovery_end_ts']:
        try:
            user_config[inp]
        except KeyError as err:
            raise AirflowFailException(f"#### The key '{inp}' doesn't exist in the input although it's required.\n"
                                       f"error:{err} ####")
    # enrich user input
    secret = Variable.get('cs_dwh_streaming_' + user_config['cluster'] + '_secret', deserialize_json=True)
    user_config.update(secret)
    # push user input as xcom
    for key in user_config.keys():
        ti.xcom_push(key=key, value=user_config[key])
    return user_config


def get_process_task_name(dag_run) -> str:
    """
    Returns the name of the task to be executed based on the process value passed in the trigger variables of a DAG run
    """
    from airflow.exceptions import AirflowFailException

    process = dag_run.conf['process']
    if process == 'history':
        task_name = 'read_kafka_topic_history'
    elif process == 'recovery':
        task_name = 'read_kafka_topic_recovery'
    else:
        raise AirflowFailException("#### 'process' key in the trigger variables must be 'history' or 'recovery',"
                                   f"found '{process}'####")
    print(f'#### starting {process} process ####')
    return task_name


def get_member_id(user_name: str, slack_token: str) -> str:
    """
    Returns the Slack ID of a member based on their user name
    """
    from airflow.exceptions import AirflowFailException
    import requests

    try:
        user_name = user_name.strip('@wix.com')
        slack_call = f'https://slack.com/api/users.lookupByEmail?token={slack_token}&email={user_name}@wix.com'
        answer = requests.get(slack_call).json()
        member_id = answer['user']['id']
    except KeyError as e:
        raise AirflowFailException(f"#### provided user name is not in the found.\ngot '{user_name}'.\nerror :{e} ####")
    return member_id


def get_ask_approval_message(entity: str, user_name: str, recovery_table: str, slack_token: str, ti) -> None:
    """
    Sends a message to streaming channel asking for user approval to insert the recovery_table table
    into production tables. It uses the get_member_id() function to get the Slack ID and sends a message with tag.
    The message contains a unique ok_message that is pushed to XCom to validate the approval.
    """
    from uuid import uuid4

    member_id = get_member_id(user_name, slack_token)
    process_id = str(uuid4())
    ok_message = f'ok {process_id}'
    message = \
        f"<@{member_id}> Please approve the Insert of the table `sandbox.cs.{recovery_table.format(entity)}` into `{entity}` " \
        f"streaming and full table by sending the exact message in this channel -> \n \n{ok_message}"
    send_slack_message(message)
    ti.xcom_push(key='ok_message', value=ok_message)


def send_slack_message(message: str) -> None:
    """
    sends a message to a Slack channel using the SlackAPIPostOperator
    """
    from airflow.providers.slack.operators.slack import SlackAPIPostOperator

    SlackAPIPostOperator(
        task_id='ask_for_user_approval',
        slack_conn_id='slack_bot_token',
        channel='cc-data-streaming',
        text=message
    ).execute()


def get_slack_response(slack_token: str) -> str:
    """
    returns the most recent message in the "cc-data-streaming" Slack channel, converted to lowercase
    """
    import requests

    slack_call = 'https://slack.com/api/conversations.history?channel=C03N27UE945&limit=1' \
                 f'&token={slack_token}'
    res = requests.get(slack_call).json()
    response = res['messages'][0]['text']
    return response.lower()


def get_user_approval(user_name: str, ok_message: str, slack_token: str) -> bool:
    """
    Waits for a user response in the "cc-data-streaming" Slack channel for a maximum of 10 minutes.
    If the user responds with the ok_message that was sent in get_ask_approval_message(), this function returns True.
    If the user does not respond (or respond with wrong input) within the time limit, an exception is raised.
    """
    from airflow.exceptions import AirflowFailException
    from time import sleep

    min_to_wait = 10
    while min_to_wait > 0:
        answer = get_slack_response(slack_token)
        if answer == ok_message:
            print(f'#### user {user_name} has approved the insert. got the answer: {answer} ####')
            return True
        else:
            print(f'#### waiting for user response ####')
            sleep(60)
            min_to_wait -= 1
    raise AirflowFailException(f'#### user {user_name} has NOT approved the insert. got the answer: {answer} '
                               f'expect {ok_message} ####')


def create_kafka_table_if_not_exists(catalog: str, schema: str, history_table: str) -> None:
    """
    Creates a table in Trino with the specified name and schema if it doesn't already exist.
    Raise Error if the table already exists.
    """
    from wix_trino_client.trino_connection import WixTrinoConnection, DatabaseError

    pc = WixTrinoConnection()
    try:
        table_creation_statement = \
            f""" CREATE TABLE {catalog}.{schema}.{history_table}(
                    before varchar,
                    after varchar,
                    batch_id varchar,
                    process_timestamp timestamp(6),
                    kafka_key varchar,
                    kafka_topic varchar,
                    kafka_partition integer,
                    kafka_offset bigint,
                    kafka_timestamp timestamp(6),
                    kafka_timestamptype integer
                    )"""
        pc.execute_sql(table_creation_statement)
    except DatabaseError as e:
        raise Exception(f'#### failed to create the table {catalog}.{schema}.{history_table}, '
                        f'overwrite existing table is not allowed.\n'
                        f'query:\nby executing:\n{table_creation_statement} \ngot the error:{e}####')
    print(f'#### created the table {catalog}.{schema}.{history_table}\nby executing:\n{table_creation_statement} ####')


def create_s3_folder_if_not_exists(s3_full_path: str) -> None:
    """
    Creates a folder in S3 bucket in the entity name, if it doesn't already exist.
    Raise Error if the folder already exists.
    """
    import boto3

    s3_resources = boto3.resource('s3')
    s3_client = boto3.client('s3')
    bucket_name, cluster_folder_name, entity_folder_name = s3_full_path.strip('s3://').split('/')
    bucket = s3_resources.Bucket(bucket_name)
    full_folder_name = cluster_folder_name + '/' + entity_folder_name + '/'

    # check if folder already exists
    for obj in bucket.objects.all():
        if full_folder_name in obj.key:
            raise Exception(f'#### {full_folder_name} already exists in {bucket_name} bucket. ####')

    s3_client.put_object(Bucket=bucket_name, Key=full_folder_name)
    print(f'#### {full_folder_name} created successfully in {bucket_name} bucket. ####')


def get_table_batch_records(catalog: str, schema: str, table: str) -> list:
    """
    Querying the num of records fetched from given table.
    """
    from wix_trino_client.trino_connection import WixTrinoConnection

    pc = WixTrinoConnection()
    res = pc.execute_sql(f'select batch_id, count(*) as num_of_records '
                         f'from {catalog}.{schema}.{table} '
                         f'group by batch_id '
                         f'order by CAST(batch_id AS INT) desc '
                         f'limit 1')
    return res


def check_if_process_succeeded(catalog: str, schema: str, table: str) -> None:
    """
    Checking if the history process was successful by querying the num of records fetched
    in the last streaming batch. fails the task if the table empty or doesn't exists.
    """
    from wix_trino_client.trino_connection import DatabaseError
    from airflow.exceptions import AirflowFailException

    try:
        res = get_table_batch_records(catalog, schema, table)
        if res[0][1] == 0:
            raise AirflowFailException(f'#### process fail, try again ####')
    except DatabaseError as e:
        raise AirflowFailException(f'#### process fail, try again ####')
# TODO: move here the non-spark func from
