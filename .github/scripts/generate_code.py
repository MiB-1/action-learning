import os
import openai
import subprocess
import sys

openai.api_key = os.getenv("OPENAI_API_KEY")
issue_title = sys.argv[1]
issue_body = sys.argv[2]

promt = f"""
you are a code assistant. Based on the following issue title and description, generate a React component or code update:

Title: {issue_title}
Description: {issue_body}
"""

response = openai.ChatCompletion.create(
  model="gpt-4",
  message=[{"role": "user", "content": promt}]
)

code = response['choices'][0]['message']['content']

filename = "src/NewComponent.jsx"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as f:
  f.write(code)

branch = f"ai/codegen_{issue_title.replace(' ', '-').lower()}"
subprocess.run(["git", "checkout", "-b", branch])
subprocess.run(["git", "add", filename])
subprocess.run(["git", "commit", "-m", f"🤖 AI-generated code for: {issue_title}"])
subprocess.run(["git", "push", "origin", branch])

subprocess.run([
  "gh", "pr", "create",
  "--title", f"AI-generated: {issue_title}",
  "--body", "This PR was generated automatically by AI based on issue content.",
  "--base", "main",
  "--head", branch
])
