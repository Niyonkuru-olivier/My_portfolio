from flask import Flask, render_template, request, redirect, flash, url_for
import requests, os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key_here")

# Use Resend Email API (works even on Render free tier)
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "your_resend_api_key_here")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "oniyonkuru233@gmail.com")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        name = request.form['name']
        sender_email = request.form['email']
        message_content = request.form['message']

        # Prepare email content
        subject = f"New Message from {name}"
        html_content = f"""
        <p><strong>You have received a new message from your portfolio contact form:</strong></p>
        <p><strong>Name:</strong> {name}<br>
        <strong>Email:</strong> {sender_email}</p>
        <p><strong>Message:</strong><br>{message_content}</p>
        """

        # Send via Resend API
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": f"{name} <onboarding@resend.dev>",
                "to": [RECEIVER_EMAIL],
                "subject": subject,
                "html": html_content
            }
        )

        if response.status_code == 200:
            flash('✅ Message sent successfully! Thank you for contacting me.', 'success')
        else:
            print(response.text)
            flash('❌ Error sending message. Please try again later.', 'danger')

        return redirect(url_for('index'))

    except Exception as e:
        print(f"Error: {e}")
        flash('❌ Error sending message. Please try again later.', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
