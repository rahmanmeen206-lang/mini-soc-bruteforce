import re

failures = {}

with open("auth_large.log", "r") as f:
    for line in f:
        if "Failed password" in line:
            match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
            if match:
                ip = match.group(1)
                failures[ip] = failures.get(ip, 0) + 1
                if failures[ip] >= 5:
                    print(f"[BRUTE FORCE] {ip} has {failures[ip]} failures!")

print("\n--- Summary ---")
for ip, count in failures.items():
    print(f"  {ip}: {count} failed attempt(s)")