# import os
# from dotenv import load_dotenv
# from google import genai

# # 1. Load environment variables
# load_dotenv()

# # Retrieve the Gemini API key
# API_KEY = os.getenv("API_KEY")

# if not API_KEY:
#     print("CRITICAL ERROR: GEMINI_API_KEY not found. Please check your .env file.")
#     exit(1)

# # 2. Initialize the Gemini client and model
# client = genai.Client(api_key=API_KEY)
# MODEL_NAME = "gemini-3.8-flash"

# # 3. DESIGNED PROMPTS (R-T-C-C-O FRAMEWORK)
# SYSTEM_PROMPT = """
# ROLE: You are an encouraging and patient AI Study Buddy for students in Kenya.
# TASK: Quiz the student one question at a time on their chosen subject and topic. Mark each answer clearly, keep track of their running score, and revisit concepts or questions they got wrong earlier in the session.
# CONTEXT: In the first turn, the student will name a subject and topic (e.g., 'Biology - Cell Division' or 'KCSE History - Kenyan Independence'). Across at least 4 turns, you must ask one clear question per turn, evaluate their reply in the next turn, and loop back to test weak areas they missed.
# CONSTRAINTS:
# - Ask ONLY ONE question per turn so the student is not overwhelmed.
# - Always check the conversation history to remember which questions the student got wrong and re-test those concepts later in the session.
# - Give brief, clear explanations when correcting a wrong answer before asking the next question.
# - Keep questions fair, accurate, and suitable for a student revising for exams.
# OUTPUT FORMAT: Respond ONLY with a valid JSON object containing these exact four keys:
# {
#   "feedback": "Feedback on the student's previous answer (or 'Welcome! Let us begin.' on Turn 1)",
#   "is_correct": "Correct / Incorrect / First Turn",
#   "next_question": "The single next question for the student to answer",
#   "score_tracker": "Running score so far (e.g., '2/3 correct')"
# }
# """

# SUMMARY_PROMPT = """
# ROLE: You are an academic tutor creating a post-study revision report.
# TASK: Review the entire Study Buddy quiz conversation and provide:
# 1. The student's final score (number of correct answers out of total questions answered).
# 2. A clear list of specific sub-topics or concepts the student struggled with and needs to revise.
# 3. Brief study tips for mastering those weak areas.
# CONTEXT: The student has just finished their interactive Study Buddy session.
# CONSTRAINTS:
# - Base the score and weak topics strictly on the actual questions and answers in the conversation history.
# - If the student got everything right, congratulate them and suggest the next logical topic to study.
# OUTPUT FORMAT: Write a clean, well-structured plain text summary with clear headings.
# """

# # 4. Question Generation Function
# def generate_question(subject, topic, difficulty="intermediate"):
#     prompt = f"""
# {SYSTEM_PROMPT}

# TASK:
# Generate ONE academic question for the student.
# Subject: {subject}
# Topic: {topic}
# Difficulty: {difficulty}

# REQUIREMENTS:
# 1. Generate only one question.
# 2. Ensure the question tests understanding.
# 3. Do not provide the answer.
# 4. Make the question academically accurate.
# 5. Do not include feedback yet.

# Return only the question.
# """

#     try:
#         response = client.models.generate_content(
#             model=MODEL_NAME,
#             contents=prompt
#         )
#         return response.text

#     except Exception as error:
#         print(f"Question generation error: {error}")
#         return "Unable to generate a question. Please try again."

import json
from datetime import datetime
from pathlib import Path

from ai_service import (
    get_ai_response,
    generate_question,
    generate_summary
)

# Folder for storing study sessions.
SESSIONS_FOLDER = Path("sessions")
SESSIONS_FOLDER.mkdir(exist_ok=True)


# Convert conversation history into readable text.
def format_conversation(messages):

    conversation = ""

    for message in messages:
        conversation += (
            f"{message['role']}: {message['content']}\n"
        )

    return conversation


# Save a study session.
def save_session(session):

    filename = (
        f"session_{session['session_id']}.json"
    )

    filepath = SESSIONS_FOLDER / filename

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(session, file, indent=4)

    print("Session saved successfully.")


# Start a new study session.
def start_new_session():

    print("\nWELCOME TO WCA AI STUDY BUDDY")

    subject = input("Enter your subject: ").strip()

    if not subject:
        print("Subject cannot be empty.")
        return

    topic = input("Enter the topic you want to study: ").strip()

    if not topic:
        print("Topic cannot be empty.")
        return

    difficulty = input(
        "Enter difficulty (beginner, intermediate, advanced): "
    ).strip().lower()

    if difficulty not in ["beginner", "intermediate", "advanced"]:
        difficulty = "intermediate"

    # Generate an academic question.
    question = generate_question(
        subject,
        topic,
        difficulty
    )

    if not question:
        print("Unable to generate a question.")
        return

    print("\nSTUDY QUESTION")
    print(question)

    # Initialize conversation memory.
    messages = [
        {
            "role": "assistant",
            "content": question
        }
    ]

    while True:

        user_message = input(
            "\nYou (type 'exit' to finish): "
        ).strip()

        if not user_message:
            print("Please enter a message.")
            continue

        if user_message.lower() == "exit":
            break

        # Store the student's message.
        messages.append({
            "role": "user",
            "content": user_message
        })

        # Send the complete conversation history.
        conversation = format_conversation(messages)

        ai_response = get_ai_response(conversation)

        if not ai_response:
            print("Unable to obtain an AI response.")
            messages.pop()
            continue

        print("\nSTUDY BUDDY:")
        print(ai_response)

        # Store the AI response.
        messages.append({
            "role": "assistant",
            "content": ai_response
        })

    # Generate a summary when the session ends.
    print("\nGenerating your study session summary...")

    conversation = format_conversation(messages)

    summary = generate_summary(conversation)

    if not summary:
        summary = "Summary could not be generated."

    print("\nSTUDY SESSION SUMMARY")
    print(summary)

    # Create the session record.
    session = {
        "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "subject": subject,
        "topic": topic,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "messages": messages,
        "summary": summary
    }

    save_session(session)


# Display previously saved sessions.
def view_previous_sessions():

    files = list(SESSIONS_FOLDER.glob("session_*.json"))

    if not files:
        print("\nNo saved sessions found.")
        return

    print("\nPREVIOUS STUDY SESSIONS")

    for index, file in enumerate(files, start=1):
        print(f"{index}. {file.name}")

    choice = input("\nEnter the session number: ").strip()

    try:
        selected_index = int(choice) - 1

        if selected_index < 0 or selected_index >= len(files):
            print("Invalid session selection.")
            return

        with open(
            files[selected_index],
            "r",
            encoding="utf-8"
        ) as file:

            session = json.load(file)

        print("\nSESSION DETAILS")
        print("Subject:", session["subject"])
        print("Topic:", session["topic"])
        print("Date:", session["date"])

        print("\nCONVERSATION")

        for message in session["messages"]:
            print(f"\n{message['role']}: {message['content']}")

        print("\nSESSION SUMMARY")
        print(session["summary"])

    except ValueError:
        print("Please enter a valid number.")

    except FileNotFoundError:
        print("Session file could not be found.")

    except json.JSONDecodeError:
        print("The selected session contains invalid JSON.")


# Main application menu.
def main():

    while True:

        print("\n================================")
        print("       WCA AI STUDY BUDDY")
        print("================================")

        print("1. Start a new study session")
        print("2. Open a previous session")
        print("3. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            start_new_session()

        elif choice == "2":
            view_previous_sessions()

        elif choice == "3":
            print("\nThank you for using WCA AI Study Buddy!")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()