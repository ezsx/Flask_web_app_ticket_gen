import re
from docx import Document

def read_questions_from_docx(file_path):
    doc = Document(file_path)
    questions = {'theoretical': [], 'practical': []}

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if re.match(r'^Theoretical:', text):
            question_type = 'theoretical'
        elif re.match(r'^Practical:', text):
            question_type = 'practical'
        elif text:
            questions[question_type].append({'text': text, 'difficulty': None})

    return questions

def read_questions_from_file(file_path):
    doc = Document(file_path)
    questions = {'theoretical': [], 'practical': []}
    current_section = None

    for paragraph in doc.paragraphs:
        if paragraph.text.lower().startswith('theoretical'):
            current_section = 'theoretical'
        elif paragraph.text.lower().startswith('practical'):
            current_section = 'practical'
        elif current_section:
            question = {
                'text': paragraph.text,
                'difficulty': 0
            }
            questions[current_section].append(question)

    return questions


