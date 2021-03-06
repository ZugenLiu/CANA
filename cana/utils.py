import networkx as nx
import numpy as np
from itertools import product
import copy
import math

def binstate_to_statenum(binstate):
	""" Converts from binary state to state number.
	
	Args:
		binstate (string) : The binary state.
	Returns:
		int : The state number.
	Example:
		
		.. code-block:: python
		
			'000' -> 0
			'001' -> 1
			'010' -> 2 ...

	See also:
		:attr:`statenum_to_binstate`, :attr:`statenum_to_density`
	"""
	return int(binstate, 2)

def statenum_to_binstate(statenum, base):
	""" Converts an interger into the binary string.
	
	Args:
		statenum (int) : The state number.
		base (int) : The binary base
	Returns:
		string : The binary state.
	Example:
		
		.. code-block:: python

			0 -> '00' (base 2)
			1 -> '01' (base 2)
			2 -> '10' (base 2)
			...
			0 -> '000' (base 3)
			1 -> '001' (base 3)
			2 -> '010' (base 3)

	See also:
		:attr:`binstate_to_statenum`, :attr:`binstate_to_density`
	"""
	# binary representation
	bstate = bin(statenum)[2::]
	# 0 padding
	bstate = "".join(['0' for n in xrange(base - len(bstate))]) + bstate
	return bstate

def flip_bit(bit):
	"""Flips the binary value of a state.

	Args:
		bit (string/int/bool): The current bit position
	Returns:
		same as input: The flipped bit
	"""
	if isinstance(bit, str):
		return '0' if (bit=='1') else '1'
	elif isinstance(bit, int) or isintance(bit, bool):
		return 0 if (bit == 1) else 1
	else:
		raise TypeError("'bit' type format must be either 'string', 'int' or 'boolean'")

def flip_binstate_bit(binstate, idx):
	"""Flips the binary value of a bit in a binary state.

	Args:
		binstate (string) : The binary state.
		idx (int) : The index of the bit to flip.
	Returns:
		(string) : New binary state.

	"""
	if idx > len(binstate):
		raise TypeError('Binary state (%s) length and index position (%d) mismatch for.' % (binstate, idx))

	_binstate = list(binstate)
	_binstate[idx] = flip_bit(_binstate[idx])
	return ''.join(_binstate)

def flip_binstate_bit_set(binstate, idxs):
	"""Flips the binary value for a set of bits in a binary state.
	
	Args:
		binstate (string) : The binary state to flip.
		idxs (int) : The indexes of the bits to flip.
	
	Returns:
		(list) : The flipped states
	"""
	flipset = []
	if (len(idxs) != 0):
		fb = idxs.pop()
		flipset.extend(flip_binstate_bit_set(binstate, copy.copy(idxs) ) )
		flipset.extend(flip_binstate_bit_set(flip_binstate_bit(binstate, fb), copy.copy(idxs) ) )
	else:
		flipset.append(binstate)
	return flipset

def statenum_to_density(statenum):
	"""Converts from state number to density
	
	Args:
		statenum (int): The state number 
	Returns:
		int: The density of ``1`` in that specific binary state number.
	Example:
		>>> statenum_to_binstate(14, base=2)
		>>> '1110'
		>>> statenum_to_density(14)
		>>> 3
	"""
	return sum(map(int, bin(statenum)[2::]))

def binstate_to_density(binstate):
	"""Converts from binary state to density

	Args:
		binstate (string) : The binary state
	Returns:
		int
	Example:
		>>> binstate_to_density('1110')
		>>> 3
	"""
	return sum(map(int, binstate))

def binstate_to_constantbinstate(binstate, constant_template):
	""" @Not Sure yet. It is being used in the boolean_network._update_trans_func @ """
	constantbinstate = ''
	iorig = 0
	for value in constant_template:
		if value is None:
			constantbinstate += binstate[iorig]
			iorig += 1
		else:
			constantbinstate += str(value)

	return constantbinstate

def constantbinstate_to_statenum(constantbinstate, constant_template):
	""" @NOT SURE """
	binstate = ''.join([constantbinstate[ivar] for ivar in xrange(len(constant_template)) if constant_template[ivar] is None])
	return binstate_to_statenum(binstate)

def expand_logic_line(line):
	""" This generator expands a logic line containing ``-`` (ie. ``00- 0`` or ``0-0 1``) to a series of logic lines containing only ``0`` and ``1``.

	Args:
		line (string) : The logic line. Format is <binary-state><space><output>.
	Returns:
		generator : a series of logic lines
	Example:
		>>> expand_logic_line('1-- 0')
		>>> 100 0
		>>> 101 0
		>>> 110 0
		>>> 111 0
	"""
	# helper function for expand_logic_line
	def _insert_char(la,lb):
		lc=[]
		for i in range(len(lb)):
			lc.append(la[i])
			lc.append(lb[i])
		lc.append(la[-1])
		return ''.join(lc)

	line1,line2=line.split()
	chunks=line1.split('-')
	if len(chunks)>1:
		for i in product(*[('0','1')]*(len(chunks)-1)):
			yield _insert_char(chunks,i)+' '+line2
	else:
		for i in [line]:
			yield i

def print_logic_table(outputs):
	""" Print Logic Table

	Args:
		outputs (list) : The transition outputs of the function.
	Returns:
		print : a print-out of the logic table.
	Example:
		>>> print_logic_table([0,0,1,1])
		>>> 00 : 0
		>>> 01 : 0
		>>> 10 : 1
		>>> 11 : 1

	"""
	k = int(math.log(len(outputs))/math.log(2))
	for statenum in xrange(2**k):
		print(statenum_to_binstate(statenum, base=k) + " : " + str(outputs[statenum]))

def entropy(prob_vector, logbase = 2.):
	""" Calculates the entropy given a probability vector
	@ SHOULD THIS BE CALCULATED USING scipy.entropy INSTEAD? @
	"""
	prob_vector = np.array(prob_vector)
	pos_prob_vector = prob_vector[prob_vector > 0]
	return - np.sum(pos_prob_vector * np.log(pos_prob_vector)/np.log(logbase))

def hamming_distance(s1, s2):
	"""Calculates the hamming distance between two configurations strings.

	Args:
		s1 (string): First string
		s2 (string): Second string
	Returns:
		float : The Hamming distance
	Example:
		>>> hamming_distance('001','101')
		>>> 1
	"""
	assert len(s1) == len(s2) , "The two strings must have the same length"
	return sum([s1[i] != s2[i] for i in xrange(len(s1))])


