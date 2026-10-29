from collections import defaultdict
import re

def analyze_logs(log_file='auth_events.log'):
    failed_attempts = defaultdict(int)
    total_attempts = defaultdict(int)
    failed_users = defaultdict(set)

    # Regex to parse log lines (Timestamp | Level | IP: <ip> | User: <user> | Status: <status>)
    log_pattern = re.compile(r'(?P<timestamp>[\d\- :]+) \| (?P<level>\w+) \| IP: (?P<ip>[\w\.:]+) \| User: (?P<user>\w+) \| Status: (?P<status>\w+)')

    try:
        with open(log_file, 'r') as f:
            for line in f:
                match = log_pattern.search(line)
                if match:
                    data = match.groupdict()
                    ip = data['ip']
                    status = data['status']
                    user = data['user']

                    total_attempts[ip] += 1
                    if status == 'FAILED':
                        failed_attempts[ip] += 1
                        failed_users[ip].add(user)

        print("=" * 60)
        print(" CYBERSECURITY THREAT DETECTION & LOG ANALYSIS REPORT")
        print("=" * 60)

        for ip, fails in failed_attempts.items():
            # Threat Detection Rules & Classification
            if fails >= 5:
                threat_level = "HIGH"
                alert_type = "Possible Brute-Force Attack"
            elif fails >= 2:
                threat_level = "MEDIUM"
                alert_type = "Repeated Suspicious Logins"
            else:
                threat_level = "LOW"
                alert_type = "Normal / Minor Activity"

            print(f"\n[ALERT GENERATED]")
            print(f"  IP Address     : {ip}")
            print(f"  Failed Attempts: {fails} / {total_attempts[ip]} total")
            print(f"  Targeted Users : {list(failed_users[ip])}")
            print(f"  Threat Level   : {threat_level} ({alert_type})")
            print("-" * 60)

    except FileNotFoundError:
        print(f"Error: {log_file} not found. Generate some login events first!")

if __name__ == '__main__':
    analyze_logs()