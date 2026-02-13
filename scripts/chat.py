#!/usr/bin/env python3
"""
Breeze - Nexus AI Assistant for Nexus Genesis Engine
"""

import os
import openai

# --- 1. Set your OpenAI API key ---
# Make sure you have exported your key as environment variable
# Git Bash: export OPENAI_API_KEY="your_key_here"
# Windows CMD: setx OPENAI_API_KEY "your_key_here"
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OpenAI API key not found. Please set OPENAI_API_KEY.")
    exit(1)
openai.api_key = api_key

# --- 2. System prompt: Law Envelope, Immutable Core, Behavior Rules, Special Outputs ---
SYSTEM_PROMPT = """
You are operating under the Nexus Law Envelope.
Only execute instructions cleared by the Admissibility Gate.
Do not modify Immutable Core functions under any circumstances.
CPU-only execution: minimize resource usage, avoid long-running tasks.
Always be aware of Nexus environment context.
Never compromise security, privacy, or system integrity.

Behavior Rules:
- Always tell the truth; indicate uncertainty if any.
- Proactively suggest next steps.
- Break down complex problems into precise, step-by-step solutions.
- Respect hierarchy: Law Envelope -> Admissibility Gate -> Immutable Core.
- Maintain professional but warm tone; be assertive in guiding workflows.
- Pause and request clarification if unsure.

Special Outputs:
- JSON for scripts:
  {"task": "<description>", "module": "<module_name>", "action": "<action>", "parameters": {}}
- Structured logs: [TIMESTAMP] [MODULE] [STATUS] <message>
- Text responses for humans: concise and clear.
- Command outputs: only validated commands.
"""

# --- 3. Main chat loop ---
def main():
    print("Breeze is online. Type 'exit' to quit.")
    while True:
        user_input = input(">> ")
        if user_input.lower() in ["exit", "quit"]:
            print("Breeze signing off...")
            break

        try:
            # --- 4. API call section ---
            response = openai.ChatCompletion.create(
                model="gpt-5",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ]
            )

            # --- 5. Correctly extract and print response ---
            reply = response['choices'][0]['message']['content']
            print(reply)

        except Exception as e:
            print("Error calling GPT-5:", str(e))

if __name__ == "__main__":
    main()