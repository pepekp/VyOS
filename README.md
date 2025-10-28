## VyOS

### VyOS router configuration tool 

VyOS router configuration tool will generate configuration based on parameters provided by inventory file and upload configuration to VyOS router.
Supported protocols: BGP, OSPF, Static routes, VRRP, DHCP, SNAT, DNAT, Netflow.  
WAN - connection to ISP router
LAN - connection to end customer router, switch or firewall.
### Option description:
 - Primary and Backup options require dynamic routing protol on the WAN side. VRRP is optional and might be replaced with
  link state protocol or dynamic routing protocol on the LAN side. Static routes and OSPF always require BGP with
  ISP router to redistribute routes.
 such as DHCP server, DHCP Relay, SNMP, Netflow are available if they are required.
 - Standalone option will generate configuration only with LAN side subnet and default route. All protocols
 such as DHCP server, DHCP Relay, SNMP, Netflow are available if they are required.

### Inventory file
Each protocol in inventory file has on/off switch, 0 = off, 1 = on. Jinja2 template logic is based on those switches and
device role selected at the beginning of the script.
