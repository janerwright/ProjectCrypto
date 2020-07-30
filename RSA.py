import random

def RSAKeyGeneration(nBits=2048):
    """
    This function generates a pair of random RSA keys with a modulus of nBits
    bits. It does this by generating 2 random primes so that their product (the
    modulus) has the required size and the primes vary in size by a random
    number of bits. It then randomly generates the public key's power and
    increments it until it is coprime to the product of p-1 and q-1 where p and
    q are the primes generated earlier. Finallly it calculates the private
    key's power by finding the multiplicative inverse of e (the public key's
    power) mod (p-1)*(q-1). It returns the public key's power, the private key's
    power and the modulus in an array.

    Parameters:
        nBits - An integer that specifies the required number of bits for the
                modulus. If unspecified it has a default value of 2048 and if
                too small (less than 8) then it is replaced by this value.

    The returned value is an array containing the public key's power, the
    private key's power and the modulus respectively.

    Other functions from this module used:
        GetRandomPrime
        hcf
        inv_mod
    """
    mBits=nBits//2
    if mBits<8:
        print('Not enough bits so will generate a 2048 bit key.')
        mBits=1024
    diffInSize=random.randrange(0,16)
    if diffInSize>=mBits-7:
        diffInsize=random.randrange(0,mBits-7)
    p=getRandomPrime(mBits+diffInSize)
    q=getRandomPrime(mBits-diffInSize)
    n=p*q
    e=random.randrange(3,2**(mBits-1),2)
    while hcf(e,(p-1)*(q-1))!=1:
        e=e+2
    d=inv_mod(e,(p-1)*(q-1))
    return [e,d,n]

def getRandomPrime(nBits=1024):
    """
    This function generates a random prime that is nBits bits in size. For small
    primes (at most 256 bits) it does this by repeatedly generating a random odd
    number of the required size and checking if it's prime. For larger primes it
    does this by generating a random range (of size 2^16) of numbers of the
    required size and finding the first prime in this range.

    Parameters:
        nBits - An integer specifying the size of the prime to be generated in
                bits. If unspecified it has a default value of 1024.

    The returned value is the generated prime.

    Other functions from this module used:
        sieve
    """
    if nBits>256:
        x=random.randrange(2**(nBits-1)+1,2**nBits-2**16,2)
        p=sieve(x,2**16)
        while p==0:
            x=random.randrange(2**(nBits-1)+1,2**nBits-2**16,2)
            p=sieve(x,2**16)
    else:
        p=random.randrange(2**(nBits-1)+1,2**nBits,2)
        while not isPrime(p):
            p=random.randrange(2**(nBits-1)+1,2**nBits,2)
    return p

def RSAEnc(text,power,modulus,padding=True):
    """
    This function encrypts a given string with the RSA key (power and modulus)
    provided. It applies padding to the string first if required and will remove
    the end of the string if it is too long to be encrypted by the modulus
    without loss of information.

    Parameters:
        text - A string containing the text to be encrypted.
        power - An integer that is the RSA key's power.
        modulus - An integer that is the RSA key's modulus.
        padding - A Boolean specifying whether or not to add padding. If
                  unspecified it will have a default value of True.

    The returned value is the encrypted string.

    Other functions from this module used:
        numBits
        pad
        StrToInt
        power_mod
        IntToStr
    """
    block_size=(numBits(modulus)//8)+1
    if padding:
        temp_str=pad(text[0:block_size-4],block_size)
    else:
        temp_str=text[0:block_size-1]
    temp_str=IntToStr(power_mod(StrToInt(temp_str),power,modulus),block_size)
    return temp_str

def RSADec(text,power,modulus,padding=True):
    """
    This function decrypts the given string with the RSA key (power and modulus)
    provided. It removes any padding after the decryption if required.

    Parameters:
        text - A string containing the text to be decrypted.
        power - An integer that is the RSA key's power.
        modulus - An intger that is the RSA key's modulus.
        padding - A Boolean specifying whether or not to remove padding. If
                  unspecified it will have a default value of True.

    The returned value is the decrypted string.

    Other functions in this module used:
        numBits
        StrToInt
        power_mod
        IntToStr
        removePadding
    """
    block_size=(numBits(modulus)//8)
    temp_str=IntToStr(power_mod(StrToInt(text),power,modulus),block_size)
    if padding:
        temp_str=removePadding(temp_str)
    return temp_str

def pad(text,block_size):
    """
    This function adds PKCS1 v1.5 padding to the given text so that the text is
    the required block size. That is it adds padding starting with the hex 0002
    and ending with the hex ffff to the begining of the string. The rest of the
    padding is random and does not contain the hex sequence ffff.

    Parameters:
        text - A string containing the text to be padded.
        block_size - An integer specifying the required size of the padded text.

    The returned value is the padded text.
    """
    temp_str=chr(255)+chr(255)+text
    prev=255
    while len(temp_str)<block_size-2:
        if prev==255:
            prev=random.randrange(255)
            temp_str=chr(prev)+temp_str
        else:
            prev=random.randrange(256)
            temp_str=chr(prev)+temp_str
    return chr(0)+chr(2)+temp_str

def removePadding(text):
    """
    This function removes PKCS1 padding from the given text. If it does not have
    valid padding the function returns an empty string.

    Parameters:
        text - A string containing the text to remove the padding from.

    The returned value is the text with the padding removed or an empty
    string.
    """
    comp_str=chr(0)+chr(2)
    if text[0:2]!=comp_str:
        return ''
    comp_str=chr(255)+chr(255)
    for loop in range(2,len(text)-1):
        if text[loop:loop+2]==comp_str:
            return text[loop+2:len(text)]
    return ''
    
def StrToInt(text):
    """
    This function turns a string into an integer. It does this by iterating
    through each character in the string, converting it to its extended ASCII
    value and adding this to a running total by first multiplying by 256 to the
    power of the number of places from the end of the string the character is.
    This assigns each string a unique integer.

    Parameters:
        text - The string to be turned into an integer.

    The returned value is the integer produced from the string.
    """
    running_total=0
    running_power256=1
    for loop in range(len(text)-1,-1,-1):
        running_total=running_total+ord(text[loop])*running_power256
        running_power256=running_power256*256
    return running_total

def IntToStr(number,block_size):
    """
    This function turns an integer into a string. It does this by finding the
    remainder of the current number (initialised to the given integer) divided
    by 256, adding the character relating to this remainder (using extended
    ASCII) to the begining of a string (initialised to an empty string) and
    then replaces the current number with itself divided (integer division) by
    256. It repeats this process until a string of the required length is
    produced.

    Parameters:
        number - The integer to be turned into a string.
        block_size - An integer specifying the required length of the produced
                     string.

    The returned value is the string produced from the number.
    """
    temp_str=''
    current_number=number
    for _ in range(0,block_size):
        temp_str=chr(current_number%256)+temp_str
        current_number=current_number//256
    return temp_str

def numBits(number):
    """
    This function calculates the number of bits required to represent a given
    integer.

    Parameters:
        number - The integer to calculate the number of bits for.

    The returned value is the number of required bits.
    """
    n_bits=0
    current_power2=1
    while current_power2<=number:
        current_power2=current_power2*2
        n_bits=n_bits+1
    return n_bits

def power_mod(base,power,modulus):
    """
    This function calculates a number to a given power modulo (the remainder
    when divided by) a given modulus. It does this efficiently by repeatedly
    squaring the given number, if the current power number is odd it
    multiplies a running value (initialised to 1) by the current squared value
    and divides the current power value by 2 (integer division). Every operation
    is performed in modular arithmetic (using the remainders when divided by the
    given modulus) to improve efficiency.

    Parameters:
        base - An integer that is the base for the exponentiation.
        power - An integer that is the power to raise base to.
        modulus - An integer that is the number to divide by to calculate the
                  remainders.

    The returned value is base^power (mod modulus).
    """
    temp_int=1
    current_power=power
    current_square=base
    while current_power>0:
        if (current_power%2)==1:
            temp_int=(temp_int*current_square)%modulus
        current_square=(current_square*current_square)%modulus
        current_power=current_power//2
    return temp_int

def inv_mod(number,modulus):
    """
    This function calculates the multiplcative inverse of a given number with a
    given modulus (when a number and its inverse are multiplied the remainder
    when divided by the modulus is 1). It does this using the extended Euclidean
    algorithm to find 2 numbers a and b such that a*number + b*modulus = 1. In
    this formula the number a is the inverse of number for the given modulus.
    This function assumes that the inverse exists (i.e. the given number and
    modulus aare coprime).

    Parameters:
        number - The integer to find the multiplicative inverse of.
        modulus - The integer that is the modulus to find the inverse of number
                  for.

    The returned value is the multiplicative inverse of the given number for the
    given modulus.

    Other functions from this module used:
        extendedhcf
    """
    temp_arr=extendedhcf(number,modulus)
    return temp_arr[0]%modulus

def hcf(num1,num2):
    """
    This function calculates the highest common factor of 2 given integers. It
    does this using the Euclidean algorithm.

    Parameters:
        num1 - One of the integers to calculate the highest common factor of.
        num2 - The other integer to calculate the highest common factor of.

    The returned value is the highest common factor of the given numbers.
    """
    remainder=num1%num2
    if remainder==0:
        return num2
    else:
        return hcf(num2,remainder)

def extendedhcf(num1,num2):
    """
    This function calculates the highest common factor of 2 given integers and
    finds a linear combination of the 2 numbers that equals this value. It does
    this using the extended Euclidean algorithm.

    Parameters:
        num1 - One of the integers to calculate the highest common factor of.
        num2 - The other integer to calculate the highest common factor of.

    The returned value is an array of integers [a,b,c] where a*num1+b*num2=c and
    c is the highest common factor of num1 and num2.
    """
    remainder=num1%num2
    quotient=num1//num2
    if remainder==0:
        return [0,1,num2]
    else:
        temp_arr=extendedhcf(num2,remainder)
        return [temp_arr[1],temp_arr[0]-quotient*temp_arr[1],temp_arr[2]]

def isPrime(number):
    """
    This function tests a given integer for primality. It does this by a Fermat
    test with base 2 and a 40 round Miller-Rabin test. This function is
    probabilistic but the probability of failure is negligible.

    Parameters:
        number - The integer to test for primality.

    The returned value is a Boolean specifying whetheror not the given number is
    prime.
    """
    if power_mod(2,number-1,number)==1:
        odd_num=number-1
        power_of_2=0
        while odd_num%2==0:
            odd_num=odd_num//2
            power_of_2=power_of_2+1
        for _ in range(40):
            temp_base=random.randrange(2,number-1)
            temp_num=power_mod(temp_base,odd_num,number)
            if not (temp_num==1 or temp_num==number-1):
                counter=0
                while counter<power_of_2-1 and not temp_num==number-1:
                    temp_num=(temp_num*temp_num)%number
                if not temp_num==number-1:
                    return False
        return True
    else:
        return False

def smallPrimes():
    """
    This function creates an array of all primes less than 2^16.
    """
    is_prime_arr=[False,False]+[True for _ in range(2,2**16)]
    prime_arr=[]
    for num in range(2,2**16):
        if is_prime_arr[num]:
            prime_arr=prime_arr+[num]
            temp_num=num*num
            while(temp_num<2**16):
                is_prime_arr[temp_num]=False
                temp_num=temp_num+num
    return prime_arr

def sieve(lower_bound,size):
    """
    This function sieves a given range for multiples of small prime numbers
    (less than 2^16) and then finds the first prime in the remaining numbers.
    It returns a 0 if there are no primes in the given range.

    Parameters:
        lower_bound - The smallest integer in the given range.
        size - The number of integers in the given range.

    The returned value is the first prime in the range or 0 if there are no
    primes in the range.
    """
    is_prime_arr=[True for _ in range(size)]
    for prime in sPrimes:
        temp_num=lower_bound+(prime-(lower_bound%prime))
        while temp_num<lower_bound+size:
            is_prime_arr[temp_num-lower_bound]=False
            temp_num=temp_num+prime
    for num in range(lower_bound,lower_bound+size):
        if is_prime_arr[num-lower_bound]:
            if isPrime(num):
                return num
    return 0

#This array of small prime numbers is used by the sieve function and is stored as a variable so that it does not need to be generated everytime a new large prime is needed.
sPrimes=smallPrimes()

