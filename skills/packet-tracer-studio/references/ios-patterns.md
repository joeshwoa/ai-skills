# IOS patterns for Packet Tracer 9 (copy, then change names and numbers)

Every block goes in a `pt_configure_ios` command list that starts with `enable`, `configure terminal` and ends with `end`, `write memory`. Interface lines are shown flat; keep `exit` between interfaces.

## VLANs, access and trunk ports
```
vlan 10
 name SALES
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 10
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20
```
Layer-2 switch 2960: no `switchport trunk encapsulation` (dot1q only). 3560/3650: add `switchport trunk encapsulation dot1q` BEFORE `switchport mode trunk`.
Native VLAN mismatch: set `switchport trunk native vlan 99` on both ends.

## Inter-VLAN routing
Router-on-a-stick (physical port `no shutdown`, no IP on it):
```
interface GigabitEthernet0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
```
Layer-3 switch (3560/3650):
```
ip routing
interface vlan 10
 ip address 192.168.10.1 255.255.255.0
 no shutdown
```
Routed uplink on an L3 switch: `no switchport`, then `ip address ...`.

## Spanning tree and EtherChannel
```
spanning-tree mode rapid-pvst
spanning-tree vlan 10 root primary
interface range FastEthernet0/23 - 24
 channel-group 1 mode active        ! LACP; use 'on' for static, 'desirable' for PAgP
interface Port-channel1
 switchport mode trunk
```
PortFast on edge ports: `spanning-tree portfast` + `spanning-tree bpduguard enable`.

## Static, default and dynamic routing
```
ip route 192.168.30.0 255.255.255.0 10.0.0.2
ip route 0.0.0.0 0.0.0.0 203.0.113.1
router ospf 1
 router-id 1.1.1.1
 network 10.0.12.0 0.0.0.3 area 0
 passive-interface GigabitEthernet0/2
 default-information originate
router eigrp 100
 network 10.0.0.0 0.0.0.255
 no auto-summary
router rip
 version 2
 no auto-summary
 network 192.168.1.0
```
Wildcard masks in OSPF/EIGRP (`0.0.0.255`), plain masks in `ip route`.

## DHCP, relay, DNS
```
ip dhcp excluded-address 192.168.10.1 192.168.10.9
ip dhcp pool LAN
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 198.51.100.10
interface GigabitEthernet0/0.20
 ip helper-address 10.0.0.1         ! relay to a DHCP server on another subnet
```
DNS records are set on the Server's DNS service (GUI); the MCP cannot edit server services, so say so and give the records to enter.

## NAT / PAT
```
interface GigabitEthernet0/0
 ip nat inside
interface GigabitEthernet0/1
 ip nat outside
access-list 1 permit 192.168.10.0 0.0.0.255
ip nat inside source list 1 interface GigabitEthernet0/1 overload
ip nat inside source static 192.168.10.50 203.0.113.10     ! static one-to-one
```
Check with `show ip nat translations`.

## ACLs
```
ip access-list extended BLOCK-HR
 deny ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255
 permit ip any any
interface GigabitEthernet0/0.20
 ip access-group BLOCK-HR in
```
Standard ACLs go closest to the destination, extended ACLs closest to the source. Every ACL ends with an implicit `deny any`.

## Management and hardening
```
service password-encryption
enable secret Cisco123
banner motd #Authorized access only#
ip domain-name lab.local
username admin secret Admin123
crypto key generate rsa modulus 1024
line vty 0 4
 login local
 transport input ssh
ip ssh version 2
interface FastEthernet0/5
 switchport port-security
 switchport port-security maximum 2
 switchport port-security violation restrict
 switchport port-security mac-address sticky
```
`crypto key generate rsa` can prompt for a modulus in some images: pass `modulus 1024` in the same line.

## First-hop redundancy
```
interface GigabitEthernet0/0
 ip address 192.168.10.2 255.255.255.0
 standby version 2
 standby 10 ip 192.168.10.1
 standby 10 priority 110
 standby 10 preempt
```

## Wireless
WRT300N / AP-PT are configured in the GUI. The MCP cannot set SSID or WPA2: tell the user the SSID/passphrase/channel to enter, and give the client config (DHCP from the wireless router).

## ASA 5505 (basic)
```
interface Vlan1
 nameif inside
 security-level 100
 ip address 192.168.1.1 255.255.255.0
interface Vlan2
 nameif outside
 security-level 0
 ip address 203.0.113.2 255.255.255.252
interface Ethernet0/0
 switchport access vlan 2
```
Then NAT (`object network`) and an ACL if the lab asks for inbound access.

## IPv6
```
ipv6 unicast-routing
interface GigabitEthernet0/0
 ipv6 address 2001:db8:10::1/64
 no shutdown
ipv6 route ::/0 2001:db8:12::2
```
Hosts: `pt_configure_host` sets IPv4 only; enable IPv6 on hosts in the GUI (auto-config) and say so.
