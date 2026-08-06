total = 0
failures = 0

with open("auth_large.log", "r") as f:
    for line in f:
        total += 1
        if "Failed password" in line:
            failures += 1
            print(f"[ALERT] Line {total}: {line.strip()}")

print(f"\nTotal lines: {total}")
print(f"Failed logins found: {failures}")