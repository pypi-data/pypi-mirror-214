# from cetl.pandas_modules.input import generateDataFrame
from cetl import build_pipeline
from cetl.pandas_modules import generateDataFrame

def test_build_pipeline1():

    answer = generateDataFrame().transform("")
    # print(answer)


    pipe = build_pipeline(generateDataFrame())
    df = pipe.transform("")
    print(df)

    assert df.equals(answer)



