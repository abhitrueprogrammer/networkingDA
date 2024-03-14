from conversion import *

# hamming code generator
# taking leftmost bit as 0th bit.
from functools import reduce

def create_list(msg, chunks):
    remainder = len(msg) % chunks
    msg = remainder * '0' + msg
    msglist = [msg[i: i + chunks] for i in range(0, len(msg), chunks)] # split msg into list
    return msglist
def insertParity(chunk):
    #calculation of redundancy bit
    r = 0
    for i in range(1,len(chunk)):
        if 0 >= i - 2**i + len(chunk) + 1:
            r = i
            break

    chunk = '0'+chunk #adding 0th parity 
    for i in range(0, r):
        chunk = chunk[:2**i] + '0' + chunk[2**i:]
        i += 1
    return chunk
def flipbit(bit):
    return str(int(not(int(bit))))

'''takes in chunk and the bitindex of the bit of chunk to be changed'''
def insertFlipped(chunk, bitindex):
    return chunk[0:bitindex] + flipbit(chunk[bitindex]) + chunk[bitindex+1:]
def perform_xor_on_pos_where_bit_is_1(chunk):
    passedchunk = list(chunk)
    passedchunk = [int(bit) for bit in chunk]
    return reduce(lambda i,j: i^j,[pos for pos, bit in enumerate(passedchunk) if bit == 1])

def hamming_generate(msg):
    print("Generating hamming code for given message...")
    hamming_list = create_list(msg, 11)
    #insert parity
    for i in range(len(hamming_list)):
        hamming_list[i] = insertParity(hamming_list[i])
        xor_result = itob(perform_xor_on_pos_where_bit_is_1(hamming_list[i]))
        xor_result  = xor_result[::-1] #such that 1st position is 0th index in the string too
        for bitindex in range(len(xor_result)):
            if xor_result[bitindex] == '1':
                hamming_list[i] = insertFlipped(hamming_list[i], 2**bitindex)
    #add code to turn on and off 0th bit.
    return  "".join(hamming_list)

def hammingCorrect(msg):
    print("Checking msg for errors using hamming code...")
    hamming_list = create_list(msg, 16)
    for i in range(len(hamming_list)):
        xor_result = perform_xor_on_pos_where_bit_is_1(hamming_list[i])
        if xor_result == 0:
            continue
        print(f"Error detected for chunk {i}, correcting")
        hamming_list[i] = insertFlipped(hamming_list[i],xor_result)
        xor_result = itob(perform_xor_on_pos_where_bit_is_1(hamming_list[i]))
        if xor_result == 0:
            print(f"{i}th chunk corrected")
        else:
            print(f"Can't correct the error at {i}th chunk")
    return "".join(hamming_list)
# print(perform_xor_on_pos_where_bit_is_1(hamming_generate("00101110110")))
