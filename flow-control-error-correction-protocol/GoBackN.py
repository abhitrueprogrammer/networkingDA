import time 
import error_correction
#Set up the sliding window
sliding_window = []
window_size = 4
#Shared list class to store packets and ACKs
class SharedList:
    packet_list = []
    ack_list = []
class SharedVariable(SharedList):
    current_sent_ACK = -1
    def add_to_packet_list(current_packet_number, current_data):
        SharedList.packet_list.append([current_packet_number, current_data])

#Sender class that inherits from SharedList
class Sender(SharedList):
    __already_sent = []
    already_recieved_ACK = []
    def send(self, sliding_window):
        
        for packet_no, data in sliding_window:
            if packet_no not in self.__already_sent: #only add ACK if last ACK is in the lis(so ACK list required)
                data = error_correction.add_parity(data) #add error correction
                SharedVariable.add_to_packet_list(packet_no, data)
                self.__already_sent.append(packet_no)
                print(f"Sent: packet Number: {packet_no}")
    '''For the sender to remove already sent packets from the already sent list'''
    def removeAlreadySent(self, packet_numbers): 
        for item in packet_numbers:
            self.__already_sent.remove(item)
    '''For the sender to get the current ACK'''
    def ACK(self):
        if SharedVariable.current_sent_ACK not in self.already_recieved_ACK:
            self.already_recieved_ACK.append(SharedVariable.current_sent_ACK)
        return SharedVariable.current_sent_ACK
class Reciever(SharedList):
    AllData = {-1:""}
    def recieve(self):
        for packet_number, data in SharedVariable.packet_list:
            if max(self.AllData) +1 == packet_number:
                 #set list. Pop from listSharedVariable.add_to_packet_list(packet_no, data)
                if packet_number not in self.AllData:
                    if(error_correction.check_parity(data) == 0):
                        SharedVariable.packet_list.remove([packet_number, data])
                        data = error_correction.remove_parity(data)
                        self.AllData[packet_number] = data
                        print(f"Received: {data}")

                        SharedVariable.current_sent_ACK = packet_number
                        print(f"Acknowledgment sent for sequence number: {packet_number}")
                    else:
                        print(f"Data corrupted: {data}")
                        SharedVariable.current_sent_ACK = -packet_number
                        print(f"NACK sent for sequence number: {packet_number}")
packet_list = [
    [0, "A"],
    [1, "Quick"],
    [2, "Brown"],
    [3, "Fox"],
    [4, "Jumps"],
    [5, "Over"],
    [6, "The"],
    [7, "Lazy"],
    [8, "Dog"]
]
packet_no_list = [dataPacket[0] for dataPacket in packet_list]
sender = Sender()
reciever = Reciever()
max_delay = 5
start_time = current_time = time.time()

while packet_no_list != sender.already_recieved_ACK: #Removes the -1 entery + ensures packets in order
    sent = False
    while(not sent):
        while len(sliding_window) < window_size and packet_list:
            sliding_window.append(packet_list.pop(0))
        while current_time - start_time< max_delay:
            if(sent):
                break
            sender.send(sliding_window)
            reciever.recieve()

            #check for errors.
            for i in range(len(sliding_window)): #the reciever won't send a ACK for a packet in advance anyway
                packet_no = sliding_window[i][0]
                if sender.ACK() == packet_no:
                    print(f"Recieved ACK for packet no{packet_no}")
                    sliding_window.pop(i)
                    sent = True
                    break
            current_time = time.time()
            
        else:
            #if timeout error remove all the packets from the already sent list, and resend them
            while(not sent):
                print("Timeout, Resending")
                sender.removeAlreadySent([ packet_number for packet_number, _ in sliding_window])
        start_time = current_time = time.time()
reciever.AllData.pop(-1)
print(reciever.AllData)