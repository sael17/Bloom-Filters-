import sys 
import csv
import math
import array

# we specify the newline keyword argument and pass an empty string
# this is because depending on the system, strings may end with a newline,
# This technique makes sure that that the csv module works correctly accross all platforms
if len(sys.argv) > 1:
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

    bloomArray = makeBitArray(10)  # Creates a 10 bit array
    setBit(bloomArray, 5)  # Set Bit 5 of bloomArray to 1
    clearBit(bloomArray, 5)  # Set Bit 5 of bloomArray to 0
    testBit(bloomArray, 5)  # Returns a non-zero value if bit 5 is not zero.
    bloom_filter = []
    
    with open (sys.argv[1],newline="") as db_input:
        next(db_input) # the first line is the header so we skip it
        csv_read = csv.reader(db_input) # read the contents of the file
        N = len(db_input.readlines()) # Size of DB. How many emails are in the DB
        P = 0.0000001 # false positive probability 
        M = math.ceil((N*math.log(P))/math.log(1/pow(2,math.log(2)))) # size of bloom filter
        K = round((M/N) * math.log(2)) # number of hashes        
        
        db_input.seek(0)
        next(db_input)
        bloom_filter = list(makeBitArray(M))
        #print(bloom_filter)
        
        for email in csv_read:
            for hash_val in range(K):
                hash_key = (hash(email[0] + str(hash_val))) % M
                #print(hash_key)
                setBit(bloom_filter,hash_key)
            # print(bloom_filter)
            
    with open (sys.argv[2],newline="") as db_check:
        next(db_check)  # the first line is the header so we skip it
        csv_check_read = csv.reader(db_check)  # read the contents of the file
        # Size of DB. How many emails are in the DB
        N = len(db_check.readlines())
        P = 0.0000001  # false positive probability
        # size of bloom filter
        M = math.ceil((N*math.log(P))/math.log(1/pow(2, math.log(2))))
        K = round((M/N) * math.log(2))  # number of hashes

        db_check.seek(0)
        next(db_check)
        
        for email in csv_check_read:
            email_found = True
            for hash_key in range(K):
                hash_key = (hash(email[0] + str(hash_key))) % M
                if testBit(bloom_filter,hash_key) == 0:
                    email_found = False
                    print("{} Not in the DB".format(email))
                    break
            if email_found:
                print("{} probably in the DB".format(email))
                
        
            

            
        
        
                
        
        
        

    
    
  


    
    
    

    
    
    
    
    
    
    
    
    

    
    
    
    
   
    
    
  
    
    

    
    
    
    

    
    
    

