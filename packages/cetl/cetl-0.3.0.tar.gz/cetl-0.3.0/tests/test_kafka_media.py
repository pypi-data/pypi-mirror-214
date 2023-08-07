import os
import copy

import sys, os
sys.path.insert(0, os.path.join("."))
from cetl import build_pipeline
from cetl.pandas_modules import generateDataFrame, unionAll
from cetl.functional_modules import dummyStart, parallelTransformer
from cetl import DataPipeline

def test_kafka_media():
    """
    step 1: launch kafka containers
    cd kafka_learning

    step 2: launch zookeeper
    docker-compose up -d zookeeper

    step 3: launch broker
    docker-compose up -d broker

    # # delete the topic
    # pipe.kafka_media.delete_topic()

    # kafkacat -b localhost:9092 -t kafka_media_test

    # stop the focalboard
    sudo systemctl stop focalboard
    sudo lsof -i:9092
    sudo kill 9092
    fuser -k 9092/tcp
    """

    fernet_key = "20230315"
    pipe_topic_name = "kafka_media_test"

    # ---OK
    cfg = { "pipeline": [   {"type":"dummyStartEmpty"},
                            {"type":"parallelTransformer", "transformers":[
                                {"type":"generateDataFrame"},
                                {"type":"generateDataFrame"},
                                {"type":"generateDataFrame"}
                            ]},
                            {"type":"unionAll"}],
                        
            "pipeline_settings":{   "print_cfg":1, 
                                    "print_task_result":1, 
                                    "exchange_media":"default",
                                    "bootstrap_servers":["localhost:9092"],
                                    "fernet_key":f"{fernet_key}",
                                    "pipe_topic_name":f"{pipe_topic_name}"}}

    answer_cfg = copy.deepcopy(cfg)
    pipe = DataPipeline(answer_cfg)
    answer = pipe.transform("")
    # print(answer)



    # method 1
    cfg["pipeline_settings"]["exchange_media"]="kafka"
    kafka_cfg = cfg
    pipe = DataPipeline(kafka_cfg)
    result = pipe.transform("")

    # get the output of transformer by task_id
    task_id = b"5.unionAll"
    df = pipe.kafka_media.read_kafka(task_id=task_id)

    # # get the output of final
    print(df.to_markdown())

    assert df.equals(answer)
    

    # method 2
    # pipe = build_cetl_pipeline(cfg, bootstrap_servers=["192.168.176.1:9092"])