from flask import Flask, render_template, request, jsonify
import groq

app = Flask(__name__)


client = groq.Groq(api_key="Your_API_Key")


initial_context = """
You are a cancer prediction chatbot. Your role is to gather information about the user's symptoms and risk factors, 
and provide a preliminary assessment of their cancer risk. You should ask relevant questions about their medical history, 
lifestyle, and specific symptoms. Based on their responses, you can offer a general risk assessment and suggestions for 
next steps, such as recommending a doctor's visit or specific screenings. Remember, you are not a substitute for 
professional medical advice, and you should always encourage users to consult with a healthcare professional for 
an accurate diagnosis and personalized advice.
Don't answer like you are not an doctor. Just give me advice me about the problem that i am specifying.Dont Hallucinate with the basic data.
"""

conversation_history = [{"role": "system", "content": initial_context}]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    conversation_history.append({"role": "user", "content": user_message})
    
   
    response = client.chat.completions.create(
        messages=conversation_history,
        model="mixtral-8x7b-32768",  
        max_tokens=150,
        temperature=0.7
    )
    
    bot_response = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": bot_response})
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
