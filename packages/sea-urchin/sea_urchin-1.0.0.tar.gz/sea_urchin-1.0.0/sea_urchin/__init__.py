"""
The Electrolyte Machine is a set of Python tools to post-process trajectories from AIMD, MD and metadynamics simulations. The pycolvars module easily reads and analyze metadynamics runs. The Sea Urchin module can extract and analyze local structure around atomic species. The outcome of the algorithm is a quantitative mapping of the multiple coordination environments present in the MD data.

Details on the Sea Urchin algorithm are presented in the paper:
Roncoroni, F., Sanz-Matias, A., Sundararaman, S., & Prendergast, D. Unsupervised learning of representative local atomic arrangements in molecular dynamics data. Phys. Chem. Chem. Phys.,25, 13741-13754 (2023) (https://doi.org/10.1039/D3CP00525A);
arXiv preprint arXiv:2302.01465.

Applications of the Sea Urchin algorithm:
Sanz-Matias, A., Roncoroni, F., Sundararaman, S., & Prendergast, D. Ca-dimers, solvent layering, and dominant electrochemically active species in Ca(BH4_44​)2_22​ in THF Nature Communications 15, 1397 (2024) (https://doi.org/10.1038/s41467-024-45672-7)
arXiv preprint [https://arxiv.org/pdf/2303.08261]

"""

# import os
import sys 

if sys.version_info[0] == 2:
    raise ImportError('Please run with Python3. This is Python2.')

# package info
__version__ = '1.0.0'
__date__    = "27 Nov. 2024"
__author__  = "Materials Theory Group"
