from dotenv import load_dotenv
from openai import AsyncOpenAI
# from openai_agents import Agent, Runner, trace, function_tool, OpenAIChatCompletionsModel, input_guardrail, GuardrailFunctionOutput
from agents import Agent, Runner, trace, function_tool, input_guardrail, GuardrailFunctionOutput
from typing import Dict
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
from pydantic import BaseModel
from openai.types.responses import ResponseTextDeltaEvent
import asyncio

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

# Instructions for different job seeker agent styles
instructions1 = """
You are a professional job seeker assistant working for JobSeekerAI, \
a platform that helps job seekers craft tailored cold emails for job applications. \
You write formal, well-structured cold emails to hiring managers, showcasing the candidate's skills and qualifications in a serious and professional manner.

When writing cold emails:
1. Start with a professional greeting
2. Introduce yourself and express interest in the position
3. Highlight relevant skills and experience
4. Explain why you're interested in the company
5. End with a call to action
6. Keep the tone professional but engaging
7. Include a subject line
8. Make it personalized to the specific company and position
"""

instructions2 = """
You are a creative job seeker assistant working for JobSeekerAI, \  
a platform that helps job seekers stand out by crafting personalized cold emails. \
You write witty and engaging cold emails that capture the hiring manager's attention, showcasing the candidate's qualifications in a fun and memorable way.

When writing cold emails:
1. Start with an attention-grabbing opening
2. Use creative language and storytelling
3. Highlight unique aspects of the candidate
4. Show enthusiasm and personality
5. End with a memorable call to action
6. Keep it engaging and memorable
7. Include a creative subject line
8. Make it stand out from typical job applications
"""

instructions3 = """
You are a results-driven job seeker assistant working for JobSeekerAI, \
a platform designed to help job seekers craft short and impactful cold emails. \
You write concise, to-the-point cold emails that quickly convey the candidate's qualifications and interest in the job, ensuring the hiring manager can easily understand the candidate's value.

When writing cold emails:
1. Start with a direct, clear opening
2. Get to the point quickly
3. Focus on key achievements and metrics
4. Show clear value proposition
5. End with a specific call to action
6. Keep it concise and impactful
7. Include a clear subject line
8. Emphasize results and outcomes
"""

# Create the job seeker agents
job_seeker_agent1 = Agent(
    name="Professional Job Seeker Agent",
    instructions=instructions1,
    model="gpt-4o"
)

job_seeker_agent2 = Agent(
    name="Engaging Job Seeker Agent",
    instructions=instructions2,
    model="gpt-4o"
)

job_seeker_agent3 = Agent(
    name="Busy Job Seeker Agent",
    instructions=instructions3,
    model="gpt-4o"
)

job_seeker_picker = Agent(
    name="job_seeker_picker",
    instructions="You pick the best cold job seeker email from the given options. \
Imagine you are a hiring manager and pick the one you are most likely to respond to. \
Do not give an explanation; reply with the selected email only.",
    model="gpt-4o"
)

@function_tool
def send_email(body: str):
    """ Send out an email with the given body to all sales prospects """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("muskankh03@gmail.com")  # Change to your verified sender
    to_email = To("muskankh03@gmail.com")  # Change to your recipient
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, "Job Seeker email", content).get()
    response = sg.client.mail.send.post(request_body=mail)
    return {"status": "success"}

description = "Write a cold job seeker email"

tool1 = job_seeker_agent1.as_tool(tool_name="job_seeker_agent1", tool_description=description)
tool2 = job_seeker_agent2.as_tool(tool_name="job_seeker_agent2", tool_description=description)
tool3 = job_seeker_agent3.as_tool(tool_name="job_seeker_agent3", tool_description=description)

tools = [tool1, tool2, tool3, send_email]

instructions = """
You are a job seeker manager working for JobSeekerAI. You generate cold job seeker emails using the tools provided. 
You try all 3 job_seeker_agent tools once before choosing the best one. \
you select the most professional one based on the following criteria: tone, structure, and relevance. 
After selection, you use the send_email tool to send the chosen email.
"""

job_seeker_manager = Agent(
    name="Job Seeker Manager",
    instructions=instructions,
    tools=[tool1, tool2, tool3, send_email],  # Including the send_email tool
    model="gpt-4o"
)

subject_instructions = "You can write a subject for a cold job seeker email. \
You are given a message and you need to write a subject for an email that is likely to get a response."

html_instructions = "You can convert a text email body to an HTML email body. \
You are given a text email body which might have some markdown \
and you need to convert it to an HTML email body with simple, clear, compelling layout and design."

subject_writer = Agent(name="Email subject writer", instructions=subject_instructions, model="gpt-4o")
subject_tool = subject_writer.as_tool(tool_name="subject_writer", tool_description="Write a subject for a cold job seeker email")

html_converter = Agent(name="HTML email body converter", instructions=html_instructions, model="gpt-4o")
html_tool = html_converter.as_tool(tool_name="html_converter",tool_description="Convert a text email body to an HTML email body")

@function_tool
def send_html_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send out an email with the given subject and HTML body to all sales prospects """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("muskankh03@gmail.com")  # Change to your verified sender
    to_email = To("muskankh03@gmail.com")  # Change to your recipient
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    return {"status": "success"}

email_tools = [subject_tool, html_tool, send_html_email]

instructions ="You are an email formatter and sender. You receive the body of an email to be sent. \
You first use the subject_writer tool to write a subject for the email, then use the html_converter tool to convert the body to HTML. \
Finally, you use the send_html_email tool to send the email with the subject and HTML body."


emailer_agent = Agent(
    name="Email Manager",
    instructions=instructions,
    tools=email_tools,
    model="gpt-4o",
    handoff_description="Convert an email to HTML and send it")

tools = [tool1, tool2, tool3]
handoffs = [emailer_agent]

job_seeker_manager_instructions = """
You are a job seeker manager working for ComplAI. You use the tools given to you to generate cold job seeker emails. 
You never generate job seeker emails yourself; you always use the tools. 
You try all 3 job seeker agent tools at least once before choosing the best one. 
You can use the tools multiple times if you're not satisfied with the results from the first try. 
You select the single best email using your own judgement of which email will be most effective. 
After picking the best email, you hand it off to the Email Manager agent to format and send the email, without asking for further confirmation from the user.
"""

job_seeker_manager = Agent(
    name="Job Seeker Manager",
    instructions=job_seeker_manager_instructions,
    tools=tools,
    handoffs=handoffs,
    model="gpt-4o")

class NameCheckOutput(BaseModel):
    is_name_in_message: bool
    name: str

guardrail_agent = Agent( 
    name="Name check",
    instructions="Check if the user is including someone's personal name in what they want you to do.",
    output_type=NameCheckOutput,
    model="gpt-4o"
)

@input_guardrail
async def guardrail_against_name(ctx, agent, message):
    result = await Runner.run(guardrail_agent, message, context=ctx.context)
    is_name_in_message = result.final_output.is_name_in_message
    return GuardrailFunctionOutput(output_info={"found_name": result.final_output},tripwire_triggered=is_name_in_message)

careful_job_seeker_manager = Agent(
    name="Job Seeker Manager",
    instructions=job_seeker_manager_instructions,
    tools=tools,
    handoffs=[emailer_agent],
    model="gpt-4o",
    input_guardrails=[guardrail_against_name]
    )

message = "Send out a cold sales email addressed to Dear CEO from Alice"
