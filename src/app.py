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

    # Get the job title from the form
    job_title = request.form.get('jobTitle')

    if job_title is None or job_title == "":
        flash('No job title selected')
        return redirect(request.url)

    if file:
        # Save the file to the upload folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Process the file and job title (this is where you'd add your AI processing code)
        print(f"File {file.filename} uploaded successfully for job title: {job_title}")

         # Simulated feedback processing (replace with AI processing code)
        feedback = f"Resume uploaded successfully for the job title: {job_title}. Analysis and feedback would go here."

        # Store feedback and job title in session for retrieval on feedback page
        session['feedback'] = feedback
        session['job_title'] = job_title

        # You can also return a message or redirect to another page
        return redirect('/feedback')

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
