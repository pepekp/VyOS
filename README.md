# VyOS
VyOS router configuration tool 

VyOS router configuration tool will generate configuration based on Jinja2 template and upload configuration to VyOS router.
Supported protocols: BGP, OSPF, VRRP, DHCP, Netflow.  
WAN - connection to ISP router
LAN - connection to end customer router, switch or firewall.
Option description:
 - Primary and Backup options require dynamic routing protol on the WAN side. VRRP is optional and might be replaced with
  link state protocol or dynamic routing protocol on the LAN side.
 such as DHCP server, DHCP Relay, SNMP, Netflow are available if they are required.
 - Standalone option will generate configuration only with LAN side subnet and default route. All service
 such as DHCP server, DHCP Relay, SNMP, Netflow are available if they are required.
