import os
import subprocess

class NginxIPBlocker:
    def __init__(self, filepath="/etc/nginx/blocked_ips.conf", reload_cmd=["systemctl", "reload", "nginx"]):
        self.filepath = filepath
        self.reload_cmd = reload_cmd
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                pass  # create empty file

    def _read_rules(self):
        rules = {"allow": [], "deny": []}
        try:
            with open(self.filepath, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("allow "):
                        ip = line.split()[1].rstrip(";")
                        rules["allow"].append(ip)
                    elif line.startswith("deny "):
                        ip = line.split()[1].rstrip(";")
                        rules["deny"].append(ip)
        except Exception as e:
            print(f"[!] Error reading rules: {e}")
        return rules

    def _write_rules(self, rules):
        try:
            with open(self.filepath, "w") as f:
                for ip in sorted(set(rules["allow"])):
                    f.write(f"allow {ip};\n")
                for ip in sorted(set(rules["deny"])):
                    f.write(f"deny {ip};\n")
            subprocess.run(self.reload_cmd, check=True)
        except Exception as e:
            print(f"[!] Failed to write or reload NGINX: {e}")

    def get_rules(self, ip=None):
        rules = self._read_rules()
        if ip:
            if ip in rules["allow"]:
                return {"ip": ip, "action": "allow"}
            elif ip in rules["deny"]:
                return {"ip": ip, "action": "deny"}
            else:
                return None
        return rules

    def exists(self, ip):
        rules = self._read_rules()
        return ip in rules["allow"] or ip in rules["deny"]

    def add_ip(self, ip, action="deny"):
        if action not in {"allow", "deny"}:
            raise ValueError("Action must be 'allow' or 'deny'")

        rules = self._read_rules()
        opposite = "allow" if action == "deny" else "deny"

        if ip in rules[opposite]:
            rules[opposite].remove(ip)

        if ip not in rules[action]:
            rules[action].append(ip)
            self._write_rules(rules)
            print(f"[+] {action.upper()}ED {ip} in NGINX")
        else:
            print(f"[-] {ip} already in {action} list")

    def remove_ip(self, ip):
        rules = self._read_rules()
        changed = False

        for key in ["allow", "deny"]:
            if ip in rules[key]:
                rules[key].remove(ip)
                changed = True

        if changed:
            self._write_rules(rules)
            print(f"[+] Removed {ip} from NGINX rules")
        else:
            print(f"[-] {ip} not found in any list")