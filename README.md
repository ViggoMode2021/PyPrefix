PyPrefix - IP Prefix-List Checker for Cisco Networking Devices

Overview

PyPrefix is a Python-based tool designed to validate and check IP prefix lists for Cisco networking devices. It allows users to input IPv4 subnets in CIDR notation, analyze whether the subnet is private or public, retrieve Autonomous System (AS) information, and verify whether subnets meet prefix-list criteria.

Features

Validates IPv4 subnets in CIDR notation.

Checks if the subnet is private or public.

Queries CymruWhois to retrieve Autonomous System (AS) information.

Ensures subnet mask lengths comply with greater-than (ge) and less-than (le) prefix-list rules.

Allows users to add multiple subnets for validation against the prefix list.

Outputs a properly formatted Cisco prefix-list statement.

Requirements

PyPrefix requires the following Python libraries:

ipaddress

netaddr

pyfiglet

socket

cymruwhois

To install dependencies, run:

pip install netaddr pyfiglet cymruwhois

Usage

Run the script using Python:

python pyprefix.py

Example Workflow

Enter an IPv4 subnet in CIDR notation (e.g., 192.168.1.0/24).

The tool validates the subnet and adjusts if necessary (e.g., /31 and /32 are converted to /30).

The script determines if the subnet is private or public.

CymruWhois is queried to find AS information.

The user specifies greater-than (ge) and less-than (le) mask values for prefix validation.

The tool generates the corresponding Cisco prefix-list statement.

Users can enter additional subnets to check against the prefix list.

Example Output

PyPrefix

Input a IPV4 subnet in CIDR notation to test a prefix list.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Input here: 192.168.1.0/24

192.168.1.0/24 is a private IPv4 address range.

Input a greater than mask length that is larger than 24:
Input here: 25

Input a less than mask length that is greater than 25:
Input here: 30

Your prefix list is:
ip prefix-list TEST permit 192.168.1.0/24 ge 25 le 30

Add prefixes to check against ip prefix-list TEST permit 192.168.1.0/24 ge 25 le 30:
Input here: 192.168.1.128/26
Yes, 192.168.1.128/26 is in 192.168.1.0/24 and meets the criteria of ip prefix-list TEST permit 192.168.1.0/24 ge 25 le 30

Error Handling

Invalid subnets will prompt the user to re-enter the correct format.

CymruWhois lookup failures (e.g., no internet connection) will display an error but allow script continuation.

Ensures correct ordering of ge and le values for Cisco prefix-lists.

Author

Ryan Viglione

License

This project is open-source. Feel free to modify and distribute under the appropriate licensing terms.

