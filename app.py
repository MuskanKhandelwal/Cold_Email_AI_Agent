from flask import Flask, render_template, request, redirect, url_for
from agents import Runner, Agent  # Import from openai_agents library
from cold_email import job_seeker_manager  # Import your job seeker agent
from agents import Agent, Runner, trace, function_tool, input_guardrail, GuardrailFunctionOutput
import asyncio
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
async def index():
    if request.method == "POST":
        # Collect user input from the form
        user_name = request.form["user_name"]
        contact_info = request.form["contact_info"]
        company_name = request.form["company_name"]
        hiring_manager = request.form["hiring_manager"]
        job_position = request.form["job_position"]
        skills = request.form["skills"]
        
        # Construct the input for the job seeker agent
        email_input = f"""
        Candidate: {user_name}
        Contact Info: {contact_info}
        Company: {company_name}
        Hiring Manager: {hiring_manager}
        Position: {job_position}
        Skills: {skills}
        
        Write a cold email tailored to this job application using the provided information.
        """
        
        
        with trace("Protected Automated Job Seeker"):
            result = await Runner.run(job_seeker_manager, email_input)
        print(result)
    
        return render_template("result.html", email=result)

    return  render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
