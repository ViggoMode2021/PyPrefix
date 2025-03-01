# PyPrefix - IP Prefix-List checker for Cisco networking devices

# Author: Ryan Viglione

from ipaddress import *
import ipaddress
from netaddr import IPNetwork
import pyfiglet
import cymruwhois
import socket
from cymruwhois import Client

# MAKE SURE TO FIX NOTED LINES TO MAKE SURE THAT THE GREATER THAN MASK IS NOT LARGER THAN REGULAR SUBNET MASK

def prefix_list_checker():

    pyprefix_title = pyfiglet.figlet_format("PyPrefix")
    print(pyprefix_title)

    print("Input a IPV4 subnet in CIDR notation to test a prefix list.\n")

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    while True:
        subnet = input(
            "Input here: ")  # User specifies subnet to validate prefixes against

        try:
            ipaddress.ip_network(subnet)  # Validate subnet format to be a prefix with mask in CIDR
            break
        except ValueError:  # Throw exception if prefix is not in prefix + CIDR format (example - 192.168.10.0/24)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(f"\n{subnet} is not a valid subnet with CIDR notation.\n")

    while True:

        if ip_address(IPNetwork(subnet).broadcast).is_private:
            print(f"\n{subnet} is a private IPV4 address range.")
        else:
            print(f"\n{subnet} is a public IPV4 address range.")

        socket_client = Client()

        prefix_network = IPNetwork(subnet)

        broadcast_of_prefix_network = prefix_network.broadcast

        broadcast_of_prefix_network_search = socket_client.lookup(broadcast_of_prefix_network)

        prefix_asn = broadcast_of_prefix_network_search.asn

        prefix_owner = broadcast_of_prefix_network_search.owner

        if prefix_asn == "NA" and prefix_owner == "NA":
            print(f"\nThe prefix {subnet} does not belong to an Autonomous System, according to Cymruwhois.\n")
            break
        else:
            print(f"\nThe prefix {subnet} belongs to Autonomous System # {prefix_asn} {prefix_owner}.\n")
            break

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    while True:

        main_mask = int(subnet.split("/", 1)[1])

        print(f"Input a greater than mask length that is less than {main_mask}.\n")

        greater_than_mask = (
            input(f"Input here: \n"))  # user specifies greater than mask

        try:
            if main_mask > int(greater_than_mask):
                print(f"% Invalid prefix range for {subnet}, make sure: len < ge-value <= le-value")
            elif int(greater_than_mask) > 32:
                print(f"\nInput {greater_than_mask} is out of valid range.")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            else:
                break
        except ValueError:
            print(f"\n{greater_than_mask} is not a valid integer!")

    while True:

        print("Input a less than mask length.\n")

        less_than_mask = int(input(f"ip prefix-list TEST permit {subnet} ge {greater_than_mask} le __\n"))

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        try:
            less_than_mask = int(less_than_mask)
            if 0 <= less_than_mask <= 32:
                break
            elif less_than_mask > 32:
                print(f"Input {less_than_mask} is out of valid range.\n")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        except ValueError:
            print(f"{less_than_mask} is not a valid integer!\n")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    full_statement = f"ip prefix-list TEST permit {subnet} ge {greater_than_mask} le {less_than_mask}\n"

    print(full_statement)

    subnet_lists = []

    while True:
        subnet_inputs = input(f"Add prefixes to check against {full_statement}\n")

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        if subnet_inputs == "done":
            break

        try:
            ipaddress.ip_network(subnet_inputs)
            subnet_lists.append(subnet_inputs)

            socket_client = Client()

            prefix_network = IPNetwork(subnet_inputs)

            broadcast_of_prefix_network = prefix_network.broadcast

            broadcast_of_prefix_network_search = socket_client.lookup(broadcast_of_prefix_network)

            prefix_asn = broadcast_of_prefix_network_search.asn

            prefix_owner = broadcast_of_prefix_network_search.owner

            print(f"The prefix {subnet_inputs} belongs to Autonomous System # {prefix_asn} {prefix_owner}\n")

            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        except ValueError:
            print(f"{subnet_inputs} is not a valid subnet with CIDR notation.\n")

            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        for network in subnet_lists:
            mask = int(network.split("/", 1)[1])

            if IPNetwork(network) in IPNetwork(subnet) and greater_than_mask <= mask <= less_than_mask:
                print(f"Yes, {network} is in {subnet} and meets the criteria of {full_statement}\n")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                subnet_lists.remove(subnet_inputs)
            elif IPNetwork(network) in IPNetwork(subnet):
                print(f"The {network} network is in {subnet}, but doesn't meet the comparison operator criteria.\n")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            else:
                print(f"No, {network} does not meet the criteria of {full_statement}\n.")

if __name__ == "__main__":
    prefix_list_checker()
