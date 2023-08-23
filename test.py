import json
import openai
import re
import sqlite3

from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE_NAME = 'test.db'
TABLE_NAME = 'properties'
ADDRESS_COL = 'address'
DESCRIPTION_COL = 'description'

def openai_query(prompt):
    # OpenAI API call
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
    # Extract address from the question
    pattern = r"\b[0-9]+\s([A-Z][A-Za-z]+)+(\s[A-Z][A-Za-z]+)*\b"
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    else:
        return None


@app.route('/ask', methods=['POST'])
def ask():
    try:
        question = json.loads(request.data).get("question")
    except:
        return jsonify({"error": "Invalid Request"}), 400

    if not question:
        return jsonify({"error": "Question not in the request"}), 400

    address = extract_address(question)
    if not address:
        return jsonify({"error": "Address not detected in the request"}), 400

    # Fetch description from the database
    try:
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()
        sql_query = "SELECT {} FROM {} WHERE {}=\"{}\"".format(DESCRIPTION_COL, TABLE_NAME, ADDRESS_COL, address)
        cursor.execute(sql_query)
        result = cursor.fetchone()
        connection.close()
    except:
        return jsonify({"error": "Database access failure"}), 400

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
