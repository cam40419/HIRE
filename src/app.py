# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from Evaluator import Evaluator  # import your Evaluator class
from Resume import Resume        # import your Resume class and other necessary classes
import json
from Resume import Resume
from utils import *

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '../uploads/'
app.secret_key = 'supersecretkey'

# Route to render the HTML form
@app.route('/')
def index():
    return render_template('upload.html')

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['resume']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    # Get the job title from the form
    job_title = request.form.get('jobTitle')

    if job_title is None or job_title == "":
        flash('No job title selected')
        return redirect(request.url)

    if file.filename == '' or not job_title:
        flash('Please upload a file and select a job title.')
        return redirect(request.url)

    # Save the file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Assume a function parse_resume(file_path) to convert the uploaded file into a Resume object
    uploaded_resume = resume_from_file(file_path)  # You need to implement or import this

    # Create an Evaluator instance and evaluate the resume
    evaluator = Evaluator(job_title, uploaded_resume)
    scores, feedback = evaluator.evaluate()

    # Redirect to the feedback page and pass the feedback data
    return redirect(url_for('feedback', scores=json.dumps(scores), feedback=json.dumps(feedback)))

# Route to display feedback
@app.route('/feedback')
def feedback():
    feedback = session.get('feedback', 'No feedback available.')
    job_title = session.get('job_title', 'Unknown job title')
    return render_template('feedback.html', feedback=feedback, job_title=job_title)

if __name__ == "__main__":
    # Ensure the upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)
