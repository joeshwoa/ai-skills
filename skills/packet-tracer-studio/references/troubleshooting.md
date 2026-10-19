# Troubleshooting a Packet Tracer lab (symptom, then what to check, in order)

Run the checks with `pt_configure_ios` (show commands) and `pt_pc_command`. Fix one thing, `fast_forward`, re-test.

| Symptom | Check |
|---|---|
| First ping times out, second works | ARP warm-up. Not a bug. Always ping twice before concluding. |
| PC cannot ping its own gateway | `ipconfig /all` on the PC (right IP, mask, gateway?). `show ip interface brief` on the gateway: interface up/up? VLAN of the switch port (`show vlan brief`). Cable type (straight vs crossover). |
| Link shows down/down | Wrong cable type, wrong port name, `shutdown` still on, device not powered/booted. |
| Interface up but line protocol down | Encapsulation mismatch, or the other end is shut. |
| Same VLAN works, other VLAN does not | Trunk (`show interfaces trunk`), allowed VLAN list, native VLAN, subinterface `encapsulation dot1Q N`, `ip routing` on L3 switch. |
| DHCP PCs show 169.254.x.x | Fast-forward first, then re-run `pt_configure_host dhcp:true`. Then `show ip dhcp binding`, excluded range, pool network, `ip helper-address` across subnets. |
| Routing: some LANs unreachable | `show ip route`, then `show ip protocols`; missing `network` statement; passive-interface on a transit link; wrong wildcard mask; no return route on the far side. |
| OSPF neighbours stuck in INIT/EXSTART | MTU, area, hello/dead timers, duplicate router-id, mask mismatch on the link. |
| NAT does not translate | `ip nat inside/outside` on the right interfaces, ACL matches the inside network, default route present, `show ip nat translations` after a ping. |
| ACL blocks everything | Implicit deny: add the `permit ip any any`; check direction (in/out) and that it is on the right interface. |
| Spanning-tree loop or flapping | `show spanning-tree`, make root explicit, use rapid-pvst. Only two links between two switches without EtherChannel will block one: that is correct. |
| `Invalid input detected` | Command not in this IOS image or wrong mode. Run `?` equivalent: try the shorter form, check the mode (config-if vs config), and for the 2960 drop commands it lacks (trunk encapsulation, `ip routing`). |
| Serial link impossible | 2911/1941/2811 have no serial ports until a WIC/HWIC module is installed (needs power off in the GUI; the MCP cannot add modules). Use a GigabitEthernet crossover link as the WAN and say so. |
| Config gone after reload | `write memory` was not sent. |
| pt_* tool returns no JSON / IPC not connected | Packet Tracer not running or IPC not listening: Extensions, IPC, Options, Always Listen On Start, port 39000, Start Listening. Signed in to Packet Tracer? |

Final verification set for a delivered lab: every host pings its gateway and one host in every other subnet; `show ip route` on each router lists every LAN; `show running-config` is saved; the `.pkt` file opens.
