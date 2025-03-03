# PyPrefix - IP Prefix-List checker for Cisco networking devices

# Author: Ryan Viglione

from ipaddress import *
import ipaddress
from netaddr import IPNetwork
import pyfiglet
import cymruwhois
import socket
from cymruwhois import Client
import os

# import ipaddress
#
# for i in ipaddress.ip_network('10.0.0.0/8').subnets(new_prefix=22):
#     print(i)

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

        print(f"Input a greater than mask length that is larger than {main_mask}.\n")

        greater_than_mask = (
            input(f"Input here: "))  # user specifies greater than mask

        try:
            if main_mask > int(greater_than_mask):
                print(f"\n% Invalid prefix range for {subnet}, make sure: len < ge-value <= le-value\n")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            elif int(greater_than_mask) > 32:
                print(f"Input {greater_than_mask} is out of valid range.\n")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            else:
                break
        except ValueError:
            print(f"\n{greater_than_mask} is not a valid integer!")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    while True:

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        less_than_mask = input("Input a less than mask length: ")


        try:
            if main_mask > int(less_than_mask):
                print(f"% Invalid prefix range for {subnet}, make sure: len < ge-value <= le-value\n")
            elif int(less_than_mask) < int(greater_than_mask):
                print(f"% Invalid prefix range for {subnet}, make sure: len < ge-value <= le-value\n")
            elif int(less_than_mask) > 32:
                print(f"\nInput {less_than_mask} is out of valid range.")
            else:
                break
        except ValueError:
            print(f"\n{less_than_mask} is not a valid integer!")

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

            if IPNetwork(network) in IPNetwork(subnet) and int(greater_than_mask) <= int(mask) <= int(less_than_mask):
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
