import os
import sys
import openai
from openai import OpenAI

def analyze_pipeline_failure(logs):
    """
    Analyzes Jenkins pipeline failure logs using OpenAI and returns remediation steps.
    Only error lines are sent to OpenAI to reduce token usage.
    """
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # Extract only error lines (case-insensitive)
    error_lines = []
    for line in logs.splitlines():
        if any(keyword in line.lower() for keyword in ["error", "exception", "fail", "fatal", "traceback"]):
            error_lines.append(line)
    error_log = "\n".join(error_lines) if error_lines else logs

    prompt = f"""
    You are an expert DevOps engineer specializing in CI/CD pipelines, Java, Maven, and Docker builds.
    The following Jenkins pipeline failed. Analyze the error logs below and provide:
    1. The root cause of the failure.
    2. Detailed remediation steps to fix the issue.
    3. Any preventive measures for the future.

    Error Logs:
    {error_log}

    Response Format:
    - Root Cause: [Brief explanation]
    - Remediation Steps: [Numbered list of steps]
    - Prevention: [Suggestions]
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant for CI/CD troubleshooting."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}"

if __name__ == "__main__":
    # Read logs from stdin or file
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
        with open(log_file, 'r') as f:
            logs = f.read()
    else:
        logs = sys.stdin.read()

    remediation = analyze_pipeline_failure(logs)
    print("=== AI Remediation Analysis ===")
    print(remediation)
    print("===============================")