from flask import Flask, render_template, request, jsonify
import TurboTalk_Custom

app = Flask(__name__)

def process_message(text):
    """
    Process the incoming text using TurboTalk_Custom to generate responses.
    """
    # Define parameters for TurboTalk
    company_name = "Rango Productions"
    bot_name = "Rango AI"
    behaviour = "Friendly"
    user_message = text

    # Generate response using TurboTalk
    TurboTalk_Custom.turbo_talk_instance.give_response(
        company_name,
        bot_name,
        behaviour,
        user_message
    )

    # Get the response
    response = TurboTalk_Custom.turbo_talk_instance.get_response()

    return response

@app.route('/')
def home():
    # Serve index.html from the templates folder
    return render_template('index.html')

@app.route('/process_voice', methods=['POST'])
def process_voice():
    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text:
            raise ValueError("No text provided")

        # Get the user's IP address
        user_ip = request.remote_addr
        print(f"User IP: {user_ip}")

        # Process the text and get response
        response = process_message(text)

        return jsonify({
            'response': response,
            'status': 'success',
            'user_ip': user_ip
        })

    except ValueError as ve:
        return jsonify({
            'response': str(ve),
            'status': 'error'
        }), 400
    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error for debugging
        return jsonify({
            'response': "An internal error occurred. Please try again later.",
            'status': 'error'
        }), 500

if __name__ == '__main__':
    # Run the Flask app on all available network interfaces
    app.run(host='0.0.0.0', port=5000, debug=False)
