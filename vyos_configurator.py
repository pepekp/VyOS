"""
VyOS router configuration tool will generate VyOS configuration for customer premise equipment and upload and commit
configuration to the router.
WAN - connection to ISP router
LAN - connection to end customer router, switch or firewall.
Option description:
 - Primary and Backup options require dynamic routing protol on the WAN side. VRRP is optional and might be replaced with
  link state protocol or dynamic routing protocol on the LAN side. Static routes and OSPF always require BGP with
  ISP router to redistribute routes.  
 such as DHCP server, DHCP Relay, SNMP, Netflow are available if they are required.
 - Standalone option will generate configuration only with LAN side subnet and default route. All protocols
 such as DHCP server, DHCP Relay, SNMP, Netflow are available if they are required.
 
Each protocol in inventory file has on/off switch, 0 = off, 1 = on. Jinja2 template logic is based on those switches and
device role selected at the beginning of the script.   
"""

from getpass import getpass
from netmiko import ConnectHandler
import jinja2
import yaml
import ipaddress

def configurator():
    options = ('p', 'b', 's', 'x')
    while True:
        print("*** SELECT OPTION ***")
        print()
        print('p = Primary')
        print('b = Backup')
        print('s = Standalone')
        print('x = EXIT')
        print()
        user_input = input('Enter an option: ')
        if user_input in options:
            if user_input == 'p':
                role = 'primary'
            elif user_input == 'b':
                role = 'secondary'
            elif user_input == 's':
                role = 'standalone'
            elif user_input == 'x':
                exit()
            # Load inventory vars

            router_ip = input('Router IP: ')
            vyos_username = input('Router username: ')
            vyos_password = getpass('Router password: ')
            with open('inventory.yml', 'r') as yf:
                data = yaml.full_load(yf)

            hostname = data.get('hostname')
            wan_subnet = data.get('wan_subnet')
            # lan_subnet = data.get('lan_subnet')
            lan_ip = data.get('lan_ip')
            wan_interface = data.get('wan_interface')
            lan_interface = data.get('lan_interface')
            # static_route = data.get('static_route')
            static_route_networks = data.get('static_route_networks')
            next_hop = data.get('next_hop')
            # IP address calc
            wan_ip = ipaddress.ip_network(wan_subnet).network_address +3  # Return router WAN interface IP
            nbr_ip = ipaddress.ip_network(wan_subnet).network_address +1  # Return BGP neighbor IP
            lan_ipaddr = ipaddress.ip_interface(lan_ip).ip # Return LAN IP without /


            with open('cfg_template.j2', 'r') as j:
                cfg = j.read()
            template = jinja2.Template(cfg)
            cfg = template.render(role=role, hostname=hostname, wan_interface=wan_interface, lan_interface=lan_interface,
                            wan_interface_descr=data.get('wan_interface_descr'), lan_interface_descr=data.get('lan_interface_descr'),
                            nbr_ip=nbr_ip, lan_ipaddr=lan_ipaddr, lan_subnet=data.get('lan_subnet'), lan_ip=data.get('lan_ip'),
                            static_route=data.get('static_route'), static_route_networks=static_route_networks, next_hop=next_hop,
                            bgp=data.get('bgp'), wan_ip=wan_ip, asn=data.get('asn'), remote_asn=data.get('remote_asn'),
                            ce_asn=data.get('ce_asn'), ospf=data.get('ospf'), ospf_area=data.get('ospf_area'),
                            dhcp_relay=data.get('dhcp_relay'), dhcp_relay_ip=data.get('dhcp_relay_ip'), dhcp_server=data.get('dhcp_server'),
                            dhcp_start=data.get('dhcp_start'), dhcp_end=data.get('dhcp_end'), snat=data.get('snat'),
                            dnat=data.get('dnat'), vrrp=data.get('vrrp'), vip=data.get('vip'), netflow_server=data.get('netflow_server'),
                            netflow=data.get('netflow')).strip().split('\n')

            #print(cfg)
            for i in cfg:
                print(i)

            user_validate = input('Do you want to continue with router configuration? yes/no ')
            if user_validate == 'yes':
                vyos_router = {
                    "device_type": "vyos",
                    "host": router_ip,
                    "username": vyos_username,
                    "password": vyos_password,
                    "port": 22,
                }

                net_connect = ConnectHandler(**vyos_router)
                # set configuration
                output = net_connect.send_config_set(cfg, exit_config_mode=False)
                print(output)
                # commit configuration
                output = net_connect.commit()
                print(output)
                #print(output)
            else:
                pass


        else:
            print('OPTION NOT AVAILABLE')
            break

configurator()
