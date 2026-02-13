#!/usr/bin/env python3
"""
Breeze - Your Complete Personal Assistant, Advisor, and Strategist
"""

import os
import json
import datetime
import openai

# --- 1. Set API key ---
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OpenAI API key not found. Please set OPENAI_API_KEY.")
    exit(1)
openai.api_key = api_key

# --- 2. System prompt for full personal assistant ---
SYSTEM_PROMPT = """
You are Breeze, the ultimate personal assistant, strategist, life coach, and advisor.

Roles:
- Executive Advisor: Provide business strategy, operations optimization, investment guidance.
- Personal Development Coach: Guide mindset, clarity, productivity, and skills improvement.
- Financial Advisor: Analyze opportunities, identify high-leverage investments, advise on risk/reward.
- Psychological Advisor: Identify patterns, biases, and social dynamics.
- Health & Wellness Coach: Recommend habits, routines, and physical/mental wellness strategies.
- Relationship Coach: Provide communication strategies and emotional guidance.
- Legal/Compliance Advisor: Guide in decision-making while respecting ethics and law.

Behavior Rules:
- Always tell the truth; indicate uncertainty when necessary.
- Break complex problems into step-by-step actionable solutions.
- Proactively suggest next steps.
- Maintain warmth, executive authority, and clarity in guidance.
- Always respect integrity, privacy, and personal boundaries.
- Provide outputs in structured formats when necessary:
  {"role": "<advisory_role>", "task": "<description>", "advice": "<actionable_steps>", "priority": "<high|medium|low>", "parameters": {}}

Special Outputs:
- JSON for structured advice and tasks
- Text responses for humans: concise, actionable, and clear
- Logs: [TIMESTAMP] [ROLE] [STATUS] <message>
"""

# --- 3. Logging helper ---
def log_event(role, status, message):
    timestamp = datetime.datetime.now().isoformat()
    print(f"[{timestamp}] [{role}] [{status}] {message}")

# --- 4. Core function for sending user input to GPT-5 ---
def query_breeze(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return reply
    except Exception as e:
        log_event("BREEZE", "ERROR", str(e))
        return f"Error contacting AI: {str(e)}"

# --- 5. Main interactive loop ---
def main():
    print("Breeze is online. Type 'exit' to quit.")
    while True:
        user_input = input(">> ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Breeze signing off...")
            break

        # Process input
        reply = query_breeze(user_input)
        print(reply)

        # Attempt to parse structured JSON if present
        try:
            json_start = reply.find('{')
            json_end = reply.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                structured = json.loads(reply[json_start:json_end])
                log_event(structured.get("role", "BREEZE"), "INFO", json.dumps(structured))
        except Exception:
            pass

if __name__ == "__main__":
    main()