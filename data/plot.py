import pandas
import seaborn as sns
import matplotlib.pyplot as plt

def plot(filename):
    pd = pandas.read_csv(filename, sep=" ", header=None)
    pd = pd.drop_duplicates()
    sns.pairplot(pd, plot_kws={"s": 3})
    plt.savefig(f'{filename}.png')
    
plot('inde_3_10000.txt')