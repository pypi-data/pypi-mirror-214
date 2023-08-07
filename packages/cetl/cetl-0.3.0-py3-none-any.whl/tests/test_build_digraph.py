import os
from cetl import build_pipeline
from cetl.pandas_modules import generateDataFrame, unionAll
from cetl.functional_modules import dummyStart, parallelTransformer
from cetl import DataPipeline


def test_build_digraph():

    # method 1
    cfg = {"pipeline":[ {"type":"dummyStart", "module_type":"functional"},
                        {"type":"parallelTransformer", "transformers":[
                            {"type":"generateDataFrame"},
                            {"type":"generateDataFrame"}
                        ]},
                        {"type":"unionAll"}
    ]}
    pipe = DataPipeline(cfg)
    df = pipe.transform("")
    pipe = pipe.build_digraph()
    pipe.save_png("./tests/sample1.png")

    assert os.path.exists("./tests/sample1.png")


    # method 2
    pipe = build_pipeline(  dummyStart(),
                            parallelTransformer([generateDataFrame(), generateDataFrame()]), 
                            unionAll())
    df = pipe.transform("")
    pipe = pipe.build_digraph()
    pipe.save_png("./tests/sample2.png")
    assert os.path.exists("./tests/sample2.png")