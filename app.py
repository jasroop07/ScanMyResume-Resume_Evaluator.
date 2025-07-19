
import joblib
from flask import (
    Flask,
    url_for,
    request,
    jsonify,
    redirect,
    flash,
    render_template,
    session,
    abort,
    render_template
)
import os
from forms import InputForm
from main_GEMINI import get_ats_feedback_GEMINI
from main_LLAMA import get_ats_feedback_LLAMA

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"

#model = joblib.load("model.joblib")

@app.route("/")
@app.route("/home")
def home():
    return render_template("home_css.html", title="Home")


@app.route("/process_resume", methods=["GET", "POST"])
def process_resume():
    resume_file = request.files['resume']
    job_desc = request.form['job_description']

    if not resume_file or not resume_file.filename.endswith('.pdf'):
        return "❌ Please upload a valid PDF file."


    # # Save resume file
    # file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
    # resume_file.save(file_path)


    # Call your model function to get feedback
    feedback = get_ats_feedback_LLAMA(resume_file, job_desc)

    # Pass it to ats.html
    return render_template("ats.html", title="ATS Result", feedback=feedback)








#ANOTHER WAY TO DO IT
# def home():
#     form = InputForm()
    
#     if form.validate_on_submit():
#         resume_file = form.resume.data
#         job_desc = form.job_description.data

#         if not resume_file.filename.endswith('.pdf'):
#             return "❌ Please upload a valid PDF file."

#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
#         resume_file.save(file_path)

#         # Process resume using LLAMA model
#         feedback = get_ats_feedback_LLAMA(file_path, job_desc)

#         return render_template("ats.html", title="ATS Result", feedback=feedback)

#     return render_template("home.html", title="ScanMyResume", form=form)



# @app.route("/ats")

# def ats():
#     return render_template("ats.html", title="ATS Result")





if __name__ == "__main__":
    app.run(debug=True)