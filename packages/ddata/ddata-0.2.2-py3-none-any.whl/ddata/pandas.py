import pandas as pd


class Pandas():
    def __init__(self):
        pass

    def get_pandas(self):
        # 显示所有列
        pd.set_option('display.max_columns', None)
        # 显示所有行
        pd.set_option('display.max_rows', None)
        # 显示宽度
        pd.set_option('display.width', 5000)
        # 设置value的显示长度为100，默认为50
        pd.set_option('max_colwidth', 100)
        return pd

