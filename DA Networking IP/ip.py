def main():
    address = input("Enter the IPv4 address: ")
    cls = int(input("Enter 1 for classful, 0 for CIDR: "))
    cidr = 8
    if(not cls):
        cidr = int(input("Enter the CIDR notation: "))
    ip_obj = ip(address, cls= cls , CIDR = cidr)
    while True:
        
        print("\nMenu:")
        print("1. Find out the class of given IPv4 address, network id, and host id")
        print("2. Check if an IP address is valid or not")
        print("3. Find the first address, last address, and number of addresses in the block")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            
            if cls:
                print("Class:", ip_obj.cls())
            else:
                print("Classless")
            net_id, host_id = ip_obj.find_netid_hostid_class()
            print("Network ID:", end="")
            ip.print_ip(net_id)
            print("Host ID:", end="")
            ip.print_ip(host_id)

        elif choice == "2":
            
            if ip_obj.valid():
                print("Valid IP address.")
            else:
                print("Invalid IP address.")

        elif choice == "3":
            
            first_addr, last_addr, count = ip_obj.start_end_number_hosts()
            print("First Address:")
            ip.print_ip(first_addr)
            print("Last Address:")
            ip.print_ip(last_addr)
            print("Number of addresses in the block:", count)

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a valid option.")
def negation( octet):
        octet = str(bin(octet)[2:])
        octet += '0' * (8 -len(octet))
        octet_str = ""
        for bit in octet:
            if bit == '1':
                octet_str += '0'
            else:
                octet_str += '1'
        octet_str = octet_str[::-1] #reversing string cz addition happens in front
        octet = int(octet_str,2)
        return octet


class ip:
    ip_addr = []
    ip_addr_num = 0 #ip address in numberical form
    __addr_subnet = []
    #use CIDR only if class is 0.
    def __init__(self,address:str , cls = 1, CIDR = 8) -> None:
        self.ip_addr = address.split(".")
        self.ip_addr_num = "".join(self.ip_addr)
        self.ip_addr = [int(octet) for octet in self.ip_addr]
        
        if(cls):
            first_octet = self.ip_addr[0]
            if first_octet >= 0 and first_octet < 128:
                self.__addr_subnet =  [255,0,0,0]
            elif first_octet >= 128 and first_octet < 192:
                self.__addr_subnet =  [255,255,0,0]
            elif first_octet >= 192 and first_octet  < 224:
                self.__addr_subnet =  [255,255,255,0]
            elif first_octet >= 224 and first_octet < 240:
                self.__addr_subnet =  [255,255,255,255]
            else:
                self.__addr_subnet =  [] #E is multicast
        else:
            if CIDR > 32 or CIDR < 0:
                raise ValueError("CIDR ranges from 0 to 32")
            self.__addr_subnet = []
            one_in_current_octet = 0
            for _ in range(CIDR):
                one_in_current_octet += 1
                if one_in_current_octet == 8:
                    self.__addr_subnet.append(255)
                    one_in_current_octet = 0
            if len(self.__addr_subnet) > 4:
                raise ValueError("ERROR!")
            if one_in_current_octet:
                self.__addr_subnet.append(int(one_in_current_octet*'1'+ '0' *(one_in_current_octet ), 2))
            while(len(self.__addr_subnet) < 4):
                    self.__addr_subnet.append(0)
    def cls(self) -> str:
            count = -1  #cz 0 needed to be added in 1st one.
            if(self.__addr_subnet == []):
                return 'E'
            for i in self.__addr_subnet:
                if i:
                    count += 1
            return chr( ord('A') + count) 
    
    def find_netid_hostid_class(self) -> list:
        net_id = [self.__addr_subnet[i] & self.ip_addr[i] for i in range(0, 4)]
        host_id = [~self.__addr_subnet[i] & self.ip_addr[i] for i in range(0, 4)]
        return [net_id, host_id]
    
    def valid(self) -> bool:
        conditions= []
        condition1 = all([True if i <= 255 and i >= 0 else False for i in self.ip_addr])
        conditions.append(condition1)
        return (all(conditions))
    
    def start_end_number_hosts(self):
        net_id =  [self.__addr_subnet[i] & self.ip_addr[i] for i in range(0, 4)]
        first_addr = net_id
        last_addr = []
        for i in range(len(self.__addr_subnet)):
            octet = negation(self.__addr_subnet[i])
            last_addr.append(self.ip_addr[i]|octet)

        binary_subnet = [bin(i) for i in self.__addr_subnet ] #get the binary representation of number
        num_zeros = sum([ i.count('0') - 1 for i in binary_subnet]) #binary representation is in 0bx format. remove the first 0
        count = 2 ** num_zeros

        return [first_addr, last_addr, count]


    @staticmethod
    def print_ip(ip: list):
        ip = [str(octet) for octet in ip]
        str_ip = '.'.join(ip)
        print(str_ip)


if __name__ == "__main__":
    main()