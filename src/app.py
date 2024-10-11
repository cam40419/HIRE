# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

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


    if file.filename == '':
        flash('Please upload a file and select a job title.')
        return redirect(request.url)

    # Save the file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Redirect to the feedback page and pass the feedback data
    return redirect('/feedback')

# Route to display feedback
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

if __name__ == "__main__":
    # Ensure the upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)
