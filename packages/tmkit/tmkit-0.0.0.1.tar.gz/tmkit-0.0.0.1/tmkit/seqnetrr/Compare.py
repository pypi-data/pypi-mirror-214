__author__ = "Jianfeng Sun"
__version__ = "v1.0"
__copyright__ = "Copyright 2023"
__license__ = "GPL v3.0"
__email__ = "jianfeng.sunmt@gmail.com"
__maintainer__ = "Jianfeng Sun"

import time
from tmkit.seqnetrr.Path import to
from tmkit.seqnetrr.window.Pair import pair
from tmkit.seqnetrr.window.Single import single
from tmkit.seqnetrr.util.Reader import reader as prrcreader
from tmkit.seqnetrr.util.Writer import writer as pfwriter
from tmkit.seqnetrr.combo.Length import length as plength
from tmkit.seqnetrr.sequence.Fasta import fasta as sfasta
from tmkit.seqnetrr.combo.Position import position as pfasta
from tmkit.seqnetrr.graph.Bipartite import bipartite as bigraph
from tmkit.seqnetrr.graph.Unipartite import unipartite as unigraph
from tmkit.seqnetrr.graph.Cumulative import cumulative as cumugraph
from tmkit.seqnetrr.util.Console import console


class compare(object):

    def __init__(
            self,
            fasta_path,
            window_size,
            seq_sep_inferior,
            pair_mode='patch',
            mode='hash',
            input_kind='general',
            list_fpn=None,
            fc_path=None,
            sv_fpn=None,
            is_sv=False,
            len_thres=500,
            verbose=True,
    ):
        self.sv_fpn = sv_fpn
        self.pfreader = prrcreader()
        self.pfwriter = pfwriter()
        self.console = console()
        self.console.verbose = verbose
        self.is_sv = is_sv
        self.fc_path = fc_path
        self.seq_sep_inferior = seq_sep_inferior
        self.pair_mode = pair_mode
        self.mode = mode
        self.len_thres = len_thres
        self.input_kind = input_kind
        self.window_size = window_size
        self.prot_df = self.pfreader.generic(list_fpn)
        self.prot_df['len_seq'] = -1
        for i in self.prot_df.index:
            prot_name = self.prot_df.iloc[i, 0]
            file_chain = self.chain(self.prot_df.iloc[i, 1])
            sequence = sfasta().get(
                fasta_fpn=fasta_path + prot_name + file_chain + '.fasta',
            )
            # print(sequence)
            self.prot_df.loc[i, 'seq'] = sequence
            self.prot_df.loc[i, 'len_seq'] = len(sequence)
        self.prot_df = self.prot_df.loc[self.prot_df['len_seq'] < len_thres].reset_index(drop=True)
        self.console.print('Sequence separation inf: {}'.format(self.seq_sep_inferior))
        self.console.print('Length thres: {}'.format(self.len_thres))
        self.console.print('Window size: {}'.format(self.window_size))
        self.console.print('Input kind: {}'.format(self.input_kind))
        self.console.print('\n{}'.format(self.prot_df))
        self.console.print(self.prot_df.shape)

    def chain(self, prot_chain):
        return str(prot_chain) + 'l' if str(prot_chain).islower() else str(prot_chain)

    def unipartite(self, mode):
        self.console.print('Mode: {}'.format(mode))
        for i in self.prot_df.index:
            stime = time.time()
            sequence = self.prot_df.loc[i, 'seq']
            prot_name = self.prot_df.iloc[i, 0]
            file_chain = self.chain(self.prot_df.iloc[i, 1])
            self.console.print('===>ID.{}'.format(i))
            self.console.print('===>protein: {}'.format(prot_name + file_chain))
            self.console.print('===>protein length: {}'.format(self.prot_df.loc[i, 'len_seq']))
            # /* scenario of position */
            pos_list = plength(seq_sep_inferior=self.seq_sep_inferior).topair(len(sequence))
            self.console.print('===>pair number: {}'.format(len(pos_list)))

            # /* position */
            position = pfasta(sequence).pair(pos_list=pos_list)

            # /* window */
            window_m_ids = pair(
                sequence=sequence,
                position=position,
                window_size=self.window_size,
            ).mid()

            p = unigraph(
                sequence=sequence,
                window_size=self.window_size,
                window_m_ids=window_m_ids,
                input_kind=self.input_kind,
            )
            # /* local ec scores */
            list_2d = position
            p.assign(
                fpn=self.fc_path + prot_name + file_chain + '.evfold',
                list_2d=list_2d,
                mode=mode,
            )
            self.console.print('===>total time: {time}s.'.format(time=time.time() - stime))
            # print(vec)

    def bipartite(self, pair_mode, mode):
        self.console.print('Pair mode: {}'.format(pair_mode))
        self.console.print('Mode: {}'.format(mode))
        for i in self.prot_df.index:
            stime = time.time()
            sequence = self.prot_df.loc[i, 'seq']
            prot_name = self.prot_df.iloc[i, 0]
            file_chain = self.chain(self.prot_df.iloc[i, 1])
            self.console.print('===>ID.{}'.format(i))
            self.console.print('===>protein: {}'.format(prot_name + file_chain))
            self.console.print('===>protein length: {}'.format(self.prot_df.loc[i, 'len_seq']))
            # /* scenario of position */
            pos_list = plength(seq_sep_inferior=self.seq_sep_inferior).topair(len(sequence))
            self.console.print('===>pair number: {}'.format(len(pos_list)))

            # /* position */
            position = pfasta(sequence).pair(pos_list=pos_list)

            # /* window */
            window_m_ids = pair(
                sequence=sequence,
                position=position,
                window_size=self.window_size,
            ).mid()

            p = bigraph(
                sequence=sequence,
                window_size=self.window_size,
                window_m_ids=window_m_ids,
                kind=pair_mode,
                patch_size=2,
                input_kind=self.input_kind,
            )
            # /* global ec scores */
            list_2d = position
            p.assign(
                fpn=self.fc_path + prot_name + file_chain + '.evfold',
                list_2d=list_2d,
                mode=mode,
            )
            self.console.print('===>total time: {time}s.'.format(time=time.time() - stime))
            # print(vec)

    def cumulative(self, cumu_ratio=0.5):
        self.console.print('cumulative ratio: {}'.format(cumu_ratio))
        for i in self.prot_df.index:
            stime = time.time()
            sequence = self.prot_df.loc[i, 'seq']
            prot_name = self.prot_df.iloc[i, 0]
            file_chain = self.chain(self.prot_df.iloc[i, 1])
            self.console.print('===>ID.{}'.format(i))
            self.console.print('===>protein: {}'.format(prot_name + file_chain))
            self.console.print('===>protein length: {}'.format(self.prot_df.loc[i, 'len_seq']))
            # /* scenario of position */
            pos_list = plength(seq_sep_inferior=self.seq_sep_inferior).tosgl(len(sequence))
            self.console.print('===>pair number: {}'.format(len(pos_list)))

            # /* position */
            position = pfasta(sequence).single(pos_list=pos_list)

            # /* window */
            window_m_ids = single(
                sequence=sequence,
                position=position,
                window_size=self.window_size,
            ).mid()

            p = cumugraph(
                sequence=sequence,
                window_size=self.window_size,
                window_m_ids=window_m_ids,
                input_kind=self.input_kind,
            )
            # /* global ec scores */
            list_2d = position
            p.assign(
                list_2d=list_2d,
                fpn=self.fc_path + prot_name + file_chain + '.evfold',
                L=int(len(sequence) * cumu_ratio),
                simu_seq_len=None,
            )
            self.console.print('===>total time: {time}s.'.format(time=time.time() - stime))
            # print(vec)


if __name__ == "__main__":
    DEFINE = {
        # 'list_fpn': to('data/rrc/tm_alpha_n165/fasta/prot_n165.txt'),
        # 'fasta_path': to('data/rrc/tm_alpha_n165/fasta/'),
        # 'fc_path': to('data/rrc/tm_alpha_n165/freecontact/'),

        # 'list_fpn': to('data/rrc/tm_alpha_n44/fasta/prot_n44.txt'),
        # 'fasta_path': to('data/rrc/tm_alpha_n44/fasta/'),
        # 'fc_path': to('data/rrc/tm_alpha_n44/freecontact/'),

        'list_fpn': to('data/rrc/tm_alpha_n57/fasta/prot_n57.txt'),
        'fasta_path': to('data/rrc/tm_alpha_n57/fasta/'),
        'fc_path': to('data/rrc/tm_alpha_n57/freecontact/'),

        'window_size': 2,
        'seq_sep_inferior': 0,
    }
    p = compare(
        fasta_path=DEFINE['fasta_path'],
        list_fpn=DEFINE['list_fpn'],
        fc_path=DEFINE['fc_path'],
        window_size=DEFINE['window_size'],
        seq_sep_inferior=DEFINE['seq_sep_inferior'],
        verbose=True,

        # input_kind='general',
        input_kind='freecontact',
        # input_kind='simulate',
    )

    print(p.unipartite(
        # mode='hash_rl',
        # mode='hash_ori',
        # mode='hash',
        # mode='pandas',
        mode='numpy',
    ))

    # print(p.bipartite(
    #     pair_mode='patch',
    #     # pair_mode='cross',
    #     # pair_mode='memconp',
    #     # pair_mode='unchanged',
    #
    #     # mode='hash_rl',
    #     # mode='hash_ori',
    #     # mode='hash',
    #     mode='pandas',
    #     # mode='numpy',
    # ))

    # print(p.cumulative(
    #     cumu_ratio=1,
    # ))