
import time
import csv
import urllib.request
from datetime import datetime

URLS = [
    "https://www.google.com",
    "https://www.cloudflare.com",
]

INTERVAL = 30
LOG_FILE = "connection_log.csv"


def check_connection(url):
    start = time.time()

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "VPN-Monitor/1.0"}
        )

        with urllib.request.urlopen(request, timeout=10):
            latency = round((time.time() - start) * 1000, 2)
            return "ONLINE", latency

    except Exception:
        return "OFFLINE", None


def main():
    print("VPN Stability Monitor Started")

    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow(
                ["Time", "Website", "Status", "Latency"]
            )

        while True:
            for url in URLS:
                status, latency = check_connection(url)

                now = datetime.now().isoformat()

                writer.writerow([now, url, status, latency])
                file.flush()

                print(now, url, status, latency)

            time.sleep(INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Monitoring stopped")
