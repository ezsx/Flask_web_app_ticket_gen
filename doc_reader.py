import re
from docx import Document
def read_questions_from_docx(file_path):
    questions = []
    question_pattern = re.compile(r'Task \d+')

    # Read the Word document
    doc = Document(file_path)
    file_content = '\n'.join([para.text for para in doc.paragraphs])

    # Detect question type
    if "Theoretical" in file_content:
        question_type = 'theoretical'
        file_content = file_content.replace("Theoretical", "")
    elif "Practical" in file_content:
        question_type = 'practical'
        file_content = file_content.replace("Practical", "")
    else:
        question_type = 'unknown'

    question_texts = question_pattern.split(file_content)[1:]  # Ignore the first element, which is the text before the first question

    for question_text in question_texts:
        question_text = question_text.strip()
        question = {
            'type': question_type,
            'text': question_text,
            'difficulty': 1
        }
        questions.append(question)

    return questions
