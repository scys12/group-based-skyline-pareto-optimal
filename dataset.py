import pandas


def transform_real_world_dataset(filename):
    # 'CA', 'Wor', 'Tec',
    # 'CA', 'Wor', 'Tec', 'Tea',
    # 'CA', 'Wor', 'Tec', 'Tea', 'Str'
    # 'CA', 'Wor', 'Tec', 'Tea', 'Str', 'Pas'
    # 'CA', 'Wor', 'Tec', 'Tea', 'Str', 'Pas', 'Dri'
    pd = pandas.read_csv(filename)
    pd = pd[
        [
            "CA",
            "Wor",
            "Tec",
            "Tea",
            "Str",
            "Pas",
            "Dri",
            "Ldr",
            "Pos",
            "Fir",
            "Sta",
            "Det",
            "Cnt",
        ]
    ]
    pd = pd.drop_duplicates()
    pd = pd.interpolate()
    pd = -pd
    # pd = pd.sample(n=15000)
    pd.to_csv(
        "data/fm_{}_1000000.txt".format(len(pd.columns)),
        header=False,
        index=False,
        sep=" ",
    )
    return pd.values.tolist()


def read_txt_dataset(filename):
    pd = pandas.read_csv(filename, sep=" ", header=None)
    pd = pd.drop_duplicates()
    return pd.values.tolist()
