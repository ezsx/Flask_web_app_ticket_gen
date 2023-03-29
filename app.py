from flask import Flask, render_template, request, redirect, url_for, flash,json
from doc_reader import read_questions_from_file
from werkzeug.utils import secure_filename
import os

questions = []
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "your_secret_key"


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/', methods=['GET', 'POST'])
def index():
    print(f"Index called with questions: {questions}")  # Add this line
    if request.method == 'POST':
        # Handle file upload and other actions here
        pass
    return render_template('index.html', questions=questions)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(f"File saved at {filepath}")  # Add this line

        try:
            global questions
            questions = read_questions_from_file(filepath)
            print(f"Questions: {questions}")  # Add this line
            return index()
        except Exception as e:
            return str(e)

    return redirect(request.url)


@app.route('/edit', methods=['POST'])
def edit_question():
    question_type = request.form['question_type']
    question_index = int(request.form['question_index'])
    question_text = request.form['question_text']
    question_difficulty = int(request.form['question_difficulty'])

    questions[question_type][question_index]['text'] = question_text
    questions[question_type][question_index]['difficulty'] = question_difficulty

    return redirect(url_for('index'))


from flask import jsonify

@app.route('/edit_questions', methods=['POST'])
def edit_questions():
    for key, value in request.form.items():
        if key.startswith('question_type_'):
            index = int(key.split('_')[-1])
            question_type = value
            question_index = int(request.form[f'question_index_{index}'])
            question_text = request.form[f'question_text_{index}']
            question_difficulty = int(request.form[f'question_difficulty_{index}'])

            questions[question_type][question_index]['text'] = question_text
            questions[question_type][question_index]['difficulty'] = question_difficulty

    return redirect(url_for('index'))



@app.route('/generate_tickets', methods=['GET', 'POST'])
def generate_tickets():
    target_difficulty = request.form.get('target_difficulty')
    num_tickets = int(request.form.get('num_tickets', 0))

    if not target_difficulty:
        target_difficulty = None
    else:
        target_difficulty = int(target_difficulty)

    generated_tickets = generate_balanced_tickets(questions, num_tickets, target_difficulty)

    # Add a unique ID to each ticket
    tickets = []
    for i, ticket in enumerate(generated_tickets):
        tickets.append({"id": f"{i}", "content": ticket})

    return render_template('tickets.html', tickets=tickets)




import random


def generate_balanced_tickets(questions, num_tickets, target_difficulty=None):
    theoretical_questions = questions['theoretical']
    practical_questions = questions['practical']

    # Calculate the average difficulty if target_difficulty is not provided
    if target_difficulty is None:
        total_difficulty = sum(q['difficulty'] for q in theoretical_questions) + 2 * sum(
            q['difficulty'] for q in practical_questions)
        target_difficulty = total_difficulty // (num_tickets * 3)

    tickets = []
    for _ in range(num_tickets):
        ticket = []

        # Select one theoretical question and two practical questions
        for question_type, num_questions in [('theoretical', 1), ('practical', 2)]:
            question_list = questions[question_type].copy()

            for _ in range(num_questions):
                if not question_list:
                    question_list = questions[question_type].copy()

                # Sort the questions based on their closeness to the target difficulty and randomize the selection
                sorted_questions = sorted(question_list, key=lambda q: abs(
                    q['difficulty'] - target_difficulty // (1 if question_type == 'theoretical' else 2)))
                selected_question = random.choice(sorted_questions[:3])  # Select one of the three closest questions
                ticket.append(selected_question)
                question_list.remove(selected_question)

        tickets.append(ticket)

    return tickets


import os

from flask import send_file

from io import BytesIO


@app.route('/save_tickets', methods=['POST'])
def save_tickets():
    data = request.get_json()
    tickets_data = data['ticketsData']

    doc = Document()

    for idx, ticket in enumerate(tickets_data):
        doc.add_heading(f'Ticket {idx + 1}', level=1)

        for question_idx, question in enumerate(ticket):
            formatted_question = f"{question_idx + 1}. {question['text']} (Difficulty: {question['difficulty']})"
            doc.add_paragraph(formatted_question)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='tickets.docx',
                     mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')


from docx import Document


def save_tickets_to_word(tickets, file_path):
    doc = Document()

    for idx, ticket in enumerate(tickets):
        doc.add_heading(f'Ticket {idx + 1}', level=1)

        doc.add_heading('Theory', level=2)
        doc.add_paragraph(ticket[0]['text'])

        doc.add_heading('Practice', level=2)
        for question in ticket[1:]:
            doc.add_paragraph(question['text'])

        doc.add_page_break()

    doc.save(file_path)


if __name__ == '__main__':
    app.run(debug=True)
