import sys
import csv
import array
import math


def makeBitArray(bitSize, fill=0):
    intSize = bitSize >> 5                   # number of 32 bit integers
    if (bitSize & 31):                      # if bitSize != (32 * n) add
        intSize += 1  # a record for stragglers
    if fill == 1:
        fill = 4294967295                                 # all bits set
    else:
        fill = 0                                      # all bits cleared

    bitArray = array.array('I')          # 'I' = unsigned 32-bit integer
    bitArray.extend((fill,) * intSize)
    return(bitArray)

  # testBit() returns a nonzero result, 2**offset, if the bit at 'bit_num' is set to 1.
def testBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    return(array_name[record] & mask)

# setBit() returns an integer with the bit at 'bit_num' set to 1.
def setBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] |= mask
    return(array_name[record])

# clearBit() returns an integer with the bit at 'bit_num' cleared.
def clearBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = ~(1 << offset)
    array_name[record] &= mask
    return(array_name[record])

# toggleBit() returns an integer with the bit at 'bit_num' inverted, 0 -> 1 and 1 -> 0.
def toggleBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] ^= mask
    return(array_name[record])

"""
Function that counts how many lines, or items, are in a CSV file
returns: int number that represents the number lines present in the file

"""
def calculate_N(input_file):
    with open(input_file) as file:
        next(file)
        return len(file.readlines())
            
# first file is the input emails found in the DB    
csv_file_input = sys.argv[1]
# Seconf file is to check emails in the DB
csv_file_output = sys.argv[2]

""" Constans used for the Bloom Filter Equations"""
# Number of items in the filter 
N = int(calculate_N(csv_file_input))
# Probability of False Positives
P = 0.0000001
# Number of bits in the bloom filter
M = int(math.ceil((N*math.log(P))/math.log(1/math.pow(2,math.log(2)))))
# Number of Hash Functions that are going to be done for each email
K = int(round((M/N)*math.log(2)))

# bit array that represents the bloom filter 
bloom_filter = list(makeBitArray(M))
# open input DB file to read emails from it. We are using with in order to close the file once we finish
with open(csv_file_input) as csv_file:
    # skip the header of the file 
    next(csv_file)
    reader = csv.reader(csv_file)
    for email in reader:
        # Hash every email found in the DB K times
        for hash_instance in range(K): 
            # a int is represented with M bits, so in order to hash it in those bits we use % M
            # add a str to the email in order to make hashes different each time
            hash_key = hash(email[0] + str(hash_instance)) % M
            setBit(bloom_filter, hash_key)
    
       
with open(csv_file_output) as csv_out:
    next(csv_out)
    reader = csv.reader(csv_out)
    for email in reader:
        # This variable will tell us if an email was found or not in the DB
        email_found = True
        for hash_instance in range(K):
            # emails are hashed again in order to get their key for the bit array
            hash_key = hash(email[0] + str(hash_instance)) % M
            # check if email is in the bitarray using its hash_key
            test_bit = testBit(bloom_filter, hash_key)
            # testBit = 0 -> Not in the bitarray, testBit != 0 -> email in the bitarray
            if test_bit == 0:
                print("{}, Not in the DB".format(email[0]))
                # set flag to false since we did not found the email
                email_found = False
                # there is no point in keep looking since its already known that the email is not present
                break
        # email is probably in the DB, let the user know
        if email_found:
            print("{}, Probably in the DB".format(email[0]))


            
    
            
            
        






            

            
        
        
                
        
        
        

    
    
  


    
    
    

    
    
    
    
    
    
    
    
    

    
    
    
    
   
    
    
  
    
    

    
    
    
    

    
    
    

