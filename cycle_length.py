import sys

def main(argv):
	a = int(argv[0])
	m = int(argv[1])
	print cycle_length(a,m)

#Measures the GCD of two numbers
def hop_skip(target, divisor):
	multiple = target/divisor
	remainder = target - (multiple * divisor)

	while(remainder != 0):
		target = divisor
		divisor = remainder
		multiple = target/divisor
		remainder = target - (multiple * divisor)

	return divisor

#Measures the length of a cycle obtained by multiplying a mod m among numbers co-prime to m
def cycle_length(a,m):
	#Checks if a and m are co-prime
	#If they are not, then the function stops
	if (hop_skip(a,m) != 1):
		print "The inputs must by co-prime"
		return

	#Keeps track of the length of the cycle
	exponent = 1
	x = a
	
	#Multiplies a mod m to x until x = 1
	while (x != 1):
		exponent += 1
		x = (x * a) % m

	return exponent

if __name__ == "__main__":
	main(sys.argv[1:])