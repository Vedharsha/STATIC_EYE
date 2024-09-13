from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apk_name = db.Column(db.String(100), nullable=False)
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)
    result = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f'<AnalysisResult {self.apk_name}>'

class UserFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    analysis_result_id = db.Column(db.Integer, db.ForeignKey('analysis_result.id'), nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<UserFeedback for AnalysisResult {self.analysis_result_id}>'

def init_db(app):
   # db.init_app(app)
    with app.app_context():
        db.create_all()
