import re
from collections import defaultdict
import json

# Raw input data
with open(
    file="C://Users/Dqrkky/Downloads/ips.txt",
    mode="r"
) as fp:
    data = fp.read()

# Processing
asn_dict = defaultdict(list)
current_asn = None

for line in data.splitlines():
    line = line.strip()
    if not line or line == "--------------":
        continue
    if line.startswith("AS "):
        current_asn = line.replace("AS ", "")
    else:
        asn_dict[current_asn].append(line)

# Convert to desired JSON format
result = [
    {"type": "asn", "asn": asn, "ips": ips}
    for asn, ips in asn_dict.items()
]
with open(
    file="C://Users/Dqrkky/Downloads/ips.json",
    mode="w"
) as fp1:
    json.dump(
        fp=fp1,
        obj=result,
        indent=4
    )