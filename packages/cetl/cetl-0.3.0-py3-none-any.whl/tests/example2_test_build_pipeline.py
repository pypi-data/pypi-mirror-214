from cetl import build_pipeline
from cetl.pandas_modules import generateDataFrame, unionAll
from cetl.functional_modules import dummyStart, parallelTransformer
from cetl import DataPipeline

def test_build_pipeline2():

    answer = dummyStart().transform("")
    answer = parallelTransformer([generateDataFrame(), generateDataFrame()]).transform(answer)
    answer = unionAll().transform(answer)


    # method 1
    pipe = build_pipeline(  dummyStart(),
                            parallelTransformer([generateDataFrame(), generateDataFrame()]), 
                            unionAll())
    df = pipe.transform("")
    assert df.equals(answer)

    # method 2
    cfg = {"pipeline":[ {"type":"dummyStart", "module_type":"functional"},
                        {"type":"parallelTransformer", "transformers":[
                            {"type":"generateDataFrame"},
                            {"type":"generateDataFrame"}
                        ]},
                        {"type":"unionAll"}
    ]}

    pipe = DataPipeline(cfg)
    df = pipe.transform("")

    assert df.equals(answer)