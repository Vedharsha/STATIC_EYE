from flask import Blueprint, render_template, request, jsonify, send_file, redirect,current_app
from app.analysis import hybrid_analysis
from app.reports import generate_report
from app.database import db, AnalysisResult, UserFeedback
import os

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        apk_file = request.files["apk_file"]

        # Perform hybrid analysis
        analysis_result = hybrid_analysis(apk_file)

        # Generate report
        generate_report(analysis_result)

        # Save result to database
        new_result = AnalysisResult(apk_name=apk_file.filename, result=analysis_result)
        db.session.add(new_result)
        db.session.commit()

        return render_template("index.html", analysis_result=analysis_result)

    return render_template("index.html", analysis_result={})

@main.route("/report")
def report():
    file_path = os.path.join(current_app.root_path, 'static', 'static_analysis_report.png')
    return send_file(file_path, mimetype='image/png')

    
@main.route("/verify-result/<int:result_id>", methods=["GET", "POST"])
def verify_result(result_id):
    result = AnalysisResult.query.get_or_404(result_id)
    
    if request.method == "POST":
        user_feedback = request.form["feedback"]
        new_feedback = UserFeedback(analysis_result_id=result_id, feedback=user_feedback)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect("/")

    return render_template("verify_result.html", result=result)