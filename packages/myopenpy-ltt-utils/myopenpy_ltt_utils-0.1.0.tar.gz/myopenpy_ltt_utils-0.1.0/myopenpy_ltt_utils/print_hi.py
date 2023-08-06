"""
@FileName  :util.py
@Time      :2023/6/17 15:28
@Author    :tingting.liu
@Comment:
"""
import pandas as pd


def print_hi(text):
    x = pd.DataFrame(data={1, 2, 3}, columns=["key"])
    return x, text


if __name__ == '__main__':
    print(print_hi("hello"))
