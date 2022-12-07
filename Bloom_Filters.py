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


def calculate_N(input_file):
    with open(input_file,newline="") as file:
        next(file)
        return len(file.readlines())
                
csv_file_input = sys.argv[1]
csv_file_output = sys.argv[2]

N = calculate_N(csv_file_input)
P = 0.0000001
M = math.ceil((N*math.log(P))/math.log(1/math.pow(2,math.log(2))))
K = round((M/N)*math.log(2))

bloom_filter = list(makeBitArray(M))

with open(csv_file_input,newline="") as csv_file:
    next(csv_file)
    reader = csv.reader(csv_file)
    for email in reader:
        for hash_instance in range(K): 
            hash_key = hash(email[0] + str(hash_instance)) % M
            setBit(bloom_filter, hash_key)
    
       
with open(csv_file_output,newline="") as csv_out:
    next(csv_out)
    reader = csv.reader(csv_out)
    for email in reader:
        email_found = True
        for hash_instance in range(K):
            hash_key = hash(email[0] + str(hash_instance)) % M
            test_bit = testBit(bloom_filter, hash_key)
            if test_bit == 0:
                print("{}, Not in the DB".format(email[0]))
                email_found = False
                break
        if email_found:
            print("{}, Probably in the DB".format(email[0]))


            
    
            
            
        






            

            
        
        
                
        
        
        

    
    
  


    
    
    

    
    
    
    
    
    
    
    
    

    
    
    
    
   
    
    
  
    
    

    
    
    
    

    
    
    

