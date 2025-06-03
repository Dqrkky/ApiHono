def ip_to_int(ip):
    parts = list(map(int, ip.strip().split('.')))
    if len(parts) != 4 or not all(0 <= p <= 255 for p in parts):
        raise ValueError("Invalid IP address format")
    return (parts[0] << 24) | (parts[1] << 16) | (parts[2] << 8) | parts[3]

def int_to_ip(val):
    return ".".join(str((val >> offset) & 0xFF) for offset in (24, 16, 8, 0))

def netmask_to_prefix(mask):
    binary = ''.join(f"{int(octet):08b}" for octet in mask.split('.'))
    if len(binary) != 32 or '01' in binary:
        raise ValueError("Invalid subnet mask")
    return binary.count('1')

def prefix_to_netmask(prefix):
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    return int_to_ip(mask)

def calculate_network(ip_int, mask_int):
    return ip_int & mask_int

def calculate_broadcast(network_int, prefix):
    host_bits = 32 - prefix
    return network_int | ((1 << host_bits) - 1)

def ip_and_mask_info(ip, mask):
    try:
        ip_int = ip_to_int(ip)
        mask_int = ip_to_int(mask)
        prefix = netmask_to_prefix(mask)
        network_int = calculate_network(ip_int, mask_int)
        broadcast_int = calculate_broadcast(network_int, prefix)

        host_min = network_int + 1 if prefix < 31 else network_int
        host_max = broadcast_int - 1 if prefix < 31 else broadcast_int
        num_hosts = max(0, (host_max - host_min + 1))

        return {
            "ip": ip,
            "netmask": mask,
            "cidr": f"{int_to_ip(network_int)}/{prefix}",
            "network": int_to_ip(network_int),
            "broadcast": int_to_ip(broadcast_int),
            "first_host": int_to_ip(host_min),
            "last_host": int_to_ip(host_max),
            "host_count": num_hosts,
            "prefix": prefix
        }

    except Exception as e:
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    ip = input("Enter IP address: ").strip()
    mask = input("Enter Subnet Mask: ").strip()
    result = ip_and_mask_info(ip, mask)

    if "error" in result:
        print("Error:", result["error"])
    else:
        print(f"IP Address     : {result['ip']}")
        print(f"Subnet Mask    : {result['netmask']}")
        print(f"CIDR Notation  : {result['cidr']}")
        print(f"Network Address: {result['network']}")
        print(f"Broadcast Addr : {result['broadcast']}")
        print(f"First Host     : {result['first_host']}")
        print(f"Last Host      : {result['last_host']}")
        print(f"Usable Hosts   : {result['host_count']}")
        print(f"Prefix Length  : /{result['prefix']}")