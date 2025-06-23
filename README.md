# Cold Email Agent

## Overview

The **Cold Email Agent** is an AI-powered tool designed to help job seekers craft personalized and professional cold emails for job applications. Using OpenAI's API and advanced agent orchestration, this project generates tailored job application emails based on user input such as name, skills, job position, company, and more. The tool generates multiple email drafts, selects the best option, formats it, and sends it via email.

This project leverages Flask for the web application and integrates OpenAI's GPT model for generating email content, providing an intuitive and automated solution for job seekers.

## Features

* **Job Application Email Generation**: Automatically generates personalized cold emails tailored to specific job applications.
* **Multiple Email Tones**: Choose between various tones (e.g., professional, creative, concise) for the email.
* **Automatic Email Selection**: The system evaluates multiple email drafts and selects the most effective one.
* **Email Formatting**: Converts the selected draft into a properly formatted HTML email.
* **Email Sending**: Uses a third-party email service (e.g., SendGrid) to send the generated email directly to the recipient.
* **User-Friendly Interface**: A simple and intuitive UI where users can input their details and receive the generated email.

## Requirements

* Python 3.11 or higher
* Flask 2.x or higher
* OpenAI API Key (for generating email content)
* SendGrid API Key (for sending emails)

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/MuskanKhandelwal/Cold_Email_AI_Agent.git
   cd Cold_Email_AI_Agent
   ```

2. Set up a virtual environment:

   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:

4. Set up environment variables for the OpenAI and SendGrid API keys:

   * Create a `.env` file in the root directory.
   * Add the following to the `.env` file:

     ```
     OPENAI_API_KEY=your_openai_api_key_here
     SENDGRID_API_KEY=your_sendgrid_api_key_here
     ```

### Dependencies

* **Flask**: A lightweight web framework for Python to build the web application.
* **OpenAI API**: The API for generating text-based email drafts using GPT models.
* **SendGrid API**: Used for sending the generated email via email services.
* **Asyncio**: To handle asynchronous tasks like waiting for email generation.
* **dotenv**: For securely loading environment variables.

## How It Works

1. **User Input**: The user inputs their job application details via a simple form, including their name, contact information, company name, position, and skills.

2. **Email Generation**: The **Job Seeker Manager** agent orchestrates multiple **Job Seeker Agents** that generate email drafts based on the user’s input.

3. **Email Selection**: The **Job Seeker Manager** evaluates the generated drafts and selects the most effective email based on tone, structure, and relevance.

4. **Email Formatting**: The selected email is formatted into an HTML email using the **Email Manager** agent.

5. **Email Sending**: The formatted email is then sent to the user via SendGrid.

## Usage

1. **Run the Flask App**:

   Start the Flask development server by running:

   ```bash
   python app.py
   ```

2. **Access the Web Interface**:

   Once the server is running, open your web browser and navigate to `http://127.0.0.1:5000/`.

   * Input the necessary details in the form (name, contact info, company, job position, skills, etc.).
   * Submit the form to generate and receive your tailored job application email.

## File Structure

```
/cold-email-agent
├── /templates                # HTML templates for Flask
│   ├── index.html            # Form for user input
│   └── result.html           # Display the generated email
├── app.py                    # Main Flask application
├── your_agent_tools.py       # Job seeker agent logic
├── .env                      # Environment variables (API keys)
└── README.md                 # Project documentation
```

## Troubleshooting

1. **500 Server Error**: Ensure your API keys for OpenAI and SendGrid are set up correctly in the `.env` file.
2. **Missing Dependencies**: Run `pip install -r requirements.txt` to ensure all dependencies are installed.
3. **Form Not Submitting**: Check the Flask logs for any issues related to the form submission or agent processing.

