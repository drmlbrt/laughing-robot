"""
This is a python script where I tried to use the netmask logic to find the network, first and last host.
In a second venture I added 'subnet' calculation
27-10-21 new_branch add new-feature subnetting based on hosts
"""


def and_operator(splitted_binary_subnetmask, splitted_binary_ipaddress):
    """This is the AND operation, where two lists are zipped. The 'ampesand' is the AND operator in python"""
    new_list = [se & so for se, so in zip(splitted_binary_subnetmask, splitted_binary_ipaddress)]
    return new_list


def complete_binary_bits(network_octet1, network_octet2, network_octet3, network_octet4):
    converted = []
    binary_address = [network_octet1, network_octet2, network_octet3, network_octet4]
    """Adding trailing zero's"""

    for octet in binary_address:
        if len(octet) < 8:
            trailing_zero = 8 - len(octet)
            corrected_binary_octet = str(trailing_zero * "0") + str(octet)
            converted.append(corrected_binary_octet)
        else:
            converted.append(octet)
    return converted


def chop_string_octets_to_bits(binary_address):
    long_binary_string = "".join(binary_address)
    binary_subnet = [int(long_binary_string[i:i + 1]) for i in range(0, len(long_binary_string), 1)]
    # print(f"This is the chopped binary string {binary_subnet}")
    return binary_subnet


def convert_bits_to_octets(subnetstring):
    octets_subnet = [subnetstring[i:i + 8] for i in range(0, len(subnetstring), 8)]
    # print(f"This is the convert bits to octets {octets_subnet} ")
    return octets_subnet


def convert_to_binary(decimal):
    octet1 = "{0:b}".format(int(decimal[0]))
    octet2 = "{0:b}".format(int(decimal[1]))
    octet3 = "{0:b}".format(int(decimal[2]))
    octet4 = "{0:b}".format(int(decimal[3]))
    return [octet1, octet2, octet3, octet4]


def convert_to_decimal(binary):
    # print(f"This is the provided binary string to convert to decimal {binary}")
    decimal = []
    for octet in binary:
        bits = [char for char in octet]
        calculate = (pow(2, 7) * (int(bits[0]))) + (pow(2, 6) * (int(bits[1]))) + (pow(2, 5) * (int(bits[2]))) + (
                pow(2, 4) * (int(bits[3]))) + (pow(2, 3) * (int(bits[4]))) + (pow(2, 2) * (int(bits[5]))) + (
                            pow(2, 1) * (int(bits[6]))) + (pow(2, 0) * (int(bits[7])))
        decimal.append(calculate)
    subnet = f"{decimal[0]}.{decimal[1]}.{decimal[2]}.{decimal[3]}"
    return subnet


def split_ip_address(address):
    all_octets = address.split(".")
    octet1 = all_octets[0]
    octet2 = all_octets[1]
    octet3 = all_octets[2]
    octet4 = all_octets[3]
    return [octet1, octet2, octet3, octet4]


def first_host(subnet, host_bits, network_bits):
    """The method should convert all host reserved bits to '0' except the last = '1' """
    """We receive a list of subnet bits"""
    try:
        if len(subnet) == 32:

            n = int(network_bits)
            h = int(host_bits)
            partial_subnet=(subnet[0:n])
            first_host_bits = ['0' for _ in range(h)]
            first_host_bits[-1] = '1'
            first_host_ = partial_subnet + first_host_bits
            octets_first_host_  = convert_bits_to_octets(first_host_)
            decimal_first_host_ = convert_to_decimal(octets_first_host_)
            return decimal_first_host_
        else:
            print("error with subnet length provided to function first_host()")
        pass
    except Exception as e:
        print(f"{e}: check you subnet a /31 or /32 is not calculated")


def last_host(subnet, host_bits, network_bits):
    """The method should convert all host reserved bits to '1' except the last = '0' """
    try:
        if len(subnet) == 32:

            n = int(network_bits)
            h = int(host_bits)
            partial_subnet = (subnet[0:n])
            first_host_bits = ['1' for _ in range(h)]
            first_host_bits[-1] = '0'
            first_host_ = partial_subnet + first_host_bits
            octets_first_host_ = convert_bits_to_octets(first_host_)
            decimal_first_host_ = convert_to_decimal(octets_first_host_)
            return decimal_first_host_
        else:
            print("error with subnet length provided to function last_host()")
        pass
    except Exception as e:
        print(f"{e}: check you subnet a /31 or /32 is not calculated")

def broadcast_(subnet, host_bits, network_bits):
    """The method should convert all host reserved bits to '1' """
    try:
        if len(subnet) == 32:

            n = int(network_bits)
            h = int(host_bits)
            partial_subnet = (subnet[0:n])
            first_host_bits = ['1' for _ in range(h)]
            first_host_ = partial_subnet + first_host_bits
            octets_first_host_ = convert_bits_to_octets(first_host_)
            decimal_first_host_ = convert_to_decimal(octets_first_host_)
            return decimal_first_host_
        else:
            print("error with subnet length provided to function broadcast_host()")
        pass
    except Exception as e:
        print(f"{e}: check you subnet a /31 or /32 is not calculated")


def flip(*args):
    flipped_octet = []
    for arg in args:
        octet_for_change = [char for char in arg]
        for item in octet_for_change:
            if item == "0":
                flipped_octet.append(1)
            else:
                flipped_octet.append(0)
    return flipped_octet


def wildcard_mask(subnetmask):
    # binary flip ?
    wildcard = []
    flippedwildcard = []

    for octet in subnetmask:
        flipped = flip(octet)
        wildcard.append(flipped)
    for item in wildcard:
        newoctect = "".join(map(str, item))
        flippedwildcard.append(newoctect)
    return convert_to_decimal(flippedwildcard)


class Subnetfinder:

    number_of_bits = 32

    def __init__(self, octet1, octet2, octet3, octet4, network_bits, host_bits):
        self.octet1 = octet1
        self.octet2 = octet2
        self.octet3 = octet3
        self.octet4 = octet4
        self.network_bits = network_bits
        self.host_bits = host_bits

    def find_network(self):
        """AND operation where 1 AND 1 = 1, 0 AND 1 = 0 # The final result is the network where the 'Host is in'"""
        """FIRST create a subnet mask in binary derived from CIDR notation /**"""

        if int(self.host_bits) + int(self.network_bits) == 32:
            network_binary = (int(self.network_bits) * "1") + (int(self.host_bits) * "0")
            # print(network_binary)
            network_octets = [network_binary[i:i+8] for i in range(0, len(network_binary), 8)]
            # print(network_octets)

            netmask_octet1 = network_octets[0]
            netmask_octet2 = network_octets[1]
            netmask_octet3 = network_octets[2]
            netmask_octet4 = network_octets[3]
        else:
            return print("Something went wrong with the CIDR notation")
        pass
        """SECOND create a provided decimal IP ADDRESS to binary"""

        ip_address = [self.octet1, self.octet2, self.octet3, self.octet4]
        convert_ip_address = convert_to_binary(ip_address)

        """Add zeros to the binary conversion so that it complies to 8 bits octet"""
        completed_ip_address = complete_binary_bits(*convert_ip_address)

        network_octet1 = completed_ip_address[0]
        network_octet2 = completed_ip_address[1]
        network_octet3 = completed_ip_address[2]
        network_octet4 = completed_ip_address[3]

        # print(f"This is your IP address in binary: {network_octet1}."
                     # f"{network_octet2}.{network_octet3}.{network_octet4}/{self.network_bits}")

        subnetmask = [netmask_octet1, netmask_octet2, netmask_octet3, netmask_octet4]
        ipaddress = [network_octet1, network_octet2, network_octet3, network_octet4]

        """It has to chop the network octets to integer bits for further processing"""
        splitted_subnetmask = chop_string_octets_to_bits(subnetmask)
        splitted_ipaddress = chop_string_octets_to_bits(ipaddress)

        """This is the AND operation, where two lists are zipped. The 'ampesand' is the AND operator in python"""
        subnet = and_operator(splitted_subnetmask, splitted_ipaddress)

        subnet_octets = convert_bits_to_octets(subnetstring=subnet)

        decimal_subnet = convert_to_decimal(binary=subnet_octets)

        """Here we pass the list of integer bits to find the first and last host and broadcast address"""
        firsthost = first_host(subnet, self.host_bits, self.network_bits)
        lasthost = last_host(subnet, self.host_bits, self.network_bits)
        broadcast = broadcast_(subnet, self.host_bits, self.network_bits)
        decimal_subnetmask = convert_to_decimal(binary=subnetmask)
        wildcard = wildcard_mask(subnetmask)

        return print(f"\n\nThis is your INPUT: {self.octet1}.{self.octet2}.{self.octet3}.{self.octet4}/{self.network_bits}"
                     f"\n\nThis is the network of the Provided IP ADDRESS: {decimal_subnet}"
                     f"\n This is the network Subnetmask     : {decimal_subnetmask}"
                     f"\n This is the network Wildcardmask   : {wildcard}"
                     f"\n\n This is the network FIRST host     : {firsthost}"
                     f"\n This is the network LAST host      : {lasthost}"
                     f"\n This is the network BROADCAST host : {broadcast}")


    @classmethod
    def ip_address(cls, address):
        """Deconstruct the IP address to all octets and subnet bits and host bits. This enables further processing later."""
        ip, network_bits = address.split("/")
        all_octets = ip.split(".")
        octet1 = all_octets[0]
        octet2 = all_octets[1]
        octet3 = all_octets[2]
        octet4 = all_octets[3]
        host_bits = int(cls.number_of_bits) - int(network_bits)
        ip = {"octet1": octet1,
              "octet2": octet2,
              "octet3": octet3,
              "octet4": octet4,
              "network_bits": network_bits,
              "host_bits": host_bits}
        return cls(**ip)

    def __str__(self):
        return f"This is your address in the class {self.octet1}.{self.octet2}.{self.octet3}.{self.octet4}/{self.network_bits}"


class Subnet_On_Hosts(Subnetfinder):
    def __init__(self, address, hosts):
        super().__init__(address)
        self.hosts = hosts #Should be a list of hosts from biggest to lowest

    def __str__(self):
        return f"{super().__str__()} : {self.hosts} provided for sunetting, for network"

    def hosts(self, *hosts):
        #here i probably need the ip-address and the provide 'large' enough subnet mask
        #provide a list of 'hosts' , per group of hosts create a subnet

address = input("What IP Address - Subnet would you like to calculate?: ip/cidr => ")
calculate_address = Subnetfinder.ip_address(address)
calculate_address.find_network()
