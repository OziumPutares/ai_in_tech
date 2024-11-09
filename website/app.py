from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint="https://educationhackathon.openai.azure.com/",
api_key="F4t6ZhKWbThgotYQuaNURBVcJsDcqL4xkebqwPiVrVHw3s8d7dTjJQQJ99AKACfhMk5XJ3w3AAABACOGoNkI",
    api_version="2024-08-01-preview",
)

def getResponse(prompt):
    # Function that gets AI generated flashcards and returns
    response = client.chat.completions.create(
        model="gpt-4o",  # model = "deployment_name".
        messages=[
            {"role": "system", "content": "Create as text based format for flashcards using the users subject, level, passions and topic also don't include any remarks and include commas between the question and answer and a semicolon between an answer and the next question and provide it in plain text"},
            {"role": "user", "content": f"{prompt}"},
        ],
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

# Route to serve the HTML file
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the AI prompt
@app.route('/send-prompt', methods=['POST'])
def send_prompt():
    # Gets inputted text box
    data = request.json
    prompt = data.get('prompt')

    # Parse AI input
    if not prompt:
        return jsonify({"response": "Please enter a prompt."}), 400
    response = getResponse(prompt)
    response.replace('\n', '')
    result1 = ""
    result2 = ""
    result1 = response.split(';')
    for i in result1:
    # Provied parsed output
        print(f"Question is{i.split(',')[0]}")
        print(f"Answer is{i.split(',')[1]}")
    # Mock AI response (replace this with actual AI logic if needed)
    # Provied parsed output in website
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)

