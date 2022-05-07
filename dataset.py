import pandas


def read_nba_dataset(filename):
    nba_file = open(filename)
    pd = pandas.read_csv(nba_file)
    pd = pd[['PTS', 'REB', 'AST', 'STL', 'BLK']]
    pd = pd.drop_duplicates()
    pd = pd.interpolate()
    pd = -pd
    outfile = open('nba_{}.txt'.format(len(pd.columns)), 'w')
    outfile.write(pd.to_csv(header=False, index=False, sep=' '))
    outfile.close()
    return pd.values.tolist()


def read_txt_dataset(filename):
    file = open(filename)
    pd = pandas.read_csv(file, sep=" ", header=None)
    return pd.values.tolist()
