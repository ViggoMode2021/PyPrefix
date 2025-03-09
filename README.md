# PyPrefix

PyPrefix is a prefix list checker written in Python. It checks subnets against a larger subnet/supernet, using the Cisco
'ip prefix-list permit (subnet) ge (mask) le (mask)' syntax as a reference.

### Dependencies

ipaddress
netaddr
pyfiglet
socket
cymruwhois

### Executing program

Run as a simple Python script, or pull and run from Docker Hub:

  docker pull pyprefix
  docker run --rm --interactive --tty pyprefix

## Authors

ex. Ryan Viglione 
ex. [@ViggoMode2021](https://github.com/ViggoMode2021/)

## Version History

* 0.1
