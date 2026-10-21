###如何对一列数字分段统计

    import pandas as pd

    # 创建一个包含数字的 Series
    data = pd.Series([1, 3, 5, 7, 9, 11, 13, 15, 17, 19])

    # 分段统计
    bins = [0, 5, 10, 15, 20]
    cuts = pd.cut(data, bins)
    result = cuts.value_counts()

    # 输出结果
    print(result)

