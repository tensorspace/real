import json
import openai
import re
import sqlite3

from flask import Flask, request, jsonify

app = Flask(__name__)


# OpenAI API call
def openai_query(prompt):
    openai.api_key = "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"
    primer = f"""You are Q&A bot. A highly intelligent system that answers
user questions based on the information provided by the user above
each question..
"""

    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": primer},
            {"role": "user", "content": prompt}
        ],
        max_size=800
    )
    response = res['choices'][0]['message']['content']
    return response


def extract_address(text):
    pattern = r"\b[0-9]+\s([A-Z][a-zA-Z]]+)+(\s[A-Z][a-zA-Z]]+)*\b"
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    else:
        return None


@app.route('/ask', methods=['POST'])
def ask():
    question = json.loads(request.data).get("question")
    address = extract_address(question)

    if not address:
        return jsonify({"error": "Address not detected in the request"}), 400

    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()
    cursor.execute("SELECT description FROM properties WHERE address=?", (address,))
    result = cursor.fetchone()
    connection.close()

    if not result:
        return jsonify({"error": "Address not found in database"}), 400

    description = result[0]
    prompt = (f"The description of the house located at {address} is \"{description}\". Use the description to answer the "
              f"question: {question}")

    # OpenAI API call
    response = openai_query(prompt)

    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(debug=True)
