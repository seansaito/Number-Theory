__author__ = "Sean Saito"

from Crypto.PublicKey.pubkey import *
from Crypto.Util import number
from Crypto import Random
from Crypto.Util.number import GCD

class ElGamal(object):
	
	#Storing public and private keys
	keys = ["q", "g", "h", "x"]

	#For Generating Key
	def keyGen(self,bits):
		if bits < 5:
			print "Bit length must be longer than five"
			return
		
		p = 0
		q = 0
		#Generating a safe prime number q
		while 1:
			p = bignum(getPrime(bits-1, Random.new().read))
			q = 2*p + 1
			if number.isPrime(q, randfunc = Random.new().read):
				break
		
		g = 3
		#Generating generator g
		while (g < q):
			if pow(g, 2, q) != 1 and pow(g, p, q) != 1:
				break
			g += 1
		
		#Generate private key x
		x = number.getRandomRange(2, q-1, Random.new().read)
		self.private = x
		
		#Generate public key h
		#self is the core of the discrete log problem
		h = pow(g, x, q)
		
		self.keys = [q, g, h, x]
		return self.keys
		
	"""	
	Sign a piece of data with ElGamal
	Parameter M: The piece of data to sign with ElGamal
	Return: A tuple which represents the signature
	"""
	def sign(self, m):
		#Choose a random number k that is coprime with q
		r,s,k = 0,0,0
		while 1:
			while 1:
				k = number.getRandomRange(2, self.keys[0]-1, Random.new().read)
				if GCD(k, self.keys[0]-1) == 1:
					break
			#Get r
			r = pow(self.keys[1], k, self.keys[0])
			#Get s
			#Use hash function to generate s
			invert_k = self.invert(k, self.keys[0] - 1)
			t = (self.hash(m) - self.keys[3] * r) % (self.keys[0] - 1)
			s = (t * invert_k) % (self.keys[0] - 1)
			#If s is not equal to 0, then success. Otherwise, start over again
			if s != 0:
				break
		signature = (r, s)
		return signature
		
	"""
	Verification of the signature
	Returns a boolean based on success
	"""
	def verify(self, m, signature):
		r = signature[0]
		s = signature[1]
		if not (0 < r < self.keys[0] and 0 < s < self.keys[0] - 1):
			return False
		a = pow(self.keys[1], self.hash(m), self.keys[0])
		b = pow(self.keys[2], r, self.keys[0])
		b = (b * pow(r, s, self.keys[0])) % self.keys[0]
		if a == b:
			return True
		return False
	
	"""
	Encryption
	Parameter m: The data to encrypt
	"""
	def encrypt(self, m):
		c1, c2, shared_secret = 0,0,0
		y = number.getRandomRange(2, self.keys[0]-1, Random.new().read)
		c1 = pow(self.keys[1], y, self.keys[0])
		shared_secret = pow(self.keys[2], y, self.keys[0])
		c2 = (m * shared_secret) % self.keys[0]
		return (c1, c2)
	
	"""
	Decryption
	Parameter tup: Tuple obtained from encryption
	"""
	def decrypt(self, tup):
		ax = pow(tup[0], self.keys[3], self.keys[0])
		message = (tup[1] * self.invert(ax, self.keys[0])) % self.keys[0]
		return message
		

	#The helper functions
	#For finding multiplicative inverse of n, mod p
	def invert(self, n, p):
		t = 0
		newt = 1
		r = p
		newr = n
		while (newr != 0):
			quotient = r/newr
			t, newt = newt, t - quotient * newt
			r, newr = newr, r - quotient * newr
		if r > 1:
			return "n is not invertible"
		if t < 0:
			t = t + p
		return t
	
	#Hashing function to be used in signature
	def hash(self, x):
		digest = md5(x).hexdigest()
		number = int(digest, 16)
		return number
	