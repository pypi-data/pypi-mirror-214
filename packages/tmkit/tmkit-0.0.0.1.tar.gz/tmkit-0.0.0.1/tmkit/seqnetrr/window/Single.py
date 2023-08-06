__author__ = "Jianfeng Sun"
__version__ = "v1.0"
__copyright__ = "Copyright 2023"
__license__ = "GPL v3.0"
__email__ = "jianfeng.sunmt@gmail.com"
__maintainer__ = "Jianfeng Sun"

import time
from tmkit.seqnetrr.Path import to
from tmkit.seqnetrr.util.Console import console


class single():
    """
    Methods
    -------
       mid(), mname(), bipartite(), make().

    Notes
    -----
       window class offers methods to perform a sliding window op for each of central
       residue pairs for a given sequence.

    See Also
    --------
       It was introduced since v1.0.
       Change Log:
       1>. It has been revised since the end of June, 2018.
       2>. It has been revised since Oct. 10th, 2018.

    """

    def __init__(
            self,
            sequence,
            position,
            window_size,
            verbose=True,
    ):
        self.sequence = sequence
        self.m_sgls = position
        self.window_size = window_size
        self.len_seq = len(self.sequence)
        self.console = console()
        self.console.verbose = verbose

    def mid(self):
        """

        Notes
        -----
           mid() gets all of residues around central residues with a window size.

        Methods
        -------
           > This function generates all residues with a sliding window for all pairs being in
             contact or not. The ensemble of final data doesn't include the pair residues
             themselves, which means
             [al1, al2, al3, ar1, ar2, ar3, bl1, bl2, bl3, br1, br2, br3]
             for one pair a and b (the 2 dimension of the dataset) but please notice that it
             does not include a and b themselves inside.
           > block 1: assigning central residues to residues around them.
           > block 2: assigning only None for window_m_id.

        See Also
        --------
           It was introduced since v1.0.
           Change Log:
           1>. It has been revised since the end of June, 2018.
           2>. It has been revised since Oct. 10th, 2018.

        Returns
        -------
            oder number of pairs and name of pairs.

        """
        start_time = time.time()
        num_m = len(self.m_sgls)
        window_m_id = [[] for _ in range(num_m)]
        # #/*** block 1 ***/
        for i in range(num_m):
            for index_left in range(self.window_size):
                window_m_id[i].append(self.m_sgls[i][0] - (self.window_size - index_left))
            window_m_id[i].append(self.m_sgls[i][0])
            for index_right in range(self.window_size):
                window_m_id[i].append(self.m_sgls[i][0] + (index_right + 1))
        # print(window_m_id)
        # #/*** block 2 ***/
        for i in range(len(window_m_id)):
            for j in range(len(window_m_id[0])):
                if window_m_id[i][j] < 1 or window_m_id[i][j] > len(self.sequence):
                    window_m_id[i][j] = None
        # print(window_m_id)
        self.console.print('=========>Window molecule generation: {time}s.'.format(time=time.time() - start_time))
        return window_m_id

    def mname(self, m_idices):
        """

        Notes
        -----
           mname() gets all residues names corresponding to mid().

        Methods
        -------
           It will assgin residues in the window with amino acids name and assign residues
           in the window but beyond the sequence boundary with None.

        See Also
        --------
           what kind of residues and how many residues the window includes, see method
           mid().

        References
        ----------
           It was introduced since v1.0.
           Change Log:
           1>. It has been revised since the end of June, 2018.
           2>. It has been revised since Oct. 10th, 2018.

        Parameters
        ----------
        m_idices

        Returns
        -------
            2d array (list)

        """
        num_m = len(m_idices)
        window_m_name = [[] for _ in range(num_m)]
        for i in range(len(m_idices)):
            for j in range(len(m_idices[0])):
                if m_idices[i][j] is None:
                    window_m_name[i].append(None)
                # print(window_m_name)
                for k, character in enumerate(self.sequence):
                    if m_idices[i][j] == k + 1:
                        # print(character)
                        window_m_name[i].append(character)
        # print(len(m_idices), len(window_m_name[92]))
        return window_m_name


if __name__ == "__main__":
    from tmkit.seqnetrr.sequence.Fasta import fasta as sfasta
    from tmkit.seqnetrr.combo.Position import position as pfasta
    from tmkit.seqnetrr.combo.Length import length as plength

    DEFINE = {
        'prot_name': '1aig',
        'file_chain': 'L',
        'seq_chain': 'L',

        # 'prot_name': '5lki',
        # 'file_chain': 'A',
        # 'seq_chain': 'A',

        'cutoff': 5.5,
        'seq_sep_inferior': 4,
        'seq_sep_superior': None,
        'fasta_path': to('data/example/'),
    }

    # /* sequence */
    fasta_path = to('data/example/1aigL.fasta')
    sequence = sfasta().get(fasta_path)
    print(sequence)

    # /* scenario of position */
    pos_list = plength(seq_sep_inferior=0).tosgl(len(sequence))
    print(pos_list)

    # /* position */
    position = pfasta(sequence).single(pos_list=pos_list)
    print(position)

    window_size = 2
    window_m_ids = single(
        sequence=sequence,
        position=position,
        window_size=window_size,
    ).mid()
    print(window_m_ids)

