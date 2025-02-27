 PyPrefix - IP Prefix-List checker for Cisco networking devices

# Author: Ryan Viglione

from netaddr import IPNetwork
import ipaddress
import pyfiglet

def prefix_list_checker():
    PyPrefix_title = pyfiglet.figlet_format("PyPrefix")
    print(PyPrefix_title)

    print(" ~~~~ Input a IPV4 subnet in CIDR notation to test a prefix list. ~~~~\n")

    while True:
        subnet = input(
            "ip prefix-list TEST permit ______________ ge __ le __")  # user specifies supernet to validate prefixes against

        try:
            ipaddress.ip_network(subnet)  # validate supernet formatting to be a prefix with subnet expressed in CIDR
            break  # break loop if above condition is met
        except ValueError:  # throw exception if prefix is not in prefix + CIDR format (example - 192.168.10.0/24)
            print(f"{subnet} is not a valid subnet with CIDR notation.")

    while True:

        print(" ~~~~ Input a greater than mask length. ~~~~\n")

        greater_than_mask = (
            input(f"ip prefix-list TEST permit {subnet} ge __ le __"))  # user specifies greater than mask

        try:
            greater_than_mask = int(greater_than_mask)
            if 0 <= greater_than_mask <= 32:
                break
            elif greater_than_mask > 32:
                print(f"Input {greater_than_mask} is out of valid range.")
        except ValueError:
            print(f"{greater_than_mask} is not a valid integer!")

    while True:

        print(" ~~~~ Input a less than mask length. ~~~~\n")

        less_than_mask = int(input(f"ip prefix-list TEST permit {subnet} ge {greater_than_mask} le __"))

        try:
            less_than_mask = int(less_than_mask)
            if 0 <= less_than_mask <= 32:
                break
            elif less_than_mask > 32:
                print(f"Input {less_than_mask} is out of valid range.")
        except ValueError:
            print(f"{less_than_mask} is not a valid integer!")

    full_statement = f"ip prefix-list TEST permit {subnet} ge {greater_than_mask} le {less_than_mask}"

    print(full_statement)

    subnet_lists = []

    while True:
        subnet_inputs = input(f"Add prefixes to check against {full_statement}.")

        if subnet_inputs == "done":
            break

        try:
            ipaddress.ip_network(subnet_inputs)
            subnet_lists.append(subnet_inputs)
        except ValueError:
            print(f"{subnet_inputs} is not a valid subnet with CIDR notation.")

        for network in subnet_lists:
            mask = int(network.split("/", 1)[1])

            if IPNetwork(network) in IPNetwork(subnet) and greater_than_mask <= mask <= less_than_mask:
                print(f"Yes, {network} is in {subnet} and meets the criteria of {full_statement}")
                subnet_lists.remove(subnet_inputs)
            elif IPNetwork(network) in IPNetwork(subnet):
                print(
                    print(f"The {network} network is in {subnet}, but doesn't meet the comparison operator criteria."))
            else:
                print(f"No, {network} does not meet the criteria of {full_statement}.")

if __name__ == "__main__":
    prefix_list_checker()
