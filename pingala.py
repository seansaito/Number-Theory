import sys

def main(argv):
	a = int(argv[0])
	e = int(argv[1])
	m = int(argv[2])

	print pingala(a,e,m)


# Computes a to the power of e in mod m context
def pingala(a,e,m):
	# Converts the exponent into a binary form
    e_base2 = bin(e)[2:]
    # This keeps track of the final answer
    answer = 1

    # A for loop that iterates through each digit
    # of the binary form of the exponent
    for t in range(len(e_base2)):
        signal = e_base2[t]

        # Squares the current answer
        answer = answer**2

        # If the current digit of the binary form
        # is "on" (or equal to one), then multiply
        # answer by a
        if signal == '1':
            answer = answer*a
            
    #Return the answer in modulo
    return answer % m

if __name__ == '__main__':
	main(sys.argv[1:])