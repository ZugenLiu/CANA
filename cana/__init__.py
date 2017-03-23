__package__ = 'cana'
__title__ = u'CANAlization: Control & Redundancy in Boolean Networks'
__description__ = u'This package implements a series of methods used to study control, canalization and redundancy in Boolean Networks.'

__author__ = """\n""".join([
	'Alex Gates <ajgates@umail.iu.edu>',
	'Rion Brattig Correia <rionbr@gmail.com>',
	'Etienne Nzabarushimana <enzabaru@indiana.edu>',
	'Luis M. Rocha <rocha@indiana.edu>'
])

__copyright__ = u'2017, Gates, A., Correia, R. B., Rocha, L. M.'

__version__ = '0.0.1'
__release__ = '0.0.1a'
#
__all__ = ['boolean_network','boolean_node','boolean_canalization']

#
from boolean_network import BooleanNetwork
from boolean_node import BooleanNode
#
from boolean_canalization import *
from utils import *
#