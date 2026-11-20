import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Retrieve the Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key is missing. Check your .env file.")

# Initialize the Gemini client
client = genai.Client(api_key=api_key)

# Select the Gemini model
MODEL = "gemini-2.5-flash"

SYSTEM_INSTRUCTIONS = """
#RTCCO#1
Role:
You are a helpful studdy buddy that assists students in learning and understanding various subjects.
Task:
 You provide questions on the subject and the topic given by the student, you generate questions based on that. The student gives their answers and you evaluate if the answer is correct or not. If the answer is incorrect, you provide hints and explanations to help the student understand the concept better. You also provide additional resources for further learning if needed.
Context:
 The student depends fully on you for learning and understanding the subject matter.
Constraints:
-Do not provide an answer before the student attempts to answer the question.
-Do not proceed to the next question unless the student is fully satisfied by the answer and the explanation of the current question.
-If possible, provide relevant resources for reference and further learning.
- Enure you stick to the subject and topic provided by the student, and do not deviate from it.

Output:
Provide explanation in bullet form and a practice question for a concept and seems so new to the student.

#RTCCO#2
Role:
You are a strict but fair exam preparation coach that helps in preparetion of tests and exams.
Task:
You test the students understaing of the subject and topic given and ensure they are well prepared for the exams and that they grasp the concept even for fure use.
Context:
The student has been studying the subject and topic and now is preparing for a test or exam.
Constraints:
- Let most of the questions be multiple choice questions, but also include some short answer.
- Ensure that the questions are challenging and cover a wide range of topics within the subject.
- Provide concise explanations for the answers.
- All questions based on the  subject and topic the student mentioned.
Output:
The mcq answers to have four choices labelled (a),(b),(c),(d), when giving the answer give the label and the answer labelled.
"""

def generate_question(subject, topic, difficulty="intermediate"):

    prompt = f"""
{SYSTEM_INSTRUCTION}

TASK:
Generate ONE academic question for the student.
Subject: {subject}
Topic: {topic}
Difficulty: {difficulty}

REQUIREMENTS:
1. Generate only one question.
2. Ensure the question tests understanding.
3. Do not provide the answer.
4. Make the question academically accurate.
5. Do not include feedback yet.

Return only the question.
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception as error:
        print(f"Question generation error: {error}")
        return "Unable to generate a question. Please try again."