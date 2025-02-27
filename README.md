# PyPrefix
A prefix list validator made with Python

PyPrefix is made with the goal of simplifying 'ip prefix-list' creation, primarily for Cisco L3 devices. Since, prefix-lists use 'ge' and 'le' operators, network admins may want a way to ensure that certain prefixes are permitted or denied based upon their needs. We all know about the BGP horror stories where prefixes are falsely accepted or advertised. The aim of this script is to just be another tool to check subnetting/prefixes when filtering potential routing updates.

<a href="https://hub.docker.com/r/ryanv203/pyprefix" target="_blank">DockerHub link to PyPrefix image</a>
