import subprocess
from datetime import datetime
import pytz
import os

# Get current time in Singapore Time
sgt = pytz.timezone("Asia/Singapore")
now = datetime.now(sgt).strftime("%Y-%m-%d %H:%M:%S SGT")

# Get commit info
message = subprocess.getoutput("git log -1 --pretty=format:'%h - %s'")
commit_time = subprocess.getoutput("git log -1 --date=format:'%Y-%m-%d %H:%M:%S SGT' --pretty=%cd")

# Write the output
with open("overrides/timestamp.txt", "w") as f:
    f.write(f"""
<div style="font-size: 0.7rem; text-align: right; color: var(--md-footer-fg-color);">
  <span><strong>Last Deployment:</strong> {now}</span><br>
  <span style="opacity: 0.8;">({commit_time}: {message})</span>
</div>
""")
