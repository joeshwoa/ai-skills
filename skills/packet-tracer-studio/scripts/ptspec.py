#!/usr/bin/env python3
"""ptspec — check a Packet Tracer topology spec before building it, or print a paste-ready lab guide.

The spec is the same JSON that the pt_build_topology tool takes:
  {devices:[{name,deviceType,model,x,y}], links:[{device1,port1,device2,port2,cableType}],
   iosConfigs:{name:[cmds]}, hostConfigs:[{device,portName,ip,mask,gateway,dns,dhcp}], notes, savePath}

Usage:
  ptspec.py check SPEC.json     # exit 0 = no errors (warnings allowed), 1 = errors
  ptspec.py guide SPEC.json     # addressing table + per-device CLI, for manual paste when Packet Tracer is not reachable

Checks: duplicate names, unknown devices in links, port names that do not exist on a known model, a port used
twice, cable type vs device pair, duplicate IPs, host/gateway in the wrong subnet, overlapping subnets,
IOS blocks missing enable/configure terminal/end/write memory, DHCP hosts. Unknown models are warned about, never
rejected: the real port list always comes from pt_list_devices after the device is placed.
"""
import ipaddress
import json
import re
import sys

def rng(fmt, a, b):
    return [fmt.format(i) for i in range(a, b + 1)]

PORTS = {
    "2911": rng("GigabitEthernet0/{}", 0, 2),
    "1941": rng("GigabitEthernet0/{}", 0, 1),
    "2811": rng("FastEthernet0/{}", 0, 1),
    "4321": rng("GigabitEthernet0/0/{}", 0, 1),
    "ISR4331": rng("GigabitEthernet0/0/{}", 0, 1) + ["GigabitEthernet0"],
    "2960-24TT": rng("FastEthernet0/{}", 1, 24) + rng("GigabitEthernet0/{}", 1, 2),
    "3560-24PS": rng("FastEthernet0/{}", 1, 24) + rng("GigabitEthernet0/{}", 1, 2),
    "3650-24PS": rng("GigabitEthernet1/0/{}", 1, 24) + rng("GigabitEthernet1/1/{}", 1, 4),
    "PC-PT": ["FastEthernet0"],
    "Server-PT": ["FastEthernet0"],
    "Laptop-PT": ["FastEthernet0"],
    "5505": rng("Ethernet0/{}", 0, 7),
}
ROUTERS = {"2911", "1941", "2811", "4321", "ISR4331"}
SWITCHES = {"2960-24TT", "3560-24PS", "3650-24PS"}
HOSTS = {"PC-PT", "Server-PT", "Laptop-PT"}
ABBR = {"fa": "FastEthernet", "gi": "GigabitEthernet", "gig": "GigabitEthernet", "eth": "Ethernet", "se": "Serial"}


def canon(port):
    m = re.match(r"^([A-Za-z]+)\s*([\d/\.]+)$", port.strip())
    if not m:
        return port.strip()
    word, num = m.group(1), m.group(2)
    full = ABBR.get(word.lower())
    if full:
        return full + num
    return word[0].upper() + word[1:] + num


def kind(model):
    if model in ROUTERS:
        return "router"
    if model in SWITCHES:
        return "switch"
    if model in HOSTS:
        return "host"
    return "other"


def parse_ios_ips(name, cmds):
    """Yield (interface, ip, mask) found in 'interface X' / 'ip address A M' command sequences."""
    iface = None
    for c in cmds:
        c = c.strip()
        m = re.match(r"^interface\s+(\S+(?:\s+\S+)?)$", c, re.I)
        if m and not c.lower().startswith("interface range"):
            iface = canon(m.group(1).replace(" ", ""))
            continue
        if re.match(r"^(exit|end|router |ip dhcp pool)", c, re.I):
            iface = None if c.lower().startswith(("exit", "end")) else iface
        m = re.match(r"^ip address\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)$", c, re.I)
        if m and iface:
            yield iface, m.group(1), m.group(2)


def check(spec):
    errs, warns = [], []
    devs = {d["name"]: d for d in spec.get("devices", [])}
    if len(devs) != len(spec.get("devices", [])):
        errs.append("duplicate device names")
    for d in devs.values():
        if d["model"] not in PORTS:
            warns.append(f"{d['name']}: model {d['model']!r} not in my port table; confirm ports with pt_list_devices")
    used = {}
    for l in spec.get("links", []):
        for side in ("1", "2"):
            dn, pn = l["device" + side], canon(l["port" + side]) if l["port" + side].upper() != "AUTO" else "AUTO"
            if dn not in devs:
                errs.append(f"link uses unknown device {dn!r}")
                continue
            model = devs[dn]["model"]
            if pn != "AUTO" and model in PORTS and pn not in PORTS[model]:
                errs.append(f"{dn} ({model}) has no port {pn}")
            if pn != "AUTO":
                if (dn, pn) in used:
                    errs.append(f"{dn} {pn} is used by two links")
                used[(dn, pn)] = True
        a, b = devs.get(l["device1"]), devs.get(l["device2"])
        cable = l.get("cableType", "ETHERNET_STRAIGHT")
        if a and b and cable != "AUTO" and cable.startswith("ETHERNET"):
            ka, kb = kind(a["model"]), kind(b["model"])
            same = (ka == kb and ka in ("router", "switch", "host")) or {ka, kb} == {"router", "host"}
            if same and cable == "ETHERNET_STRAIGHT":
                warns.append(f"{a['name']}-{b['name']}: same-type devices usually need ETHERNET_CROSS (or AUTO)")
            if not same and ka != "other" and kb != "other" and cable == "ETHERNET_CROSS":
                warns.append(f"{a['name']}-{b['name']}: different device types usually need ETHERNET_STRAIGHT")
    # IPs
    ips = []  # (owner, ip, mask)
    for h in spec.get("hostConfigs", []):
        if h.get("dhcp"):
            continue
        if h.get("ip"):
            ips.append((h["device"], h["ip"], h.get("mask", "255.255.255.0")))
            try:
                net = ipaddress.ip_network(f"{h['ip']}/{h.get('mask', '255.255.255.0')}", strict=False)
                ip = ipaddress.ip_address(h["ip"])
                if ip in (net.network_address, net.broadcast_address):
                    errs.append(f"{h['device']}: {ip} is the network/broadcast address of {net}")
                if h.get("gateway") and ipaddress.ip_address(h["gateway"]) not in net:
                    errs.append(f"{h['device']}: gateway {h['gateway']} is outside {net}")
            except ValueError as e:
                errs.append(f"{h['device']}: bad address ({e})")
        elif not h.get("gateway"):
            warns.append(f"{h['device']}: hostConfig without ip or dhcp")
    for name, cmds in (spec.get("iosConfigs") or {}).items():
        if name not in devs:
            errs.append(f"iosConfigs for unknown device {name!r}")
            continue
        low = [c.strip().lower() for c in cmds]
        if not low or low[0] != "enable":
            warns.append(f"{name}: first command should be 'enable'")
        if "configure terminal" not in low and "conf t" not in low:
            warns.append(f"{name}: no 'configure terminal'")
        if "end" not in low:
            warns.append(f"{name}: should finish with 'end'")
        if "write memory" not in low and "copy running-config startup-config" not in low:
            warns.append(f"{name}: should finish with 'write memory' or the config is lost on reload")
        hn = [c.split(None, 1)[1] for c in cmds if c.lower().startswith("hostname ")]
        if hn and hn[0] != name:
            warns.append(f"{name}: hostname {hn[0]!r} differs from the device name")
        if kind(devs[name]["model"]) == "switch" and any("switchport trunk encapsulation" in c.lower() for c in cmds) \
                and devs[name]["model"] == "2960-24TT":
            errs.append(f"{name}: 2960 has no 'switchport trunk encapsulation' (dot1q only); remove it (3560/3650 need it)")
        for iface, ip, mask in parse_ios_ips(name, cmds):
            ips.append((f"{name} {iface}", ip, mask))
    seen = {}
    for owner, ip, mask in ips:
        if ip in seen:
            errs.append(f"duplicate IP {ip}: {seen[ip]} and {owner}")
        seen[ip] = owner
    nets = []
    for owner, ip, mask in ips:
        try:
            nets.append((owner, ipaddress.ip_network(f"{ip}/{mask}", strict=False)))
        except ValueError as e:
            errs.append(f"{owner}: bad address ({e})")
    for i in range(len(nets)):
        for j in range(i + 1, len(nets)):
            a, b = nets[i][1], nets[j][1]
            if a != b and a.overlaps(b):
                errs.append(f"overlapping subnets: {nets[i][0]} {a} and {nets[j][0]} {b}")
    if any(h.get("dhcp") for h in spec.get("hostConfigs", [])):
        warns.append("DHCP hosts present: after fast_forward, re-run pt_configure_host dhcp:true for each so they ask once STP is forwarding")
    return errs, warns


def guide(spec):
    out = ["# Lab guide (generated from spec)", "", "## Devices"]
    for d in spec.get("devices", []):
        out.append(f"- {d['name']}: {d['deviceType']} {d['model']}")
    out += ["", "## Cabling"]
    for l in spec.get("links", []):
        out.append(f"- {l['device1']} {l['port1']}  <->  {l['device2']} {l['port2']}  ({l.get('cableType', 'ETHERNET_STRAIGHT')})")
    out += ["", "## Addressing"]
    for h in spec.get("hostConfigs", []):
        if h.get("dhcp"):
            out.append(f"- {h['device']}: DHCP")
        else:
            out.append(f"- {h['device']}: {h.get('ip')} {h.get('mask')} gw {h.get('gateway', '-')} dns {h.get('dns', '-')}")
    for name, cmds in (spec.get("iosConfigs") or {}).items():
        out += ["", f"## {name} (paste into its CLI)", "```"] + list(cmds) + ["```"]
    return "\n".join(out)


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("check", "guide"):
        print(__doc__)
        return 2
    spec = json.load(open(sys.argv[2]))
    if sys.argv[1] == "guide":
        print(guide(spec))
        return 0
    errs, warns = check(spec)
    for e in errs:
        print("ERROR  ", e)
    for w in warns:
        print("warning", w)
    print(f"{len(errs)} error(s), {len(warns)} warning(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
