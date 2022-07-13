import pandas
from sklearn import preprocessing


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
        ]
    ]
    pd = pd.drop_duplicates()
    pd = pd.interpolate()
    pd.sample(n=50000, replace=True)
    fname = "data/fm_{}_50000.txt".format(len(pd.columns))
    pd.to_csv(
        fname,
        header=False,
        index=False,
        sep=" ",
    )
    transform_to_scaled_data(fname)


def transform_to_scaled_data(filename):
    pd = pandas.read_csv(filename, sep=" ", header=None)
    pd = pd.drop_duplicates()
    pd = pd.interpolate()
    x = pd.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    pd = pandas.DataFrame(x_scaled)
    pd.to_csv(filename, header=False, index=False, sep=" ")


def read_txt_dataset(filename):
    pd = pandas.read_csv(filename, sep=" ", header=None)
    pd = pd.drop_duplicates()
    return pd.values.tolist()


transform_real_world_dataset("data/datafm20.csv")
