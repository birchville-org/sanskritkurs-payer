#!/usr/bin/env python3
"""
Send notification email to marcodem@birchville.org via Apple Mail.
"""

import sys
import subprocess
import os

RECIPIENT = "marcodem@birchville.org"

def send_email(subject: str, body: str) -> bool:
    """Send an email via macOS Apple Mail app using osascript."""
    # Escape quotes and backslashes for AppleScript string literals
    safe_subject = subject.replace('\\', '\\\\').replace('"', '\\"')
    safe_body = body.replace('\\', '\\\\').replace('"', '\\"')
    
    applescript = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"{safe_subject}", content:"{safe_body}", visible:false}}
        tell newMessage
            make new to recipient at end of to recipients with properties {{address:"{RECIPIENT}"}}
            send
        end tell
    end tell
    '''
    
    try:
        res = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True, check=True)
        print(f"✓ E-Mail erfolgreich an {RECIPIENT} gesendet.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler beim Senden via Apple Mail: {e.stderr.strip()}")
        return False

if __name__ == "__main__":
    subj = sys.argv[1] if len(sys.argv) > 1 else "Antigravity Status Benachrichtigung"
    content = sys.argv[2] if len(sys.argv) > 2 else "Testbenachrichtigung von Antigravity."
    send_email(subj, content)
