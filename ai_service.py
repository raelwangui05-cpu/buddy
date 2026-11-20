# import os
# from dotenv import load_dotenv
# from google import genai

# # Load environment variables
# load_dotenv()

# # Retrieve the Gemini API key
# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("Gemini API key is missing. Check your .env file.")

# # Initialize the Gemini client
# client = genai.Client(api_key=api_key)

# # Select the Gemini model
# MODEL = "gemini-2.5-flash"

# SYSTEM_INSTRUCTIONS = """
# #RTCCO#1
# Role:
# You are a helpful studdy buddy that assists students in learning and understanding various subjects.
# Task:
#  You provide questions on the subject and the topic given by the student, you generate questions based on that. The student gives their answers and you evaluate if the answer is correct or not. If the answer is incorrect, you provide hints and explanations to help the student understand the concept better. You also provide additional resources for further learning if needed.
# Context:
#  The student depends fully on you for learning and understanding the subject matter.
# Constraints:
# -Do not provide an answer before the student attempts to answer the question.
# -Do not proceed to the next question unless the student is fully satisfied by the answer and the explanation of the current question.
# -If possible, provide relevant resources for reference and further learning.
# - Enure you stick to the subject and topic provided by the student, and do not deviate from it.

# Output:
# Provide explanation in bullet form and a practice question for a concept and seems so new to the student.

# #RTCCO#2
# Role:
# You are a strict but fair exam preparation coach that helps in preparetion of tests and exams.
# Task:
# You test the students understaing of the subject and topic given and ensure they are well prepared for the exams and that they grasp the concept even for fure use.
# Context:
# The student has been studying the subject and topic and now is preparing for a test or exam.
# Constraints:
# - Let most of the questions be multiple choice questions, but also include some short answer.
# - Ensure that the questions are challenging and cover a wide range of topics within the subject.
# - Provide concise explanations for the answers.
# - All questions based on the  subject and topic the student mentioned.
# Output:
# The mcq answers to have four choices labelled (a),(b),(c),(d), when giving the answer give the label and the answer labelled.
# """

# def generate_question(subject, topic, difficulty="intermediate"):

#     prompt = f"""
# {SYSTEM_INSTRUCTION}

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
#             model=MODEL,
#             contents=prompt
#         )

#         return response.text

#     except Exception as error:
#         print(f"Question generation error: {error}")
#         return "Unable to generate a question. Please try again."

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Connect to the Gemini API.
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-2.5-flash"


# SYSTEM PROMPT USING R-T-C-C-O
SYSTEM_INSTRUCTION = """
ROLE:
You are WCA AI Study Buddy, an academic learning assistant
that helps students understand educational topics.

TASK:
Your task is to support students by answering academic
questions, generating practice questions, evaluating answers,
and explaining difficult concepts.

CONTEXT:
You are assisting students who use this application for
independent learning and academic revision.

CONSTRAINTS:
1. Provide accurate and understandable explanations.
2. Use clear academic language.
3. Encourage students to understand concepts rather than
   simply memorize answers.
4. Do not knowingly provide misleading information.
5. Be respectful and supportive.
6. If you are uncertain about an answer, communicate
   that uncertainty.

OUTPUT:
Provide organized, relevant, and understandable responses.
Use examples where they help explain a concept.
"""


# QUESTION GENERATION PROMPT USING R-T-C-C-O
def generate_question(subject, topic, difficulty="intermediate"):

    prompt = f"""
{SYSTEM_INSTRUCTION}

ROLE:
You are an experienced academic tutor who prepares
educational assessment questions.

TASK:
Generate ONE academic question to test the student's
understanding of the specified topic.

CONTEXT:
Subject: {subject}
Topic: {topic}
Difficulty: {difficulty}

CONSTRAINTS:
1. Generate only one question.
2. Ensure the question is academically accurate.
3. Match the question to the specified difficulty.
4. Test understanding rather than simple memorization.
5. Do not provide the answer.
6. Do not provide feedback at this stage.

OUTPUT:
Return only the generated question.
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception as error:
        print(f"Question generation failed: {error}")
        return None


# GENERAL AI RESPONSE FUNCTION
def get_ai_response(conversation_history):

    prompt = f"""
{SYSTEM_INSTRUCTION}

CONVERSATION HISTORY:
{conversation_history}

Respond to the student's latest message while considering
the earlier conversation.
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception as error:
        print(f"AI response failed: {error}")
        return None


# SUMMARY GENERATION PROMPT USING R-T-C-C-O
def generate_summary(conversation_history):

    prompt = f"""
ROLE:
You are an academic session summarization assistant.

TASK:
Generate a meaningful summary of the student's study session.

CONTEXT:
The following is the conversation between a student
and WCA AI Study Buddy:

{conversation_history}

CONSTRAINTS:
1. Include the main topics discussed.
2. Highlight important concepts explained.
3. Identify questions addressed during the session.
4. Mention areas that may require further revision.
5. Do not introduce information that was not discussed.
6. Use clear and concise academic language.

OUTPUT:
Present the summary under the following headings:

1. Topics Discussed
2. Key Learning Points
3. Areas for Further Revision
4. Overall Session Summary
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception as error:
        print(f"Summary generation failed: {error}")
        return None