import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statannot import add_stat_annotation
from tmkit.seqnetrr.util.Reader import reader as prrcreader
from tmkit.Path import to


class plot():

    def __init__(self, time_fpns, protein_fpns, ):
        self.time_fpns = time_fpns
        self.protein_fpns = protein_fpns
        self.prrcreader = prrcreader()
        self.df = pd.DataFrame()
        for ds, fpns in self.time_fpns['unipartite'].items():
            df_tmp = pd.DataFrame()
            for met, f in fpns.items():
                print(ds, met, f)
                df_tmp['time_total'] = self.prrcreader.generic(df_fpn=f)[0]
                df_tmp['id'] = self.prrcreader.generic(self.protein_fpns[ds]['id'])[0]
                df_tmp['length'] = self.prrcreader.generic(self.protein_fpns[ds]['length'])[0]
                df_tmp['pair_number'] = self.prrcreader.generic(self.protein_fpns[ds]['pair_number'])[0]
                df_tmp['window'] = self.prrcreader.generic(self.protein_fpns[ds]['window'])[0]
                df_tmp['dataset'] = ds
                df_tmp['method'] = met
                df_tmp['placeholder'] = '1'
                self.df = pd.concat([self.df, df_tmp], axis=0)
                print(self.df)
        self.df = self.df.reset_index(drop=True)

        self.df_cumu_train = pd.DataFrame()
        self.df_cumu_train['id'] = self.prrcreader.generic(self.protein_fpns['TRAIN']['id'])[0]
        self.df_cumu_train['length'] = self.prrcreader.generic(self.protein_fpns['TRAIN']['length'])[0]
        self.df_cumu_train['id+length'] = self.df_cumu_train.apply(lambda x: x['id'] + ' (' + str(x['length']) + ')', axis=1)
        for len_setting, fpn in self.time_fpns['cumulative']['TRAIN'].items():
            print(len_setting, fpn)
            self.df_cumu_train[len_setting] = self.prrcreader.generic(df_fpn=fpn)[0]
        print(self.df_cumu_train)
        self.df_cumu_train = self.df_cumu_train.sort_values(by=['length']).reset_index(drop=True)
        self.prot_train = self.df_cumu_train['id+length']
        self.df_cumu_train = self.df_cumu_train[['L/10', 'L/5', 'L/2', 'L', '1.5L', '2L', '5L', '10L']]
        print(self.df_cumu_train)

        self.df_cumu_previous = self.prrcreader.generic(df_fpn=self.time_fpns['cumulative']['PREVIOUS']['L'])
        self.df_cumu_previous.columns = ['L']
        self.df_cumu_previous['id'] = self.prrcreader.generic(self.protein_fpns['PREVIOUS']['id'])[0]
        self.df_cumu_previous['length'] = self.prrcreader.generic(self.protein_fpns['PREVIOUS']['length'])[0]
        self.df_cumu_previous['id+length'] = self.df_cumu_previous.apply(lambda x: x['id'] + ' (' + str(x['length']) + ')', axis=1)
        self.df_cumu_previous = self.df_cumu_previous.sort_values(by=['length']).reset_index(drop=True)
        self.prot_previous = self.df_cumu_previous['id+length']
        self.df_cumu_previous = self.df_cumu_previous[['L']]
        print(self.df_cumu_previous)

        self.df_cumu_test = self.prrcreader.generic(df_fpn=self.time_fpns['cumulative']['TEST']['L'])
        self.df_cumu_test.columns = ['L']
        self.df_cumu_test['id'] = self.prrcreader.generic(self.protein_fpns['TEST']['id'])[0]
        self.df_cumu_test['length'] = self.prrcreader.generic(self.protein_fpns['TEST']['length'])[0]
        self.df_cumu_test['id+length'] = self.df_cumu_test.apply(lambda x: x['id'] + ' (' + str(x['length']) + ')', axis=1)
        self.df_cumu_test = self.df_cumu_test.sort_values(by=['length']).reset_index(drop=True)
        self.prot_test = self.df_cumu_test['id+length']
        self.df_cumu_test = self.df_cumu_test[['L']]
        print(self.df_cumu_test)

    def biboxen(self, ):
        # t-test_ind, t-test_welch, t-test_paired, Mann-Whitney, Mann-Whitney-gt, Mann-Whitney-ls, Levene, Wilcoxon, Kruskal
        sns.set(font="Helvetica")
        sns.set_style("ticks")
        sns.set_theme(style="whitegrid")
        g = sns.catplot(
            x="placeholder",
            y="time_total",
            hue="method",
            col="dataset",
            # capsize=.2,
            palette="Set2",
            height=6,
            aspect=.75,
            # kind="point",
            kind="boxen",
            linewidth=2,
            data=self.df,
        )
        add_stat_annotation(
            g.fig.axes[0], data=self.df.loc[self.df['dataset'] == 'TRAIN'], x="placeholder", y="time_total", hue="method",
            box_pairs=[
                ((('1', 'pandas'), ('1', 'hash_ori'))),
                ((('1', 'pandas'), ('1', 'hash'))),
                ((('1', 'hash_ori'), ('1', 'hash'))),
            ],
            test='t-test_paired', text_format='full', loc='inside', verbose=2
        )
        add_stat_annotation(
            g.fig.axes[1], data=self.df.loc[self.df['dataset'] == 'PREVIOUS'], x="placeholder", y="time_total", hue="method",
            box_pairs=[
                ((('1', 'pandas'), ('1', 'hash_ori'))),
                ((('1', 'pandas'), ('1', 'hash'))),
                ((('1', 'hash_ori'), ('1', 'hash'))),
            ],
            test='t-test_paired', text_format='full', loc='inside', verbose=2
        )
        add_stat_annotation(
            g.fig.axes[2], data=self.df.loc[self.df['dataset'] == 'TEST'], x="placeholder", y="time_total", hue="method",
            box_pairs=[
                ((('1', 'pandas'), ('1', 'hash_ori'))),
                ((('1', 'pandas'), ('1', 'hash'))),
                ((('1', 'hash_ori'), ('1', 'hash'))),
            ],
            test="t-test_paired", text_format='full', loc='inside', verbose=2
        )
        leg = g._legend
        plt.setp(leg.get_title(), fontsize=14)
        plt.setp(leg.get_texts(), fontsize=14)
        leg.texts[0].set_text("Pandas")
        leg.texts[1].set_text("Hash_indirec")
        leg.texts[2].set_text("Hash")
        leg.set_title("Method")

        g.despine(left=True)
        g.set(xticklabels=[])
        g.set(xlabel=None)

        # g.set_xticklabels(fontsize=12)
        g.set_ylabels('Total running time (s)', fontsize=18)
        a0 = g.fig.axes[0]
        a0.set_title("TRAIN", fontsize=14)
        a1 = g.fig.axes[1]
        a1.set_title("PREVIOUS", fontsize=14)
        a2 = g.fig.axes[2]
        a2.set_title("TEST", fontsize=14)

        # g.set_xlabels('Sequencing error', fontsize=14)
        plt.show()

    def uniboxen(self, ):
        # t-test_ind, t-test_welch, t-test_paired, Mann-Whitney, Mann-Whitney-gt, Mann-Whitney-ls, Levene, Wilcoxon, Kruskal
        sns.set(font="Helvetica")
        sns.set_style("ticks")
        sns.set_theme(style="whitegrid")
        g = sns.catplot(
            x="placeholder",
            y="time_total",
            hue="method",
            col="dataset",
            # capsize=.2,
            palette="Set2",
            height=6,
            aspect=.75,
            # kind="point",
            kind="boxen",
            linewidth=2,
            data=self.df,
            # sharex=False
        )
        add_stat_annotation(
            g.fig.axes[0], data=self.df.loc[self.df['dataset'] == 'TRAIN'], x="placeholder", y="time_total", hue="method",
            box_pairs=[
                ((('1', 'numpy'), ('1', 'pandas'))),
                ((('1', 'numpy'), ('1', 'hash_ori'))),
                ((('1', 'numpy'), ('1', 'hash'))),
                ((('1', 'pandas'), ('1', 'hash_ori'))),
                ((('1', 'pandas'), ('1', 'hash'))),
                ((('1', 'hash_ori'), ('1', 'hash'))),
            ],
            test='t-test_paired', text_format='full', loc='inside', verbose=2
        )
        add_stat_annotation(
            g.fig.axes[1], data=self.df.loc[self.df['dataset'] == 'PREVIOUS'], x="placeholder", y="time_total", hue="method",
            box_pairs=[
                ((('1', 'numpy'), ('1', 'pandas'))),
                ((('1', 'numpy'), ('1', 'hash_ori'))),
                ((('1', 'numpy'), ('1', 'hash'))),
                ((('1', 'pandas'), ('1', 'hash_ori'))),
                ((('1', 'pandas'), ('1', 'hash'))),
                ((('1', 'hash_ori'), ('1', 'hash'))),
            ],
            test='t-test_paired', text_format='full', loc='inside', verbose=2
        )
        add_stat_annotation(
            g.fig.axes[2], data=self.df.loc[self.df['dataset'] == 'TEST'], x="placeholder", y="time_total", hue="method",
            box_pairs=[
                ((('1', 'numpy'), ('1', 'pandas'))),
                ((('1', 'numpy'), ('1', 'hash_ori'))),
                ((('1', 'numpy'), ('1', 'hash'))),
                ((('1', 'pandas'), ('1', 'hash_ori'))),
                ((('1', 'pandas'), ('1', 'hash'))),
                ((('1', 'hash_ori'), ('1', 'hash'))),
            ],
            test="t-test_paired", text_format='full', loc='inside', verbose=2
        )
        leg = g._legend
        plt.setp(leg.get_title(), fontsize=14)
        plt.setp(leg.get_texts(), fontsize=14)
        leg.texts[0].set_text("Numpy")
        leg.texts[1].set_text("Pandas")
        leg.texts[2].set_text("Hash_indirec")
        leg.texts[3].set_text("Hash")
        leg.set_title("Method")

        g.despine(left=True)
        g.set(xticklabels=[])
        g.set(xlabel=None)

        # g.set_xticklabels(fontsize=12)
        g.set_ylabels('Total running time (s)', fontsize=18)
        a0 = g.fig.axes[0]
        a0.set_title("TRAIN", fontsize=14)
        a1 = g.fig.axes[1]
        a1.set_title("PREVIOUS", fontsize=14)
        a2 = g.fig.axes[2]
        a2.set_title("TEST", fontsize=14)

        # g.set_xlabels('Sequencing error', fontsize=14)
        plt.show()

    def unibar(self, ):
        # t-test_ind, t-test_welch, t-test_paired, Mann-Whitney, Mann-Whitney-gt, Mann-Whitney-ls, Levene, Wilcoxon, Kruskal
        sns.set(font="Helvetica")
        sns.set_style("ticks")
        sns.set_theme(style="whitegrid")
        g = sns.catplot(
            x="placeholder",
            y="time_total",
            hue="method",
            col="dataset",
            # capsize=.2,
            palette="Set2",
            height=4,
            aspect=.6,
            kind="bar",
            linewidth=2,
            data=self.df,
        )

        # for bars in g.fig.axes.containers:
        # g.bar_label(g.containers[0])

        for i, bars in enumerate(g.fig.axes[0].containers):
            g.fig.axes[0].bar_label(bars, padding=14, fmt='%.2f', label_type='edge' if i != 0 else 'center', fontsize=10)
        for i, bars in enumerate(g.fig.axes[1].containers):
            g.fig.axes[1].bar_label(bars, padding=14, fmt='%.2f', label_type='edge' if i != 0 else 'center', fontsize=10)
        for i, bars in enumerate(g.fig.axes[2].containers):
            g.fig.axes[2].bar_label(bars, padding=14, fmt='%.2f', label_type='edge' if i != 0 else 'center', fontsize=10)
        # print(g.fig.axes)
        # print(g.fig.axes[0].containers)
        # print(g.fig.axes.containers)
        # print(g.containers)

        leg = g._legend
        plt.setp(leg.get_title(), fontsize=14)
        plt.setp(leg.get_texts(), fontsize=14)
        leg.texts[0].set_text("Numpy")
        leg.texts[1].set_text("Pandas")
        leg.texts[2].set_text("Hash_indirec")
        leg.texts[3].set_text("Hash")
        leg.set_title("Method")

        g.despine(left=True)
        g.set(xticklabels=[])
        g.set(xlabel=None)

        # g.set_xticklabels(fontsize=12)
        g.set_ylabels('Total running time (s)', fontsize=18)
        a0 = g.fig.axes[0]
        a0.set_title("TRAIN", fontsize=14)
        a1 = g.fig.axes[1]
        a1.set_title("PREVIOUS", fontsize=14)
        a2 = g.fig.axes[2]
        a2.set_title("TEST", fontsize=14)
        # g.set_xlabels('Sequencing error', fontsize=14)

        plt.subplots_adjust(
            top=0.92,
            bottom=0.08,
            left=0.08,
            right=0.96,
            # hspace=0.40,
            # wspace=0.15
        )
        plt.show()

    def bibar(self, ):
        # t-test_ind, t-test_welch, t-test_paired, Mann-Whitney, Mann-Whitney-gt, Mann-Whitney-ls, Levene, Wilcoxon, Kruskal
        sns.set(font="Helvetica")
        sns.set_style("ticks")
        sns.set_theme(style="whitegrid")
        g = sns.catplot(
            x="placeholder",
            y="time_total",
            hue="method",
            col="dataset",
            # capsize=.2,
            palette="Set2",
            height=4,
            aspect=.6,
            kind="bar",
            linewidth=2,
            data=self.df,
        )

        # for bars in g.fig.axes.containers:
        # g.bar_label(g.containers[0])

        for i, bars in enumerate(g.fig.axes[0].containers):
            g.fig.axes[0].bar_label(bars, padding=14, fmt='%.2f', label_type='edge' if i != 0 else 'center', fontsize=10)
        for i, bars in enumerate(g.fig.axes[1].containers):
            g.fig.axes[1].bar_label(bars, padding=14, fmt='%.2f', label_type='edge' if i != 0 else 'center', fontsize=10)
        for i, bars in enumerate(g.fig.axes[2].containers):
            g.fig.axes[2].bar_label(bars, padding=14, fmt='%.2f', label_type='edge' if i != 0 else 'center', fontsize=10)
        # print(g.fig.axes)
        # print(g.fig.axes[0].containers)
        # print(g.fig.axes.containers)
        # print(g.containers)

        leg = g._legend
        plt.setp(leg.get_title(), fontsize=14)
        plt.setp(leg.get_texts(), fontsize=14)
        leg.texts[0].set_text("Pandas")
        leg.texts[1].set_text("Hash_indirec")
        leg.texts[2].set_text("Hash")
        leg.set_title("Method")

        g.despine(left=True)
        g.set(xticklabels=[])
        g.set(xlabel=None)

        # g.set_xticklabels(fontsize=12)
        g.set_ylabels('Total running time (s)', fontsize=18)
        a0 = g.fig.axes[0]
        a0.set_title("TRAIN", fontsize=14)
        a1 = g.fig.axes[1]
        a1.set_title("PREVIOUS", fontsize=14)
        a2 = g.fig.axes[2]
        a2.set_title("TEST", fontsize=14)
        # g.set_xlabels('Sequencing error', fontsize=14)

        plt.subplots_adjust(
            top=0.92,
            bottom=0.08,
            left=0.1,
            right=0.96,
            # hspace=0.40,
            # wspace=0.15
        )
        plt.show()

    def hexa(self, ):
        sns.set(font="Helvetica")
        sns.set_style("ticks")
        fig, ax = plt.subplots(nrows=2, ncols=1, sharex=False, sharey=False, figsize=(4, 6))
        hb = ax[0].hexbin(
            self.df.loc[self.df['method'] == 'hash']['length'].values,
            self.df.loc[self.df['method'] == 'hash']['time_total'].values,
            gridsize=30, bins='log', cmap='inferno', alpha=0.7)
        # sns.jointplot(
        #     x=x,
        #     y=y, kind="hex", color="#4CB391")
        # ax.set(xlim=xlim, ylim=ylim)
        ax[0].set_title("Train")
        ax[0].set_xlabel("Molecular length", fontsize=11)
        ax[0].set_ylabel("Total running time (binned)", fontsize=11)
        cb = fig.colorbar(hb, ax=ax[0], label='log10(N)')
        ax[0].spines['right'].set_color('none')
        ax[0].spines['top'].set_color('none')

        hb = ax[1].hexbin(
            self.df.loc[self.df['method'] == 'hash']['pair_number'].values,
            self.df.loc[self.df['method'] == 'hash']['time_total'].values,
            gridsize=30, bins='log', cmap='inferno', alpha=0.7)
        # ax.set(xlim=xlim, ylim=ylim)
        ax[1].set_title("Test")
        ax[1].set_xlabel("Number of residue pairs", fontsize=11)
        ax[1].set_ylabel("Total running time (binned)", fontsize=11)
        cb = fig.colorbar(hb, ax=ax[1], label='log10(N)')
        ax[1].spines['right'].set_color('none')
        ax[1].spines['top'].set_color('none')
        plt.subplots_adjust(
            top=0.96,
            bottom=0.08,
            left=0.14,
            right=0.94,
            hspace=0.32,
            # wspace=0.10,
        )
        plt.show()

    def scatter(self, ):
        std = 'length'
        # std = 'pair_number'
        # time = 'time_total'
        time = 'window'
        df = self.df.loc[self.df['method'] == 'hash'].sort_values(by=[std])
        print(df)
        sns.set(font="Helvetica")
        sns.set_style("ticks")
        fig = plt.figure(figsize=(12, 10), dpi=80)
        grid = plt.GridSpec(4, 4, hspace=0.5, wspace=0.2)
        # Define the axes
        ax_main = fig.add_subplot(grid[:-1, :-1])
        ax_right = fig.add_subplot(grid[:-1, -1], xticklabels=[], yticklabels=[])
        ax_bottom = fig.add_subplot(grid[-1, 0:-1], xticklabels=[], yticklabels=[])

        # Scatterplot on main ax
        ax_main.scatter(
            x=std,
            y=time,
            data=df,
            # c='cornflowerblue',
            c=df[std].astype('category').cat.codes,
            cmap="crest",
            # linewidths=.5,
            alpha=.7,
            s=80,
        )
        # ax_main.plot([0, 1], [0, 1], c='black', lw=3, alpha=0.7)
        ax_main.spines['right'].set_color('none')
        ax_main.spines['top'].set_color('none')

        x = df[std].values
        y = df[time].values
        m, b = np.polyfit(x, y, 1)
        print(m, b)
        est = sm.OLS(y[40:], x[40:])
        est2 = est.fit()
        print("pvalues: ", est2.pvalues)
        print("tvalues: ", est2.tvalues)
        print("rsquared: ", est2.rsquared)
        print("rsquared_adj: ", )
        print(est2.rsquared_adj)
        ax_main.plot(x, m * x + b, c='black', lw=3, alpha=0.5)
        # ax_main.spines['right'].set_color('none')
        # ax_main.spines['top'].set_color('none')
        text_kwargs = dict(fontsize=16, )
        ax_main.text(
            ### /* uni */
            # 280,  # length
            # 0.62,  # length
            # 60000,  # pair_number
            # 1.26,  # pair_number

            ### /* bi */
            # 250, # length
            # 2.,  # length
            # 60000,  # pair_number
            # 5.26,  # pair_number

            ### /* window */
            # 60000,  # pair_number
            # 0.32,  # pair_number
            300, # length
            0.22,  # length

            'p-val: {:.2e}\n'.format(est2.pvalues[0]) + r'$R^{2}$: ' + '{:.2f}'.format(est2.rsquared), **text_kwargs)

        # histogram on the bottom
        ax_bottom.hist(df[std], 40, histtype='stepfilled', orientation='vertical', color='teal')
        ax_bottom.invert_yaxis()
        ax_bottom.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
        ax_bottom.spines['right'].set_color('none')
        ax_bottom.spines['bottom'].set_color('none')

        # histogram in the right
        ax_right.hist(df[time], 40, histtype='stepfilled', orientation='horizontal', color='teal')
        ax_right.spines['right'].set_color('none')
        ax_right.spines['top'].set_color('none')

        # Decorations
        # ax_main.set(title='Percentage of cells expressing ORs')
        ax_main.title.set_fontsize(18)
        # ax_main.set_xlabel('Number of residue pairs', fontsize=28)
        ax_main.set_xlabel('Molecular length', fontsize=28)
        # ax_main.set_ylabel('Total running time (s)', fontsize=28)
        ax_main.set_ylabel('Window generation time (s)', fontsize=28)

        for item in (
                [ax_main.xaxis.label, ax_main.yaxis.label] + ax_main.get_xticklabels() + ax_main.get_yticklabels()):
            item.set_fontsize(22)

        # for i, txt in enumerate(df['id'].values):
        #     if df[time].values[i] > 3:
        #         # print(df['length'].values[i])
        #         print(txt)
        #         ax_main.annotate(
        #             txt,
        #             (df['length'].values[i], df['time_total'].values[i] + 0.1),
        #             fontsize=8
        #         )
        # xlabels = ax_main.get_xticks().tolist()
        # ax_main.set_xticklabels(xlabels)
        fig.subplots_adjust(
            top=0.96,
            bottom=0.04,
            # left=0.08,
            left=0.10,
            right=0.98,
            # hspace=0.40,
            # wspace=0.15
        )
        plt.show()

    def uniheatmap(self, ):
        sns.set(font="Helvetica")
        sns.set_style("ticks")
        f, ax = plt.subplots(figsize=(20, 2))
        df = pd.DataFrame()
        df['id'] = self.df.loc[self.df['method'] == 'pandas'].reset_index(drop=True)['id']
        df['numpy'] = self.df.loc[self.df['method'] == 'numpy'].reset_index(drop=True)['time_total']
        df['pandas'] = self.df.loc[self.df['method'] == 'pandas'].reset_index(drop=True)['time_total']
        df['hash_ori'] = self.df.loc[self.df['method'] == 'hash_ori'].reset_index(drop=True)['time_total']
        df['hash'] = self.df.loc[self.df['method'] == 'hash'].reset_index(drop=True)['time_total']
        print(df)
        df.index = df['id']
        g = sns.heatmap(
            df[['numpy', 'pandas', 'hash_ori', 'hash']].T,
            cmap="rocket_r",
            linewidths=.5,
            xticklabels=df.index,
            yticklabels=['Numpy', 'Pandas', 'Hash_indirec', 'Hash'],
            ax=ax
        )
        # g.set_ylabel(rotate=90)
        print(g)
        plt.xticks( fontsize=6)
        plt.xlabel('')
        f.subplots_adjust(
            top=0.96,
            bottom=0.25,
            left=0.06,
            right=1,
            # hspace=0.40,
            # wspace=0.15
        )
        plt.show()
        return

    def biheatmap(self, ):
        sns.set(font="Helvetica")
        sns.set_style("ticks")
        f, ax = plt.subplots(figsize=(20, 1.5))
        df = pd.DataFrame()
        df['id'] = self.df.loc[self.df['method'] == 'pandas'].reset_index(drop=True)['id']
        df['pandas'] = self.df.loc[self.df['method'] == 'pandas'].reset_index(drop=True)['time_total']
        df['hash_ori'] = self.df.loc[self.df['method'] == 'hash_ori'].reset_index(drop=True)['time_total']
        df['hash'] = self.df.loc[self.df['method'] == 'hash'].reset_index(drop=True)['time_total']
        print(df)
        df.index = df['id']
        g = sns.heatmap(
            df[['pandas', 'hash_ori', 'hash']].T,
            cmap="rocket_r",
            linewidths=.5,
            xticklabels=df.index,
            yticklabels=['Pandas', 'Hash_indirec', 'Hash'],
            ax=ax,
        )
        # g.set_ylabel(rotate=90)
        plt.xticks(fontsize=6)
        plt.xlabel('')
        f.subplots_adjust(
            top=0.96,
            bottom=0.32,
            left=0.06,
            right=1,
            # hspace=0.40,
            # wspace=0.15
        )
        plt.show()
        return

    def biline(self, ):
        sns.set_theme(style="whitegrid")
        f, ax = plt.subplots(figsize=(20, 3))

        df = pd.DataFrame()
        df['pandas'] = self.df.loc[self.df['method'] == 'pandas'].reset_index(drop=True)['time_total']
        df['hash_ori'] = self.df.loc[self.df['method'] == 'hash_ori'].reset_index(drop=True)['time_total']
        df['hash'] = self.df.loc[self.df['method'] == 'hash'].reset_index(drop=True)['time_total']
        print(df)
        df['id'] = self.df.loc[self.df['method'] == 'pandas'].reset_index(drop=True)['id']
        df['length'] = self.df.loc[self.df['method'] == 'pandas'].reset_index(drop=True)['length']

        df['id+length'] = df.apply(lambda x: x['id'] + ' (' + str(x['length']) + ')', axis=1)
        df = df.sort_values(by=['length']).reset_index(drop=True)
        prot_marks = df['id+length']
        df = df[['pandas', 'hash_ori', 'hash']]
        df.columns = ['Pandas', 'Hash_indirec', 'Hash']
        df = df.rolling(5, center=True).mean()
        # print(self.df_cumu_train)
        sns.lineplot(
            data=df,
            palette="Set2",
            linewidth=1.5,
            ax=ax,
        )
        ax.set_xticks(np.arange(df.shape[0]), prot_marks.values)
        ax.set_xticklabels(prot_marks.values, fontsize=6, rotation=90)
        ax.set_ylabel('Total running time (s)', fontsize=14)
        ax.legend(fontsize=12)
        f.subplots_adjust(
            top=0.96,
            bottom=0.22,
            left=0.04,
            right=0.98,
            # hspace=0.40,
            # wspace=0.15
        )
        plt.show()

    def uniline(self, ):
        sns.set_theme(style="whitegrid")
        f, ax = plt.subplots(figsize=(20, 3))

        df = pd.DataFrame()
        df['numpy'] = self.df.loc[self.df['method'] == 'numpy'].reset_index(drop=True)['time_total']
        df['pandas'] = self.df.loc[self.df['method'] == 'pandas'].reset_index(drop=True)['time_total']
        df['hash_ori'] = self.df.loc[self.df['method'] == 'hash_ori'].reset_index(drop=True)['time_total']
        df['hash'] = self.df.loc[self.df['method'] == 'hash'].reset_index(drop=True)['time_total']
        print(df)
        df['id'] = self.df.loc[self.df['method'] == 'pandas'].reset_index(drop=True)['id']
        df['length'] = self.df.loc[self.df['method'] == 'pandas'].reset_index(drop=True)['length']

        df['id+length'] = df.apply(lambda x: x['id'] + ' (' + str(x['length']) + ')', axis=1)
        df = df.sort_values(by=['length']).reset_index(drop=True)
        prot_marks = df['id+length']
        df = df[['numpy', 'pandas', 'hash_ori', 'hash']]
        df.columns = ['Numpy', 'Pandas', 'Hash_indirec', 'Hash']
        df = df.rolling(5, center=True).mean()
        # print(self.df_cumu_train)
        sns.lineplot(
            data=df,
            palette="Set2",
            linewidth=1.5,
            ax=ax,
        )
        ax.set_xticks(np.arange(df.shape[0]), prot_marks.values)
        ax.set_xticklabels(prot_marks.values, fontsize=6, rotation=90)
        ax.set_ylabel('Total running time (s)', fontsize=14)
        ax.legend(fontsize=12)
        f.subplots_adjust(
            top=0.96,
            bottom=0.22,
            left=0.04,
            right=0.98,
            # hspace=0.40,
            # wspace=0.15
        )
        plt.show()

    def cumuTRAINline(self, ):
        sns.set_theme(style="whitegrid")
        f, ax = plt.subplots(figsize=(16, 6))
        self.df_cumu_train = self.df_cumu_train.rolling(5,  center=True).mean()
        print(self.df_cumu_train)
        sns.lineplot(
            data=self.df_cumu_train,
            palette="Set2",
            linewidth=1.5,
            ax=ax,
        )
        ax.set_xticks(np.arange(self.prot_train.shape[0]), self.prot_train.values)
        ax.set_xticklabels(self.prot_train.values, fontsize=9, rotation=90)
        ax.set_ylabel('Total running time (s)', fontsize=18)
        ax.legend(fontsize=12)
        f.subplots_adjust(
            top=0.96,
            bottom=0.18,
            left=0.06,
            right=0.96,
            # hspace=0.40,
            # wspace=0.15
        )
        plt.show()
        return

    def cumuPline(self, ):
        sns.set_theme(style="whitegrid")
        f, ax = plt.subplots(figsize=(10, 4))
        self.df_cumu_previous = self.df_cumu_previous.rolling(5, center=True).mean()
        print(self.df_cumu_previous)
        sns.lineplot(
            data=self.df_cumu_previous,
            palette="Set2",
            linewidth=1.5,
            ax=ax,
        )
        ax.set_xticks(np.arange(self.prot_previous.shape[0]), self.prot_previous.values)
        ax.set_xticklabels(self.prot_previous.values, fontsize=9, rotation=90)
        ax.set_ylabel('Total running time (s)', fontsize=18)
        ax.legend(fontsize=12)
        f.subplots_adjust(
            top=0.96,
            bottom=0.24,
            left=0.08,
            right=0.96,
            # hspace=0.40,
            # wspace=0.15
        )
        plt.show()
        return

    def cumuTline(self, ):
        sns.set_theme(style="whitegrid")
        f, ax = plt.subplots(figsize=(10, 4))
        self.df_cumu_test = self.df_cumu_test.rolling(5, center=True).mean()
        # print(self.df_cumu_test)
        sns.lineplot(
            data=self.df_cumu_test,
            palette="Set2",
            linewidth=1.5,
            ax=ax,
        )
        ax.set_xticks(np.arange(self.prot_test.shape[0]), self.prot_test.values)
        ax.set_xticklabels(self.prot_test.values, fontsize=9, rotation=90)
        ax.set_ylabel('Total running time (s)', fontsize=18)
        ax.legend(fontsize=12)
        f.subplots_adjust(
            top=0.96,
            bottom=0.24,
            left=0.08,
            right=0.96,
            # hspace=0.40,
            # wspace=0.15
        )
        plt.show()
        return

    def stat(self, ):
        print(self.df.loc[self.df['method'] == 'numpy']['pair_number'].sum())
        return


if __name__ == "__main__":
    DEFINE = {
        'protein': {
            'TRAIN': {
                'id': to('data/result/bipartite/tm_alpha_n165/time/protein.txt'),
                'length': to('data/result/bipartite/tm_alpha_n165/time/length.txt'),
                'pair_number': to('data/result/bipartite/tm_alpha_n165/time/pair_number.txt'),
                'window': to('data/result/bipartite/tm_alpha_n165/time/window.txt'),
            },
            'PREVIOUS': {
                'id': to('data/result/bipartite/tm_alpha_n44/time/protein.txt'),
                'length': to('data/result/bipartite/tm_alpha_n44/time/length.txt'),
                'pair_number': to('data/result/bipartite/tm_alpha_n44/time/pair_number.txt'),
                'window': to('data/result/bipartite/tm_alpha_n44/time/window.txt'),
            },
            'TEST': {
                'id': to('data/result/bipartite/tm_alpha_n57/time/protein.txt'),
                'length': to('data/result/bipartite/tm_alpha_n57/time/length.txt'),
                'pair_number': to('data/result/bipartite/tm_alpha_n57/time/pair_number.txt'),
                'window': to('data/result/bipartite/tm_alpha_n57/time/window.txt'),
            },
        },
        'time': {
            'bipartite': {
                'TRAIN': {
                    'pandas': to('data/result/bipartite/tm_alpha_n165/time/total_pandas.txt'),
                    'hash_ori': to('data/result/bipartite/tm_alpha_n165/time/total_hash_ori.txt'),
                    'hash': to('data/result/bipartite/tm_alpha_n165/time/total_hash.txt'),
                },
                'PREVIOUS': {
                    'pandas': to('data/result/bipartite/tm_alpha_n44/time/total_pandas.txt'),
                    'hash_ori': to('data/result/bipartite/tm_alpha_n44/time/total_hash_ori.txt'),
                    'hash': to('data/result/bipartite/tm_alpha_n44/time/total_hash.txt'),
                },
                'TEST': {
                    'pandas': to('data/result/bipartite/tm_alpha_n57/time/total_pandas.txt'),
                    'hash_ori': to('data/result/bipartite/tm_alpha_n57/time/total_hash_ori.txt'),
                    'hash': to('data/result/bipartite/tm_alpha_n57/time/total_hash.txt'),
                }
            },

            'unipartite': {
                'TRAIN': {
                    'numpy': to('data/result/unipartite/tm_alpha_n165/time/total_numpy.txt'),
                    'pandas': to('data/result/unipartite/tm_alpha_n165/time/total_pandas.txt'),
                    'hash_ori': to('data/result/unipartite/tm_alpha_n165/time/total_hash_ori.txt'),
                    'hash': to('data/result/unipartite/tm_alpha_n165/time/total_hash.txt'),
                },
                'PREVIOUS': {
                    'numpy': to('data/result/unipartite/tm_alpha_n44/time/total_numpy.txt'),
                    'pandas': to('data/result/unipartite/tm_alpha_n44/time/total_pandas.txt'),
                    'hash_ori': to('data/result/unipartite/tm_alpha_n44/time/total_hash_ori.txt'),
                    'hash': to('data/result/unipartite/tm_alpha_n44/time/total_hash.txt'),
                },
                'TEST': {
                    'numpy': to('data/result/unipartite/tm_alpha_n57/time/total_numpy.txt'),
                    'pandas': to('data/result/unipartite/tm_alpha_n57/time/total_pandas.txt'),
                    'hash_ori': to('data/result/unipartite/tm_alpha_n57/time/total_hash_ori.txt'),
                    'hash': to('data/result/unipartite/tm_alpha_n57/time/total_hash.txt'),
                }
            },

            'cumulative': {
                'TRAIN': {
                    'L/10': to('data/result/cumulative/tm_alpha_n165/time/total_L10.txt'),
                    'L/5': to('data/result/cumulative/tm_alpha_n165/time/total_L5.txt'),
                    'L/2': to('data/result/cumulative/tm_alpha_n165/time/total_L2.txt'),
                    'L': to('data/result/cumulative/tm_alpha_n165/time/total.txt'),
                    '1.5L': to('data/result/cumulative/tm_alpha_n165/time/total_1.5L.txt'),
                    '2L': to('data/result/cumulative/tm_alpha_n165/time/total_2L.txt'),
                    '5L': to('data/result/cumulative/tm_alpha_n165/time/total_5L.txt'),
                    '10L': to('data/result/cumulative/tm_alpha_n165/time/total_10L.txt'),

                },
                'PREVIOUS': {
                    'L': to('data/result/cumulative/tm_alpha_n44/time/total.txt'),
                },
                'TEST': {
                    'L': to('data/result/cumulative/tm_alpha_n57/time/total.txt'),
                }
            }
        }
    }
    p = plot(
        time_fpns=DEFINE['time'],
        protein_fpns=DEFINE['protein'],
    )
    # print(p.biboxen())
    # print(p.uniboxen())
    # print(p.unibar())
    # print(p.bibar())
    # print(p.hexa())
    # print(p.scatter())
    # print(p.uniheatmap())
    # print(p.biheatmap())
    # print(p.biline())
    # print(p.uniline())
    # print(p.cumuTRAINline())
    # print(p.cumuPline())
    # print(p.cumuTline())
    print(p.stat())