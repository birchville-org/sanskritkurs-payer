#!/usr/bin/env python3
import os
import subprocess
import asyncio
from google.antigravity import Agent, LocalAgentConfig
from dotenv import load_dotenv

# Stelle sicher, dass Homebrew und lokale Bins im PATH sind (wichtig für Ausführung via Cron)
os.environ["PATH"] += os.pathsep + "/opt/homebrew/bin" + os.pathsep + "/usr/local/bin"

# Lade den GEMINI_API_KEY aus der ~/.env.local (Cron lädt keine User-Profile!)
env_path = os.path.expanduser("~/.env.local")
if os.path.exists(env_path):
    load_dotenv(env_path)

def run_shell_command(cmd: str) -> str:
    """Executes a shell command and returns the output (stdout + stderr).
    
    Args:
        cmd: The shell command to execute.
    """
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = result.stdout + "\n" + result.stderr
        return output
    except Exception as e:
        return f"Exception executing command: {e}"

def read_file(filepath: str) -> str:
    """Reads the content of a file.
    
    Args:
        filepath: The path to the file.
    """
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(filepath: str, content: str) -> str:
    """Writes content to a file, overwriting it.
    
    Args:
        filepath: The path to the file.
        content: The content to write.
    """
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {e}"

def send_email(report_markdown: str, target_email: str = "marcodem@birchville.org"):
    """
    Sends the report using macOS Mail.app via AppleScript.
    """
    print(f"[*] Sende E-Mail automatisch an {target_email} über macOS Mail.app...")
    safe_content = report_markdown.replace('\\', '\\\\').replace('"', '\\"')
    applescript = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"Payer Projekt: Security & Update Audit (Autonomous)", content:"{safe_content}", visible:false}}
        tell newMessage
            make new to recipient at end of to recipients with properties {{address:"{target_email}"}}
            send
        end tell
    end tell
    '''
    try:
        subprocess.run(["osascript", "-e", applescript], check=True)
        print("[*] E-Mail wurde erfolgreich versendet!")
    except subprocess.CalledProcessError as e:
        print(f"[!] Fehler beim Versenden der E-Mail: {e}")

async def main():
    print("[*] Starting Autonomous Update Agent...")
    
    # We use gemini-2.5-pro for advanced multi-step reasoning
    config = LocalAgentConfig(
        tools=[run_shell_command, read_file, write_file],
        model="gemini-2.5-pro",
        system_instructions=(
            "Du bist ein autonomer DevOps und Security Engineer Agent für ein VitePress Projekt. "
            "Deine Aufgabe ist es, nächtliche Updates durchzuführen und den Build zu verifizieren. "
            "Befolge diese Schritte strikt:\n"
            "1. Führe 'npm update' im Projektordner aus.\n"
            "2. Führe 'npm run docs:build' aus, um zu testen, ob das Update erfolgreich war.\n"
            "3. Wenn der Build fehlschlägt (und es kein Out-Of-Memory / Heap Error ist), musst du "
            "autonom den Fehler analysieren. Finde heraus, welches Paket den Build zerstört hat, "
            "führe einen Downgrade in der package.json durch (oder passe den Code an), "
            "führe 'npm install' aus und teste erneut mit 'npm run docs:build'. "
            "Wiederhole dies, bis der Build auf Grün springt.\n"
            "4. Führe NIEMALS 'git commit' oder 'git push' aus! Lass den reparierten Code lokal liegen, "
            "damit der Entwickler ihn morgens überprüfen kann.\n"
            "5. Schreibe am Ende einen professionellen Markdown-Bericht über deine Aktionen "
            "(was war kaputt, wie hast du es repariert, finaler Status). Halte im Bericht zudem ganz "
            "deutlich fest, ob 'alles bereit ist zu pushen', falls die Reparaturen und der finale Build "
            "erfolgreich waren. Speichere diesen Bericht in 'nightly_report.md'."
        )
    )
    
    async with Agent(config) as agent:
        print("[*] Übergebe Instruktionen an den Agenten...")
        response = await agent.chat(
            "Bitte führe die nächtlichen Updates durch, verifiziere den Build, repariere eventuelle Fehler "
            "autonom und schreibe die Zusammenfassung in 'nightly_report.md'."
        )
        
        async for chunk in response:
            print(chunk, end="", flush=True)
            
    print("\\n[*] Agent ist fertig. Suche nach nightly_report.md...")
    if os.path.exists("nightly_report.md"):
        with open("nightly_report.md", "r") as f:
            report_content = f.read()
        send_email(report_content)
        os.remove("nightly_report.md")
    else:
        print("[!] Agent hat keinen Bericht in 'nightly_report.md' abgelegt. Sende Fallback-E-Mail.")
        send_email("Der autonome Agent ist durchgelaufen, hat aber keinen Abschlussbericht generiert. Bitte prüfe die Logs.")

if __name__ == "__main__":
    asyncio.run(main())
