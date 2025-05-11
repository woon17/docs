import subprocess
from datetime import datetime
import pytz
import os

# Get current time in Singapore Time
sgt = pytz.timezone("Asia/Singapore")
now = datetime.now(sgt).strftime("%Y-%m-%d %H:%M SGT")

# Get commit info
message = subprocess.getoutput("git log -1 --pretty=format:'%h - %s'")

# Write the output
with open("overrides/timestamp.txt", "w") as f:
    f.write(f"Last updated: {now} ({message})")
