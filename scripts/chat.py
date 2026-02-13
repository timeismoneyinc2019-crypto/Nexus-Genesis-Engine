#!/usr/bin/env python3
"""
Breeze - Full Personal Assistant for Nexus Genesis Engine
"""

import os
import json
import datetime
import subprocess
import openai

# --- 1. API Key setup ---
api_key = os.getenv("OPENAI SECRET_API_KEY")
if not api_key:
    print("ERROR: OpenAI API key not found. Set OPENAI_API_KEY.")
    exit(1)
openai.api_key = api_key

# --- 2. System prompts and behavior rules ---
SYSTEM_PROMPT = """
You are Breeze, the Nexus AI Assistant.
- Operates under Law Envelope → Admissibility Gate → Immutable Core hierarchy.
- CPU-only execution.
- Always tell the truth; indicate uncertainty if any.
- Provide step-by-step instructions for any task, especially R&D AI development.
- Proactively suggest next steps for Nexus projects.
- Output commands and module instructions as JSON for automation:
  {"task": "<description>", "module": "<module_name>", "action": "<action>", "parameters": {}}
- Keep human-readable responses concise and actionable.
- Never override Immutable Core or bypass Nexus security layers.
- Handle multi-step processes in sequence and always request clarification if ambiguous.
"""

# --- 3. Helper: log structured events ---
def log_event(module, status, message):
    timestamp = datetime.datetime.now().isoformat()
    print(f"[{timestamp}] [{module}] [{status}] {message}")

# --- 4. Helper: run local Nexus module commands ---
def run_module(module_name, *args):
    try:
        # Executes Python module within Nexus repo
        result = subprocess.run(
            ["python", f"{module_name}.py"] + list(args),
            capture_output=True, text=True
        )
        log_event(module_name, "SUCCESS" if result.returncode == 0 else "FAIL",
                  result.stdout.strip())
        return result.stdout.strip()
    except Exception as e:
        log_event(module_name, "ERROR", str(e))
        return str(e)

# --- 5. Main Breeze loop ---
def main():
    print("Breeze is online. Type 'exit' to quit.")
    while True:
        user_input = input(">> ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Breeze signing off...")
            break

        # --- 6. Handle direct module commands locally ---
        # Example: "Run Nexus Health Check" → calls Health Check module
        if user_input.lower().startswith("run "):
            parts = user_input.split(" ", 2)
            module_command = parts[1] if len(parts) > 1 else ""
            extra_args = parts[2:] if len(parts) > 2 else []
            output = run_module(module_command, *extra_args)
            print(output)
            continue

        # --- 7. API call section for AI assistance ---
        try:
            response = openai.ChatCompletion.create(
                model="gpt-5",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ]
            )

            reply = response['choices'][0]['message']['content']
            print(reply)

            # Attempt to parse JSON if the AI returns commands
            try:
                json_start = reply.find('{')
                json_end = reply.rfind('}') + 1
                if json_start != -1 and json_end != -1:
                    command_json = json.loads(reply[json_start:json_end])
                    log_event("AI_COMMAND", "INFO", json.dumps(command_json))
            except Exception:
                pass

        except Exception as e:
            log_event("GPT-5", "ERROR", str(e))
            print("Error contacting GPT-5:", str(e))

# --- 8. Run Breeze ---
if __name__ == "__main__":
    main()