###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

import numpy as np
import pandas as pd
from sciutil import SciUtil, SciException
import matplotlib.pyplot as plt


class SciRCMException(SciException):
    def __init__(self, message=''):
        Exception.__init__(self, message)

"""
Sci-RCM is the logical regulatory clustering of genes based on DNA-methylation, RNA-seq and Proteomics data.
"""


class SciRCM:

    def __init__(self, meth_file: str,
                 rna_file: str,
                 proteomics_file: str,
                 rna_logfc: str,
                 rna_padj: str,
                 meth_diff: str,
                 meth_padj: str,
                 prot_logfc: str,
                 prot_padj: str,
                 gene_id: str,
                 rna_padj_cutoff=0.05,
                 prot_padj_cutoff=0.05,
                 meth_padj_cutoff=0.05,
                 rna_logfc_cutoff=1.0,
                 prot_logfc_cutoff=0.5,
                 meth_diff_cutoff=10,
                 output_dir='.',
                 output_filename=None,
                 non_coding_genes=None,
                 debug_on=False, sep=',',
                 bg_type='P&R',
                 sciutil=None,
                 logfile=None,
                 reg_grp_1_lbl='RG1_All',
                 reg_grp_2_lbl='RG2_Changes',
                 reg_grp_3_lbl='RG3_Translation',
                 main_reg_label='RG2_Changes',
                 reg_grp_4_lbl='RG4_Detection', check_inputs=True):
        self.u = SciUtil() if sciutil is None else sciutil
        plt.rcParams['svg.fonttype'] = 'none'
        self.meth_diff = meth_diff
        self.merged_df = None
        self.prot_logfc = prot_logfc
        self.rna_logfc = rna_logfc
        self.rna_padj = rna_padj
        self.meth_padj = meth_padj
        self.prot_padj = prot_padj
        self.gene_id = gene_id
        self.logfile = open(logfile, "w+") if logfile is not None else None  # File for logging results
        self.rna_padj_cutoff, self.meth_padj_cutoff, self.prot_padj_cutoff = rna_padj_cutoff, meth_padj_cutoff, prot_padj_cutoff
        self.rna_logfc_cutoff, self.meth_diff_cutoff, self.prot_logfc_cutoff = rna_logfc_cutoff, meth_diff_cutoff, prot_logfc_cutoff
        self.debug = debug_on
        self.output_dir = output_dir
        self.reg_grp_1_lbl = reg_grp_1_lbl
        self.reg_grp_2_lbl = reg_grp_2_lbl
        self.reg_grp_3_lbl = reg_grp_3_lbl
        self.reg_grp_4_lbl = reg_grp_4_lbl
        self.main_reg_label = main_reg_label
        if check_inputs:
            if main_reg_label != reg_grp_2_lbl and main_reg_label != reg_grp_1_lbl and main_reg_label != reg_grp_3_lbl:
                self.u.err_p([f'ERROR: your main regulatory label (main_reg_label) must be one of: '
                              f'{reg_grp_1_lbl}, {reg_grp_2_lbl} or {reg_grp_3_lbl}, you passed: ', main_reg_label])
            # Otherwise this will be in the specific ones.
            if prot_logfc and rna_logfc and meth_diff:
                self.output_filename = output_filename if output_filename else f'scircm_r{rna_logfc_cutoff}-{rna_padj_cutoff}' \
                                                                           f'_p{prot_logfc_cutoff}-{prot_padj_cutoff}' \
                                                                           f'_m{meth_diff_cutoff}-{meth_padj_cutoff}.csv'
                if isinstance(meth_file, str):
                    self.meth_df = pd.read_csv(meth_file, sep=sep)
                    self.rna_df = pd.read_csv(rna_file, sep=sep)
                    self.prot_df = pd.read_csv(proteomics_file, sep=sep)
                else:
                    self.meth_df = meth_file
                    self.rna_df = rna_file
                    self.prot_df = proteomics_file
            self.bg_list = ['(P&M)|(P&R)', '(P&M)|(P&R)|(M&R)', '*', 'P&M&R', 'P|M|R', 'P|R', 'P&R',
                            'P|(M&R)']
            if bg_type not in self.bg_list:
                self.u.err_p(['ERROR: selected background type was not allowed, please choose from one of: ', self.bg_list,
                              '\n Note: | means OR and & means AND'])
            else:
                self.bg_type = bg_type

        self.non_coding_genes = non_coding_genes
        # Contains genes for the non-coding region (use for human only).
        self.df = None
        # Contains the vae data
        self.vae = None

    def run(self):
        # First check for duplicates in IDs and drop if there are any
        if len(self.prot_df[self.prot_df[self.gene_id].duplicated()]) > 0:
            num_dups = len(self.prot_df[self.prot_df[self.gene_id].duplicated()])
            self.u.warn_p(['Protein dataset contained duplicates based on ID! Dropping duplicate IDs,'
                           ' note you should do this '
                           'before running SiRCle. We have just dropped it and kept the first entry. You had: ',
                           num_dups, 'duplicates.'])
            self.prot_df = self.prot_df[~self.prot_df[self.gene_id].duplicated(keep='first')]
        if len(self.rna_df[self.rna_df[self.gene_id].duplicated()]) > 0:
            num_dups = len(self.rna_df[self.rna_df[self.gene_id].duplicated()])
            self.u.warn_p(['RNAseq dataset contained duplicates based on ID! Dropping duplicate IDs,'
                           ' note you should do this '
                           'before running SiRCle. We have just dropped it and kept the first entry. You had: ',
                           num_dups, 'duplicates.'])
            self.rna_df = self.rna_df[~self.rna_df[self.gene_id].duplicated(keep='first')]
        if len(self.meth_df[self.meth_df[self.gene_id].duplicated()]) > 0:
            num_dups = len(self.meth_df[self.meth_df[self.gene_id].duplicated()])
            self.u.warn_p(['Methylation dataset contained duplicates based on ID! Dropping duplicate IDs,'
                           ' note you should do this '
                           'before running SiRCle. We have just dropped it and kept the first entry. You had: ',
                           num_dups, 'duplicates.'])
            self.meth_df = self.meth_df[~self.meth_df[self.gene_id].duplicated(keep='first')]

        # Merge the dataframes together
        self.merge_dfs()

        # Calculate groups
        self.run_rcm()

        # Save the DF and return the groupings
        return self.df

    def merge_dfs(self):
        """
        Merge the supplied RNAseq, DNA methylation and proteomics dataframes together. We do an outer join. This can
        result in gene identifiers becoming disjoint (i.e. if there are two ensembl ID columns, we get two now).
        """
        self.rna_df = self.rna_df.set_index(self.gene_id)
        self.df = self.rna_df.merge(self.meth_df, on=self.gene_id, how='outer', suffixes=['_r', '_m'])
        self.df = self.df.merge(self.prot_df, on=self.gene_id, how='outer', suffixes=['', '_p'])
        # Fill the rest of the values with 0's
        self.merged_df = self.df.copy()

    def run_rcm(self, methylation_background=1.0, rna_background=1.0, protein_background=1.0):
        protein_padjs = self.df[self.prot_padj].values
        protein_logfcs = self.df[self.prot_logfc].values
        rna_padjs = self.df[self.rna_padj].values
        rna_logfcs = self.df[self.rna_logfc].values
        meth_padjs = self.df[self.meth_padj].values
        meth_diffs = self.df[self.meth_diff].values
        reg_label_1, reg_label_2, reg_label_4, reg_label_3 = [], [], [], []
        background_filter = []
        for i, gene in enumerate(self.df[self.gene_id].values):
            meth_diff = meth_diffs[i]
            meth_padj = meth_padjs[i]
            rna_logfc = rna_logfcs[i]
            rna_padj = rna_padjs[i]
            prot_logfc = protein_logfcs[i]
            prot_padj = protein_padjs[i]

            methylation_state, rna_state, protein_state = None, None, None
            methylation_bg, rna_bg, protein_bg = None, None, None
            if ~np.isnan(meth_diff) and meth_diff > self.meth_diff_cutoff and meth_padj < self.meth_padj_cutoff:
                methylation_state = 'Hypermethylation'
                methylation_bg = 'threshold'
            elif ~np.isnan(meth_diff) and meth_diff < (-1 * self.meth_diff_cutoff) and meth_padj < self.meth_padj_cutoff:
                methylation_state = 'Hypomethylation'
                methylation_bg = 'threshold'
            else:
                methylation_state = 'Methylation No change'
                if np.isnan(meth_padj):
                    methylation_bg = 'NS'
                elif meth_padj < methylation_background:
                    methylation_bg = 'threshold'
                else:
                    methylation_bg = 'NS'

            if ~np.isnan(rna_logfc) and rna_logfc > self.rna_logfc_cutoff and rna_padj < self.rna_padj_cutoff:
                rna_state = 'RNA UP'
                rna_bg = 'threshold'
            elif ~np.isnan(rna_logfc) and rna_logfc < (- 1 * self.rna_logfc_cutoff) and rna_padj < self.rna_padj_cutoff:
                rna_state = 'RNA DOWN'
                rna_bg = 'threshold'
            else:
                rna_state = 'RNA No change'
                if np.isnan(rna_padj):
                    rna_bg = 'NS'
                elif rna_padj < rna_background:
                    rna_bg = 'threshold'
                else:
                    rna_bg = 'NS'

            if ~np.isnan(prot_logfc) and prot_logfc > self.prot_logfc_cutoff and prot_padj < self.prot_padj_cutoff:
                protein_state = 'Protein UP'
                protein_bg = 'threshold'
            elif ~np.isnan(prot_logfc) and prot_logfc < (- 1 * self.prot_logfc_cutoff) and prot_padj < self.prot_padj_cutoff:
                protein_state = 'Protein DOWN'
                protein_bg = 'threshold'
            elif ~np.isnan(prot_logfc) and prot_logfc < 0 and prot_padj < self.prot_padj_cutoff:  # i.e. sig down but no threshold
                protein_state = 'Protein significant-negative'
                protein_bg = 'threshold'
            elif ~np.isnan(prot_logfc) and prot_logfc > 0 and prot_padj < self.prot_padj_cutoff:  # i.e. sig up but no threshold
                protein_state = 'Protein significant-positive'
                protein_bg = 'threshold'
            # Add in a not-detected state
            elif np.isnan(prot_logfc):
                protein_state = 'Protein Undetected'
                protein_bg = 'NS'
            else:
                protein_state = 'Protein not-significant'
                if prot_padj < protein_background:
                    protein_bg = 'threshold'
                else:
                    protein_bg = 'NS'

            background = f'{methylation_bg} + {rna_bg} + {protein_bg}'
            background_filter.append(background)
            state_label = f'{methylation_state} + {rna_state} + {protein_state}'

            if state_label == 'Hypermethylation + RNA DOWN + Protein DOWN':  # State 1
                reg_label_2.append('MDS')
                reg_label_3.append('MDS')
                reg_label_4.append('MDS')
            elif state_label == 'Hypermethylation + RNA No change + Protein DOWN':  # State 2
                reg_label_2.append('TMDS')
                reg_label_3.append('TMDS')
                reg_label_4.append('TMDS')
            elif state_label == 'Hypermethylation + RNA UP + Protein DOWN':  # State 3
                reg_label_2.append('TPDE_TMDS')
                reg_label_3.append('TMDS')
                reg_label_4.append('TPDE_TMDS')

            elif state_label == 'Hypermethylation + RNA DOWN + Protein Undetected':  # State 7
                reg_label_2.append('MDS_TMDE')
                reg_label_3.append('MDS')
                reg_label_4.append('MDS')
            elif state_label == 'Hypermethylation + RNA No change + Protein Undetected':  # State 8
                reg_label_2.append('None')  # This would only be included if we have the non-coding groups
                reg_label_3.append('None')
                reg_label_4.append('None')
            elif state_label == 'Hypermethylation + RNA UP + Protein Undetected':  # State 9
                reg_label_2.append('TPDE_TMDS')
                reg_label_3.append('TPDE')
                reg_label_4.append('TPDE')

            elif state_label == 'Hypermethylation + RNA DOWN + Protein not-significant':  # State 4
                reg_label_2.append('MDS_TMDE')
                reg_label_3.append('None')
                reg_label_4.append('MDS_TMDE')
            elif state_label == 'Hypermethylation + RNA No change + Protein not-significant':  # State 5
                reg_label_2.append('None')  # This would only be included if we have the non-coding groups
                reg_label_3.append('None')
                reg_label_4.append('None')
            elif state_label == 'Hypermethylation + RNA UP + Protein not-significant':  # State 6
                reg_label_2.append('TPDE_TMDS')
                reg_label_3.append('None')
                reg_label_4.append('TPDE_TMDS')

            elif state_label == 'Hypermethylation + RNA DOWN + Protein significant-negative':  # State 10
                reg_label_2.append('MDS_TMDE')
                reg_label_3.append('MDS')
                reg_label_4.append('MDS')
            elif state_label == 'Hypermethylation + RNA No change + Protein significant-negative':  # State 11
                reg_label_2.append('None')
                reg_label_3.append('None')
                reg_label_4.append('None')
            elif state_label == 'Hypermethylation + RNA UP + Protein significant-negative':  # State 12
                reg_label_2.append('TPDE_TMDS')
                reg_label_3.append('TMDS')
                reg_label_4.append('TPDE_TMDS')

            elif state_label == 'Hypermethylation + RNA DOWN + Protein significant-positive':  # State 10
                reg_label_2.append('MDS_TMDE')
                reg_label_3.append('TMDE')
                reg_label_4.append('MDS_TMDE')
            elif state_label == 'Hypermethylation + RNA No change + Protein significant-positive':  # State 11
                reg_label_2.append('None')
                reg_label_3.append('None')
                reg_label_4.append('None')
            elif state_label == 'Hypermethylation + RNA UP + Protein significant-positive':  # State 12
                reg_label_2.append('TPDE_TMDS')
                reg_label_3.append('TPDE')
                reg_label_4.append('TPDE')

            elif state_label == 'Hypermethylation + RNA DOWN + Protein UP':  # State 10
                reg_label_2.append('MDS_TMDE')
                reg_label_3.append('TMDE')
                reg_label_4.append('MDS_TMDE')
            elif state_label == 'Hypermethylation + RNA No change + Protein UP':  # State 11
                reg_label_2.append('TMDE')
                reg_label_3.append('TMDE')
                reg_label_4.append('TMDE')
            elif state_label == 'Hypermethylation + RNA UP + Protein UP':  # State 12
                reg_label_2.append('TPDE')
                reg_label_3.append('TPDE')
                reg_label_4.append('TPDE')

            # The same for hypomethylation
            elif state_label == 'Hypomethylation + RNA DOWN + Protein DOWN':  # State 13
                reg_label_2.append('TPDS')
                reg_label_3.append('TPDS')
                reg_label_4.append('TPDS')
            elif state_label == 'Hypomethylation + RNA No change + Protein DOWN':  # State 14
                reg_label_2.append('TMDS')
                reg_label_3.append('TMDS')
                reg_label_4.append('TMDS')
            elif state_label == 'Hypomethylation + RNA UP + Protein DOWN':  # State 15
                reg_label_2.append('MDE_TMDS')
                reg_label_3.append('TMDS')
                reg_label_4.append('MDE_TMDS')


            elif state_label == 'Hypomethylation + RNA DOWN + Protein Undetected':  # State 22
                reg_label_2.append('TPDS_TMDE')
                reg_label_3.append('TPDS')
                reg_label_4.append('TPDS_TMDE')
            elif state_label == 'Hypomethylation + RNA No change + Protein Undetected':  # State 23
                reg_label_2.append('None')  # This would only be included if we have the non-coding groups
                reg_label_3.append('None')
                reg_label_4.append('None')
            elif state_label == 'Hypomethylation + RNA UP + Protein Undetected':  # State 24
                reg_label_2.append('MDE_TMDS')
                reg_label_3.append('MDE')
                reg_label_4.append('MDE')

            elif state_label == 'Hypomethylation + RNA DOWN + Protein not-significant':  # State 16
                reg_label_2.append('TPDS_TMDE')
                reg_label_3.append('None')
                reg_label_4.append('TPDS_TMDE')
            elif state_label == 'Hypomethylation + RNA No change + Protein not-significant':  # State 17
                reg_label_2.append('None')  # This would only be included if we have the non-coding groups
                reg_label_3.append('None')
                reg_label_4.append('None')
            elif state_label == 'Hypomethylation + RNA UP + Protein not-significant':  # State 18
                reg_label_2.append('MDE_TMDS')
                reg_label_3.append('None')
                reg_label_4.append('MDE_TMDS')

            elif state_label == 'Hypomethylation + RNA DOWN + Protein significant-negative':  # State 13
                reg_label_2.append('TPDS_TMDE')
                reg_label_3.append('TPDS')
                reg_label_4.append('TPDS')
            elif state_label == 'Hypomethylation + RNA No change + Protein significant-negative':  # State 14
                reg_label_2.append('None')
                reg_label_3.append('None')
                reg_label_4.append('None')
            elif state_label == 'Hypomethylation + RNA UP + Protein significant-negative':  # State 15
                reg_label_2.append('MDE_TMDS')
                reg_label_3.append('TMDS')
                reg_label_4.append('MDE_TMDS')

            elif state_label == 'Hypomethylation + RNA DOWN + Protein significant-positive':
                reg_label_2.append('TPDS_TMDE')
                reg_label_3.append('TMDE')
                reg_label_4.append('TPDS_TMDE')
            elif state_label == 'Hypomethylation + RNA No change + Protein significant-positive':  # State 14
                reg_label_2.append('None')
                reg_label_3.append('None')
                reg_label_4.append('None')
            elif state_label == 'Hypomethylation + RNA UP + Protein significant-positive':  # State 15
                reg_label_2.append('MDE_TMDS')
                reg_label_3.append('MDE')
                reg_label_4.append('MDE')

            elif state_label == 'Hypomethylation + RNA DOWN + Protein UP':  # State 19
                reg_label_2.append('TPDS_TMDE')
                reg_label_3.append('TMDE')
                reg_label_4.append('TPDS_TMDE')
            elif state_label == 'Hypomethylation + RNA No change + Protein UP':  # State 20
                reg_label_2.append('TMDE')
                reg_label_3.append('TMDE')
                reg_label_4.append('TMDE')
            elif state_label == 'Hypomethylation + RNA UP + Protein UP':  # State 21
                reg_label_2.append('MDE')
                reg_label_3.append('MDE')
                reg_label_4.append('MDE')

            # Same for no-change
            elif state_label == 'Methylation No change + RNA DOWN + Protein DOWN':  # State 25
                reg_label_2.append('TPDS')
                reg_label_3.append('TPDS')
                reg_label_4.append('TPDS')
            elif state_label == 'Methylation No change + RNA No change + Protein DOWN':  # State 26
                reg_label_2.append('TMDS')
                reg_label_3.append('TMDS')
                reg_label_4.append('TMDS')
            elif state_label == 'Methylation No change + RNA UP + Protein DOWN':  # State 27
                reg_label_2.append('TPDE_TMDS')
                reg_label_3.append('TMDS')
                reg_label_4.append('TPDE_TMDS')

            elif state_label == 'Methylation No change + RNA DOWN + Protein Undetected':  # State 31
                reg_label_2.append('TPDS_TMDE')
                reg_label_3.append('TPDS')
                reg_label_4.append('TPDS')
            elif state_label == 'Methylation No change + RNA No change + Protein Undetected':  # State 32
                reg_label_2.append('None')  # This would only be included if we have the non-coding groups
                reg_label_3.append('None')
                reg_label_4.append('None')
            elif state_label == 'Methylation No change + RNA UP + Protein Undetected':  # State 33
                reg_label_2.append('TPDE_TMDS')
                reg_label_3.append('TPDE')
                reg_label_4.append('TPDE')

            elif state_label == 'Methylation No change + RNA DOWN + Protein not-significant':  # State 28
                reg_label_2.append('TPDS_TMDE')
                reg_label_3.append('None')
                reg_label_4.append('TPDS_TMDE')
            elif state_label == 'Methylation No change + RNA No change + Protein not-significant':  # State 29
                reg_label_2.append('None')  # This would only be included if we have the non-coding groups
                reg_label_3.append('None')
                reg_label_4.append('None')
            elif state_label == 'Methylation No change + RNA UP + Protein not-significant':  # State 30
                reg_label_2.append('TPDE_TMDS')
                reg_label_3.append('None')
                reg_label_4.append('TPDE_TMDS')

            elif state_label == 'Methylation No change + RNA DOWN + Protein significant-negative':  # State 25
                reg_label_2.append('TPDS_TMDE')
                reg_label_3.append('TPDS')
                reg_label_4.append('TPDS')
            elif state_label == 'Methylation No change + RNA No change + Protein significant-negative':  # State 26
                reg_label_2.append('None')
                reg_label_3.append('None')
                reg_label_4.append('None')
            elif state_label == 'Methylation No change + RNA UP + Protein significant-negative':  # State 27
                reg_label_2.append('TPDE_TMDS')
                reg_label_3.append('TMDS')
                reg_label_4.append('TPDE_TMDS')

            elif state_label == 'Methylation No change + RNA DOWN + Protein significant-positive':  # State 34
                reg_label_2.append('TPDS_TMDE')
                reg_label_3.append('TMDE')
                reg_label_4.append('TPDS_TMDE')
            elif state_label == 'Methylation No change + RNA No change + Protein significant-positive':  # State 35
                reg_label_2.append('None')
                reg_label_3.append('None')
                reg_label_4.append('None')
            elif state_label == 'Methylation No change + RNA UP + Protein significant-positive':  # State 36
                reg_label_2.append('TPDE_TMDS')
                reg_label_3.append('TPDE')
                reg_label_4.append('TPDE')

            elif state_label == 'Methylation No change + RNA DOWN + Protein UP':  # State 34
                reg_label_2.append('TPDS_TMDE')
                reg_label_3.append('TMDE')
                reg_label_4.append('TPDS_TMDE')
            elif state_label == 'Methylation No change + RNA No change + Protein UP':  # State 35
                reg_label_2.append('TMDE')
                reg_label_3.append('TMDE')
                reg_label_4.append('TMDE')
            elif state_label == 'Methylation No change + RNA UP + Protein UP':  # State 36
                reg_label_2.append('TPDE')
                reg_label_3.append('TPDE')
                reg_label_4.append('TPDE')

            else:
                reg_label_2.append('None')
                reg_label_3.append('None')
                reg_label_4.append('None')
            # Add the reg group 1
            reg_label_1.append(state_label)

        # Now we want to make three new columns that define the states of methylation RNA and protein
        self.df['Methylation'] = [s if s == 'None' else s.split(' + ')[0] for s in reg_label_1]
        self.df['RNA'] = [s if s == 'None' else s.split(' + ')[1] for s in reg_label_1]
        self.df['Protein'] = [s if s == 'None' else s.split(' + ')[2] for s in reg_label_1]

        self.df[self.reg_grp_1_lbl] = reg_label_1
        self.df[self.reg_grp_2_lbl] = reg_label_2
        self.df[self.reg_grp_3_lbl] = reg_label_3
        self.df[self.reg_grp_4_lbl] = reg_label_4

        self.df['Background_filter'] = background_filter
        # For each of the regulatory labels, apply the background filter depending on what the user chose
        self.apply_bg_filter()

    def apply_bg_filter(self):
        bg_type = self.bg_type
        bg = self.df['Background_filter'].values
        if bg_type == 'P|(M&R)':  # Protein AND (DNA methylation OR RNA)
            conds = ['threshold + threshold + NS',  # RNA & Methylation ~Protein
                     'threshold + threshold + threshold',  # RNA & Methylation & Protein
                     'threshold + NS + threshold',  # Methylation ~ RNA & protein
                     'NS + NS + threshold',  # Just protein
                     'NS + threshold + threshold',  # ~ methylation RNA Protein
                     ]
            self.df[f'{self.reg_grp_1_lbl}_filtered'] = [c if bg[i] in conds else 'Not-Background' for i, c in enumerate(self.df[self.reg_grp_1_lbl].values)]
            self.df[f'{self.reg_grp_2_lbl}_filtered'] = [c if bg[i] in conds else 'Not-Background' for i, c in enumerate(self.df[self.reg_grp_2_lbl].values)]
            self.df[f'{self.reg_grp_3_lbl}_filtered'] = [c if bg[i] in conds else 'Not-Background' for i, c in enumerate(self.df[self.reg_grp_3_lbl].values)]
            self.df[f'{self.reg_grp_4_lbl}_filtered'] = [c if bg[i] in conds else 'Not-Background' for i, c in enumerate(self.df[self.reg_grp_4_lbl].values)]

        elif bg_type == 'P|M|R':  # Protein OR methylation OR RNA
            conds = ['NS + NS + NS']  # i.e. only one we don't want is NS
            self.df[f'{self.reg_grp_1_lbl}_filtered'] = [c if bg[i] not in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_1_lbl].values)]
            self.df[f'{self.reg_grp_2_lbl}_filtered'] = [c if bg[i] not in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_2_lbl].values)]
            self.df[f'{self.reg_grp_3_lbl}_filtered'] = [c if bg[i] not in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_3_lbl].values)]
            self.df[f'{self.reg_grp_4_lbl}_filtered'] = [c if bg[i] not in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_4_lbl].values)]

        elif bg_type == 'P|R':  # Protein OR RNA
            conds = ['NS + NS + NS', 'threshold + NS + NS']  # i.e. only one we don't want is NS in protein and RNA
            self.df[f'{self.reg_grp_1_lbl}_filtered'] = [c if bg[i] not in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_1_lbl].values)]
            self.df[f'{self.reg_grp_2_lbl}_filtered'] = [c if bg[i] not in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_2_lbl].values)]
            self.df[f'{self.reg_grp_3_lbl}_filtered'] = [c if bg[i] not in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_3_lbl].values)]
            self.df[f'{self.reg_grp_4_lbl}_filtered'] = [c if bg[i] not in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_4_lbl].values)]

        elif bg_type == 'P&R':  # Protein AND RNA
            conds = ['threshold + threshold + threshold',  # RNA & Methylation ~Protein
                     'NS + threshold + threshold',  # Methylation ~ RNA & protein
                     ]
            self.df[f'{self.reg_grp_1_lbl}_filtered'] = [c if bg[i] in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_1_lbl].values)]
            self.df[f'{self.reg_grp_2_lbl}_filtered'] = [c if bg[i] in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_2_lbl].values)]
            self.df[f'{self.reg_grp_3_lbl}_filtered'] = [c if bg[i] in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_3_lbl].values)]
            self.df[f'{self.reg_grp_4_lbl}_filtered'] = [c if bg[i] in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_4_lbl].values)]

        elif bg_type == 'P&M&R':  # Protein AND Methylation AND RNA
            conds = ['threshold + threshold + threshold']
            self.df[f'{self.reg_grp_1_lbl}_filtered'] = [c if bg[i] in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_1_lbl].values)]
            self.df[f'{self.reg_grp_2_lbl}_filtered'] = [c if bg[i] in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_2_lbl].values)]
            self.df[f'{self.reg_grp_3_lbl}_filtered'] = [c if bg[i] in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_3_lbl].values)]
            self.df[f'{self.reg_grp_4_lbl}_filtered'] = [c if bg[i] in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_4_lbl].values)]
        elif bg_type == '(P&M)|(P&R)|(M&R)':  # At least two are significant
            conds = ['NS + NS + NS', 'NS + NS + threshold', 'NS + threshold + NS', 'threshold + NS + NS']
            self.df[f'{self.reg_grp_1_lbl}_filtered'] = [c if bg[i] not in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_1_lbl].values)]
            self.df[f'{self.reg_grp_2_lbl}_filtered'] = [c if bg[i] not in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_2_lbl].values)]
            self.df[f'{self.reg_grp_3_lbl}_filtered'] = [c if bg[i] not in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_3_lbl].values)]
            self.df[f'{self.reg_grp_4_lbl}_filtered'] = [c if bg[i] not in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_4_lbl].values)]
        elif bg_type == '(P&M)|(P&R)':  # Protein and one other
            conds = ['NS + NS + NS', 'NS + NS + threshold', 'NS + threshold + NS', 'threshold + NS + NS',
                     'threshold + NS + NS']
            self.df[f'{self.reg_grp_1_lbl}_filtered'] = [c if bg[i] not in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_1_lbl].values)]
            self.df[f'{self.reg_grp_2_lbl}_filtered'] = [c if bg[i] not in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_2_lbl].values)]
            self.df[f'{self.reg_grp_3_lbl}_filtered'] = [c if bg[i] not in conds else 'Not-Background' for i, c in
                                                         enumerate(self.df[self.reg_grp_3_lbl].values)]
            self.df[f'{self.reg_grp_4_lbl}_filtered'] = [c if bg[i] not in conds else '"Not-Background"' for i, c in
                                                         enumerate(self.df[self.reg_grp_4_lbl].values)]
        elif bg_type == '*':  # Use all genes as the background
            self.df[f'{self.reg_grp_1_lbl}_filtered'] = [c for i, c in enumerate(self.df[self.reg_grp_1_lbl].values)]
            self.df[f'{self.reg_grp_2_lbl}_filtered'] = [c for i, c in enumerate(self.df[self.reg_grp_2_lbl].values)]
            self.df[f'{self.reg_grp_3_lbl}_filtered'] = [c for i, c in enumerate(self.df[self.reg_grp_3_lbl].values)]
            self.df[f'{self.reg_grp_4_lbl}_filtered'] = [c for i, c in enumerate(self.df[self.reg_grp_4_lbl].values)]

    def get_df(self):
        return self.df

    def save_df(self, output_filename):
        """ Save DF to a csv (mainly for R) """
        self.df.to_csv(output_filename, index=False)

    def get_genes_in_reg_grp(self, label, gene_label=None, reg_label=None):
        """ Get genes for a particular regulatory group. """
        reg_label = reg_label if reg_label else self.main_reg_label
        gene_label = self.gene_id if not gene_label else gene_label
        return list(set(self.df[self.df[reg_label] == label][gene_label].values))

    def get_all_assigned_genes(self, gene_label=None, reg_label=None):
        """ Get all genes assigned to a regulatory group (i.e. any that are not none) """
        reg_label = reg_label if reg_label else self.main_reg_label
        gene_label = self.gene_id if not gene_label else gene_label
        return list(set(self.df[self.df[reg_label] != 'None'][gene_label].values))

    def get_all_unassigned_genes(self, gene_label=None, reg_label=None):
        """ Get all genes that weren't assigned to a regulatory label. """
        gene_label = self.gene_id if not gene_label else gene_label
        reg_label = reg_label if reg_label else self.main_reg_label
        return list(set(self.df[self.df[reg_label] == 'None'][gene_label].values))


def filter_methylation_data_by_genes(cpg_df, gene_id, p_val, logfc):
    cpg_df_grped = cpg_df.groupby(gene_id)
    rows = []
    num_cpgs = []
    for cpg in cpg_df_grped:
        cpg = cpg[1]
        cpg = cpg[cpg[p_val] < 0.05]
        num_cpgs.append(len(cpg))
        if len(cpg) > 0:
            if len(cpg) < 3:
                add_row = True
            else:
                pos_cpg = cpg[cpg[logfc] > 0]
                neg_cpg = cpg[cpg[logfc] < 0]
                num_pos = len(pos_cpg)
                num_neg = len(neg_cpg)
                add_row = False
                if num_pos and num_pos/len(cpg) > 0.6:
                    cpg = pos_cpg
                    add_row = True
                elif num_neg and num_neg/len(cpg) > 0.6:
                    cpg = neg_cpg
                    add_row = True
            if add_row:
                max_cpg_idx = None
                max_t_value = 0  # absolute
                idxs = cpg.index
                for i, t in enumerate(cpg[logfc].values):
                    if abs(t) > abs(max_t_value):
                        max_t_value = t
                        max_cpg_idx = i
                rows.append(cpg[cpg.index == idxs[max_cpg_idx]].values[0])
    new_cpg_df = pd.DataFrame(rows, columns=cpg_df.columns)
    u = SciUtil()
    u.dp(['Originally had: ', len(cpg_df_grped), 'genes.\n', 'Filtered DF now has: ', len(new_cpg_df), ' genes.'])
    return new_cpg_df
