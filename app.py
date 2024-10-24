import os
import requests
from flask import Flask, request ,jsonify,render_template
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from twilio.rest import Client
import base64
# Load environment variables
from openai_api import ChatGPT_conversation


load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
HUGGING_FACE_API_TOKEN = os.getenv('HUGGING_FACE_API_TOKEN')

app = Flask(__name__)
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


@app.route("/message", methods=["GET", "POST"])
def send_whatsapp():
    # data = request.get_json()
    # reciepient_number=data.get("reciepient_number")
    # message_body=data.get("message_body")
    if request.method == 'POST':
        reciepient_number = request.form['From']
        message_body = request.form['Body']

        # print('reciepient_number,message_body...',reciepient_number,message_body)
        conversation_144=[]
        conversation_144.append({'role': 'system', 'content': message_body})

        result=ChatGPT_conversation(conversation_144)
        result=result[-1]['content'].strip()
        print('result...',result)
        if 'whatsapp' in reciepient_number:
            pass
        else:
            reciepient_number="whatsapp:"+str(reciepient_number)
        try:
            message = client.messages.create(
                body=result,
                from_=os.getenv('FROM'),
                to=reciepient_number,
                # media_url=["https://huggingface.co/spaces/Kwai-Kolors/Kolors-Virtual-Try-On/resolve/main/assets/examples/model1.png"],
            )
            print('message....',message.sid)
            return jsonify({"Status": "Success","Result":result}),200
        except:
            return jsonify({"Status": "Fail"}), 500
    else:
        return render_template('chatbot.html')

if __name__ == "__main__":
    app.run(debug=True)