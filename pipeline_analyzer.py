import os
import sys
from google import genai

def analyze_pipeline_failure(logs):
    """
    Analyzes Jenkins pipeline failure logs using Google Gemini and returns remediation steps.
    Only error lines are sent to Gemini to reduce token usage.
    """
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return "Error: GEMINI_API_KEY environment variable not set."

    # Extract only error lines (case-insensitive)
    error_lines = []
    for line in logs.splitlines():
        if any(keyword in line.lower() for keyword in ["error", "exception", "fail", "fatal", "traceback"]):
            error_lines.append(line)
    error_log = "\n".join(error_lines) if error_lines else logs

    prompt = f"""
    You are an expert DevOps engineer specializing in CI/CD pipelines, Python, pytest, and Docker builds.
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
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Error calling Gemini API: {str(e)}"

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
