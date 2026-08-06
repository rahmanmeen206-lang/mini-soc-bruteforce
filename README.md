# Mini SOC Detector

A lightweight Security Operations Center (SOC) tool that monitors authentication logs, detects brute-force login attempts, and sends email alerts automatically. Built to practice core log-monitoring concepts: parsing raw auth logs, flagging suspicious activity based on a failed-attempt threshold, and automating the alerting workflow.

## Features

- **Log parsing** — reads and scans entries from `auth.log`-style files for failed login attempts
- **Brute-force detection** — flags an IP once its failed login count reaches a threshold (5+ failed attempts)
- **Email alerting** — automatically sends an email notification when an IP crosses the threshold
- **Sample data included** — `auth_large.log` for testing against a realistic dataset

## How it works

1. `log_reader.py` — reads the log file line by line and reports every failed login entry found, plus a total count
2. `bruteforce.py` — parses each line for failed logins, extracts the source IP, and counts failed attempts per IP; prints a flag once an IP hits 5+ failures, with a summary at the end
3. `automation.py` — runs the same detection logic and, when an IP crosses the threshold, sends an email alert via Gmail SMTP (each IP is only alerted once per run)

## Usage

```bash
python automation.py
```

This reads `auth_large.log`, prints an alert to the console for any IP with 5+ failed login attempts, and emails a notification for each one.

## Example Output

```
[ALERT] 192.168.1.45 has 5 failures!
[EMAIL SENT] Alert sent for IP 192.168.1.45
```

## Detection Logic

An alert is triggered when an IP address reaches **5 or more failed login attempts** anywhere in the log file. This is a simple count-based threshold — it does not currently factor in a time window (e.g. "5 failures within 60 seconds"), so it can't yet distinguish a slow trickle of failures over days from a rapid automated attack. That's listed under Future Improvements below.

## Security Note

This project sends email alerts via Gmail SMTP, which requires an email address and app password. **These must never be hardcoded or committed to the repo.** An earlier version of this project had credentials hardcoded directly in `automation.py` — that app password has since been **revoked**. Credentials should be loaded from environment variables instead:

```python
import os
sender_email = os.environ.get("SOC_SENDER_EMAIL")
sender_password = os.environ.get("SOC_SENDER_PASSWORD")
```

Set them in your shell before running, or use a `.env` file that's excluded via `.gitignore` — never commit real credentials.

## Tech Stack

- Python 3.x
- `smtplib` / `email.mime` for email alerting

## Motivation

Built to practice core SOC/blue-team concepts — log analysis, threat detection, and security automation — as part of learning cybersecurity fundamentals.

## Future Improvements

- [ ] Add a time-window condition (e.g. 5+ failures within 60 seconds) for true brute-force detection instead of a lifetime count
- [ ] Move credentials fully to environment variables / `.env` (see Security Note)
- [ ] Support multiple log formats (syslog, JSON, Windows Event Log)
- [ ] Add unit tests
- [ ] Dockerize for easy deployment
- [ ] Make the failure threshold configurable instead of hardcoded# Mini SOC detector
