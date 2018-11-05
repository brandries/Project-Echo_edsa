# Functions and classes for visualization

def plot_by_factor(df, factor, colors, showplot=False):
    ''' Plot by factor on a already constructed
    t-SNE plot.
    '''
    import matplotlib.pyplot as plt

    listof = {}     # this gets numbers to get the colors right
    listnames = []
    for i, j in enumerate(df[factor].unique()):
        listof[j] = i
        listnames.append(j)
    df[factor] = df[factor].map(listof)

    f, ax = plt.subplots(figsize=(15,10))
    for a, i in enumerate(df[factor].unique()):
        ax.scatter(df[df[factor] == i][0],
                   df[df[factor] == i][1],
                   color=colors[i], label=listnames[a])
    ax.legend()
    ax.set_title('t-SNE colored by {}'.format(factor))

    if showplot == True:
        plt.show()
    else:
        f.savefig('images/{}.png'.format(factor))


class AnalyzeClusters(object):
    def __init__(self):
        pass


    def make_dataset(self, sales_df, clus_df):
        sales_df['sku_key'] = sales_df['sku_key'].astype(int)
        self.c_dfs = {}
        for i in clus_df['cluster'].unique():
            self.c_dfs['cluster_{}'.format(i)] = clus_df[clus_df['cluster'] == i]

        for i in self.c_dfs.keys():
            self.c_dfs[i] = self.c_dfs[i].merge(sales_df, on='sku_key')

        return self.c_dfs


    def plot_cluster_continuous(self, cluster_dfs, categories, colors, showplot=False):
        import matplotlib.pyplot as plt
        for j in categories:
            f, ax = plt.subplots(figsize=(15,10))
            for a, i in enumerate(cluster_dfs.keys()):
                cluster_dfs[i][j].plot(ax=ax, kind='hist', bins=20, logy=True,
                                       alpha=0.2, color=colors[a])
                plt.title(j)
                if j == 'sales':
                    plt.xlim(-50, 800)
                elif j == 'selling_price':
                    plt.xlim(-100, 8000)
                elif j == 'avg_discount':
                    plt.xlim(-1500, 2000)
            if showplot == True:
                plt.show()
            else:
                f.savefig('images/{}_continuous.png'.format(j))

    def plot_cluster_continuous_box(self, cluster_dfs, categories, showplot=False):
        import matplotlib.pyplot as plt
        import pandas as pd
        for j in categories:
            f, ax = plt.subplots(figsize=(15,10))
            for a, i in enumerate(cluster_dfs.keys()):
                if a == 0:
                    int_df = pd.DataFrame(cluster_dfs[i][j])
                    int_df.columns = [i]
                else:
                    temp = pd.DataFrame(cluster_dfs[i][j])
                    temp.columns = [i]
                    int_df = int_df.join(temp)

            int_df.plot(ax=ax, kind='box', color='red', whis=[2.5, 97.5])
            plt.title(j)

            if showplot == True:
                plt.show()
            else:
                f.savefig('images/{}_continuous-box.png'.format(j))


    def plot_cluster_continuous_violin(self, cluster_dfs, categories, showplot=False):
        import matplotlib.pyplot as plt
        import pandas as pd
        for j in categories:
            f, ax = plt.subplots(figsize=(15,10))
            for a, i in enumerate(cluster_dfs.keys()):
                if a == 0:
                    int_df = pd.DataFrame(cluster_dfs[i][j])
                    int_df.columns = [i]
                else:
                    temp = pd.DataFrame(cluster_dfs[i][j])
                    temp.columns = [i]
                    int_df = int_df.join(temp)
                    int_df = int_df.fillna(0)

            ax.violinplot(int_df.T)
            plt.title(j)

            if showplot == True:
                plt.show()
            else:
                f.savefig('images/{}_continuous-violin.png'.format(j))

    def test_continuous_feat(self, cluster_dfs, categories):
        import statsmodels.api as sm
        from statsmodels.formula.api import ols
        from statsmodels.stats.multicomp import pairwise_tukeyhsd
        import pandas as pd
        for j in categories:
            for a, i in enumerate(cluster_dfs.keys()):
                if a == 0:
                    int_df = pd.DataFrame(cluster_dfs[i][j])
                    int_df.columns = [i]
                else:
                    temp = pd.DataFrame(cluster_dfs[i][j])
                    temp.columns = [i]
                    int_df = int_df.join(temp)

            int_df_unpiv = int_df.melt().dropna()
            int_df_unpiv.columns = ['cluster', 'value']
            mod = ols('value ~ cluster', data=int_df_unpiv).fit()
            aov_table = sm.stats.anova_lm(mod, typ=2)
            print('\n \n', j)
            print(aov_table, '\n')
            print(pairwise_tukeyhsd(int_df_unpiv['value'],
                                    int_df_unpiv['cluster']))
        self.stats_table = int_df


    def plot_cluster_categorical(self, cluster_dfs, categories, showplot=False):
        import matplotlib.pyplot as plt
        import pandas as pd
        for j in categories:
            print('\n\n', j)
            for a, i in enumerate(cluster_dfs.keys()):
                if a == 0:
                    int_df = pd.DataFrame(cluster_dfs[i][j].value_counts())
                    int_df.columns = [i]
                else:
                    temp = pd.DataFrame(cluster_dfs[i][j].value_counts())
                    temp.columns = [i]
                    int_df = int_df.join(temp)
                    int_df = int_df.fillna(0)

            f, ax = plt.subplots(figsize=(15,10))
            int_df.T.plot(ax=ax, kind='bar', stacked=True)
            plt.title(j)
            plt.legend(bbox_to_anchor=(1.35, 1.1), bbox_transform=ax.transAxes, ncol=6)
            if showplot == True:
                plt.show()
            else:
                f.savefig('images/{}_categorical.png'.format(j))

        self.int_df = int_df
