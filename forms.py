from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired



class InputForm(FlaskForm):
    resume = FileField(
        "Upload Resume (PDF only)",
        validators=[
            FileRequired(),
            FileAllowed(['pdf'], 'Only PDF files are allowed.')
        ]
    )
    
    job_description = TextAreaField(
        "Job Description",
        validators=[DataRequired()]
    )
    
    submit = SubmitField("Scan Resume")