def _calculate_parity(data):
    return sum([ord(x) for x in data]) % 2
#returns 0 if check_parity is equal 0
def check_parity(data):
    parity = _calculate_parity(data[0])
    return parity ^ int(data[1]) #adding bits removing the extra bit
def add_parity(data):
    if _calculate_parity(data) == 0:
        return [data , "0"]
    else:
        return [data , "1"]
    
def remove_parity(data):
    return data[0]
