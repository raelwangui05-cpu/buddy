import json
import os
from datetime import datetime

os.makedirs("sessions", exist_ok=True)

# Include the date and time in the filename as required by the project guide
date_stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
filepath = os.path.join("sessions", f"study_buddy_{date_stamp}.json")

# Convert memory turns into a clean, readable list for JSON storage
clean_history = []
for turn in memory:
    clean_history.append({
        "role": turn["role"],
        "text": turn["parts"][0]["text"]
    })

session_record = {
    "session_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_turns": len(clean_history) // 2,
    "conversation": clean_history,
    "summary": summary
}

with open(filepath, "w", encoding="utf-8") as file:
    json.dump(session_record, file, indent=4, ensure_ascii=False)

print(f"\n[Saved] Full study session and revision summary saved to: {filepath}")

def open_past_session():
    """Displays saved session files and opens the one chosen by the user."""
    if not os.path.exists("sessions") or not os.listdir("sessions"):
        print("\nNo saved study sessions found yet. Start a new session first!")
        return

    print("\n--- Saved Study Sessions ---")
    files = sorted(os.listdir("sessions"))
    for filename in files:
        print(f" • {filename}")

    chosen = input("\nEnter the exact filename to open: ").strip()
    if not chosen:
        print("Error: Filename cannot be empty.")
        return

    filepath = os.path.join("sessions", chosen)

    # Error handling for missing or unreadable session files
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        print(f"\n==========================================")
        print(f"STUDY SESSION DATE: {data.get('session_date', 'Unknown')}")
        print(f"==========================================")
        
        for turn in data.get("conversation", []):
            if turn["role"] == "user":
                print(f"\nSTUDENT: {turn['text']}")
            else:
                # Parse stored JSON reply for neat display
                try:
                    ai_data = json.loads(turn["text"])
                    print(f"\nSTUDY BUDDY: {ai_data.get('feedback', '')}")
                    print(f"Next Question: {ai_data.get('next_question', '')} [{ai_data.get('score_tracker', '')}]")
                except json.JSONDecodeError:
                    print(f"\nSTUDY BUDDY: {turn['text']}")

        print(f"\n------------------------------------------")
        print("FINAL SCORE & REVISION LIST:")
        print(data.get("summary", "No summary available."))
        print(f"==========================================\n")
