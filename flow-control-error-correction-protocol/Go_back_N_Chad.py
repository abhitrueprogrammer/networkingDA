import time 
import error_correction

# Initialize variables
sliding_window = []
window_size = 4

# Shared list class to store packets and ACKs
class SharedList:
    """
    A class representing a shared list for storing packets and ACKs.

    Attributes:
        packet_list (list): A list to store packets.
        ack_list (list): A list to store ACKs.
    """
    packet_list = []  # List to store packets
    ack_list = []  # List to store ACKs

# Shared variable class that inherits from SharedList
class SharedVariable(SharedList):
    current_sent_ACK = -1  # Current ACK sent

    # Method to add packet to the packet list
    def add_to_packet_list(current_packet_number, current_data):
        SharedList.packet_list.append([current_packet_number, current_data])

# Sender class that inherits from SharedList
class Sender(SharedList):
    __already_sent = []  # List to store already sent packets
    already_recieved_ACK = []  # List to store already received ACKs

    # Method to send packets in the sliding window
    def send(self, sliding_window):
        for packet_no, data in sliding_window:
            if packet_no not in self.__already_sent:  # Only add ACK if last ACK is in the list (so ACK list required)
                data = error_correction.add_parity(data)  # Add parity to data
                SharedVariable.add_to_packet_list(packet_no, data)  # Add packet to the packet list
                self.__already_sent.append(packet_no)  # Add packet to the already sent list
                print(f"Sent: packet Number: {packet_no}")

    # Method to remove already sent packets from the already sent list
    def removeAlreadySent(self, packet_numbers):
        for item in packet_numbers:
            self.__already_sent.remove(item)

    # Method to get the current ACK
    def ACK(self):
        if SharedVariable.current_sent_ACK not in self.already_recieved_ACK:
            self.already_recieved_ACK.append(SharedVariable.current_sent_ACK)
        return SharedVariable.current_sent_ACK

# Receiver class that inherits from SharedList
class Receiver(SharedList):
    """
    The Receiver class represents the receiver in a flow control and error correction protocol.

    Attributes:
        AllData (dict): A dictionary to store all received data.

    Methods:
        receive(): Method to receive packets.
    """

    AllData = {-1: ""}  # Dictionary to store all received data

    def receive(self):
        """
        Receive packets and perform error correction and flow control.

        This method iterates over the packet list and checks if the packet number is in order.
        It then checks the parity of the data and removes the parity if it is correct.
        If the data is corrupted, it sends a NACK (Negative Acknowledgment) for the sequence number.
        If the data is correct, it sends an ACK (Acknowledgment) for the sequence number.

        Returns:
            None
        """
        for packet_number, data in SharedVariable.packet_list:
            if max(self.AllData) + 1 == packet_number:  # Check if packet number is in order
                if packet_number not in self.AllData:
                    if(error_correction.check_parity(data) == 0):  # Check parity of data
                        SharedVariable.packet_list.remove([packet_number, data])  # Remove packet from packet list
                        data = error_correction.remove_parity(data)  # Remove parity from data
                        self.AllData[packet_number] = data  # Add data to AllData dictionary
                        print(f"Received: {data}")
                        SharedVariable.current_sent_ACK = packet_number  # Set current ACK
                        print(f"Acknowledgment sent for sequence number: {packet_number}")
                    else:
                        print(f"Data corrupted: {data}")
                        SharedVariable.current_sent_ACK = -packet_number  # Set current NACK
                        print(f"NACK sent for sequence number: {packet_number}")

# List of packets
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

# List of packet numbers
packet_no_list = [dataPacket[0] for dataPacket in packet_list]

# Create instances of Sender and Receiver classes
sender = Sender()
receiver = Receiver()

max_delay = 5
start_time = current_time = time.time()

# Loop until all packets are received
while packet_no_list != sender.already_recieved_ACK:  # Removes the -1 entry + ensures packets are in order
    sent = False
    while(not sent):
        while len(sliding_window) < window_size and packet_list:
            sliding_window.append(packet_list.pop(0))  # Add packets to sliding window

        while current_time - start_time < max_delay:
            if(sent):
                break
            sender.send(sliding_window)  # Send packets
            receiver.receive()  # Receive packets

            # Check for received ACKs
            for i in range(len(sliding_window)):
                packet_no = sliding_window[i][0]
                if sender.ACK() == packet_no:
                    print(f"Received ACK for packet no {packet_no}")
                    sliding_window.pop(i)  # Remove packet from sliding window
                    sent = True
                    break 

            current_time = time.time()

        else:
            while(not sent):
                print("Timeout, Resending")
                sender.removeAlreadySent([packet_number for packet_number, _ in sliding_window])  # Remove already sent packets

        start_time = current_time = time.time()

receiver.AllData.pop(-1)  # Remove the -1 entry from AllData dictionary
print(receiver.AllData)  # Print the received data