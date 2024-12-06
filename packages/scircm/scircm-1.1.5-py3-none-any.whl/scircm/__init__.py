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

__title__ = 'scircm'
__description__ = ''
__url__ = 'https://github.com/ArianeMora/scircm.git'
__version__ = '1.1.5'
__author__ = 'Ariane Mora'
__author_email__ = 'ariane.n.mora@gmail.com'
__license__ = 'GPL3'

from scircm.base import SciRCM, filter_methylation_data_by_genes
from scircm.vis import plot_cluster_ORA
from scircm.dna_rna import SciMR
from scircm.stats import RCMStats
from scircm.rna_protein import SciRP
