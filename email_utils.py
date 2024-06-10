from flask_mail import Mail, Message

# Inisialisasi objek Mail
mail = Mail()

def send_email(subject, sender, recipients, body):
    """Mengirim email menggunakan Flask-Mail."""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = body
    mail.send(msg)

    # Contoh penggunaan:
    # send_email('Welcome to Recipe App', 'noreply@recipe-app.com', ['user@example.com'], 'Welcome to Recipe App!')
