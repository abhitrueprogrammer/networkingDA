import time 
import error_correction

sliding_window = []  # Initializing sliding window
window_size = 4  # Setting window size

# Class to hold shared lists
class SharedList:
    packet_list = []  # List to hold packets
    ack_list = []  # List to hold acknowledgments

# Class to hold shared variables, inheriting from SharedList
class SharedVariable(SharedList):
    current_sent_ACK = -1  # Current acknowledgment to be sent

    # Method to add packet to the packet list
    def add_to_packet_list(current_packet_number, current_data):
        SharedList.packet_list.append([current_packet_number, current_data])

# Sender class, inheriting from SharedList
class Sender(SharedList):
    """
    The Sender class represents a sender in a flow control error correction protocol.

    Attributes:
        __already_sent (list): List to keep track of already sent packets.
        already_recieved_ACK (list): List to keep track of received acknowledgments.

    Methods:
        send(sliding_window): Sends packets from the sliding window.
        removeAlreadySent(packet_numbers): Removes packets that are already sent.
        ACK(): Handles acknowledgment.

    """

    __already_sent = []  # List to keep track of already sent packets
    already_recieved_ACK = []  # List to keep track of received acknowledgments

    # Method to send packets
    def send(self, sliding_window):
        """
        Sends packets from the sliding window.

        Args:
            sliding_window (list): A list of tuples representing the packet number and data.

        """
        for packet_no, data in sliding_window:
            if packet_no not in self.__already_sent:
                # Add error correction and add packet to the list
                data = error_correction.add_parity(data)
                SharedVariable.add_to_packet_list(packet_no, data)
                self.__already_sent.append(packet_no)
                print(f"Sent: packet Number: {packet_no}")

    # Method to remove packets that are already sent
    def removeAlreadySent(self, packet_numbers):
        """
        Removes packets that are already sent.

        Args:
            packet_numbers (list): A list of packet numbers to be removed.

        """
        for item in packet_numbers:
            self.__already_sent.remove(item)

    # Method to handle acknowledgment
    def ACK(self):
        """
        Handles acknowledgment.

        Returns:
            int: The current sent acknowledgment.

        """
        if SharedVariable.current_sent_ACK not in self.already_recieved_ACK:
            self.already_recieved_ACK.append(SharedVariable.current_sent_ACK)
        return SharedVariable.current_sent_ACK

# Receiver class, inheriting from SharedList
class Reciever(SharedList):
    """
    The Reciever class represents a receiver in a flow control error correction protocol.

    Attributes:
        AllData (dict): Dictionary to hold received data.

    Methods:
        recieve(): Method to receive packets.
    """

    AllData = {-1: ""}  # Dictionary to hold received data

    # Method to receive packets
    def recieve(self):
        """
        Receive packets and process them.

        This method iterates over the packet list and checks for errors in the received data.
        If the data is error-free, it removes the parity bits, stores the data in the AllData dictionary,
        and sends an acknowledgment. If the data is corrupted, it sends a negative acknowledgment.

        Returns:
            None
        """
        for packet_number, data in SharedVariable.packet_list:
            if packet_number not in self.AllData:
                # Check for errors and process data
                if packet_number not in self.AllData:
                    if(error_correction.check_parity(data) == 0):
                        SharedVariable.packet_list.remove([packet_number, data])
                        data = error_correction.remove_parity(data)
                        self.AllData[packet_number] = data
                        print(f"Received: {data}")
                        SharedVariable.current_sent_ACK = packet_number
                        print(f"Acknowledgment sent for sequence number: {packet_number}")
                        break  # To keep the window size of receiver 1
                    else:
                        print(f"Data corrupted: {data}")
                        SharedVariable.current_sent_ACK = -packet_number
                        print(f"NACK sent for sequence number: {packet_number}")
                        break

# Initial packet list
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

# Extract packet numbers from packet list
packet_no_list = [dataPacket[0] for dataPacket in packet_list]

# Instantiate sender and receiver objects
sender = Sender()
receiver = Reciever()

# Maximum delay for timeout
max_delay = 5

# Initialize time variables
start_time = current_time = time.time()

# Loop until all packets are received
while packet_no_list != sorted(sender.already_recieved_ACK):
    sent = False
    while(not sent):
        # Fill sliding window
        while len(sliding_window) < window_size and packet_list:
            sliding_window.append(packet_list.pop(0))
        
        # Check if within timeout
        while current_time - start_time < max_delay:
            if(sent):
                break
            sender.send(sliding_window)  # Send packets
            receiver.recieve()  # Receive packets
            # Check for acknowledgment
            for i in range(len(sliding_window)):
                packet_no = sliding_window[i][0]
                if sender.ACK() == packet_no:
                    print(f"Received ACK for packet no {packet_no}")
                    sliding_window.pop(i)
                    sent = True
                    break 
            current_time = time.time()
        else:
            # Timeout handling
            while(not sent):
                print("Timeout, Resending")
                sender.removeAlreadySent([sliding_window[0]])
        start_time = current_time = time.time()

# Remove the -1 entry from receiver's data
receiver.AllData.pop(-1)

# Print received data
print(receiver.AllData)
