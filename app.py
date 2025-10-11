from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Flask-Mail configuration (use Gmail App Password)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'oniyonkuru233@gmail.com'
app.config['MAIL_PASSWORD'] = 'dqbw wyni rgts pzsg'  # Gmail App Password

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        name = request.form['name']
        sender_email = request.form['email']
        message_content = request.form['message']

        msg = Message(
            subject=f"New Message from {name}",
            sender=app.config['MAIL_USERNAME'],
            recipients=['oniyonkuru233@gmail.com']  # You receive the email
        )
        msg.body = f"""
You have received a new message from your portfolio contact form:

Name: {name}
Email: {sender_email}

Message:
{message_content}
"""

        mail.send(msg)
        flash('✅ Message sent successfully! Thank you for contacting me.', 'success')
        return redirect(url_for('index'))

    except Exception as e:
        print(f"Error: {e}")
        flash('❌ Error sending message. Please try again later.', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
