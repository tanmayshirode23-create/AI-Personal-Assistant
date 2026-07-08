from flask import Flask , render_template , request , jsonify
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/ask",methods=["post"])
def ask():
    question = request.form.get("question")

    response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = question,
            config=types.GenerateContentConfig(
                system_instruction="""
                    You are a helpful AI Personal Assistant.
                    - Give concise answers for simple questions.
                    - Give detailed explanations only when the user explicitly asks for them.
                    - Use bullet points and markdown.
                    """,
                temperature=0.7,
                max_output_tokens =4096,
            ),
        )
    print(response)
    answer = ""

    for part in response.candidates[0].content.parts:
        if hasattr(part, "text"):
            answer += part.text

    answer = answer.strip()

    return jsonify({"response": answer})

    print(response.candidates[0].finish_reason)
   
    

    

if __name__ == "__main__":
    app.run(debug=True)