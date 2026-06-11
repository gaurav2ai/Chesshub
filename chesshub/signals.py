# chesshub/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from .models import Profile


@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    if not created:
        return

    # -------- PROFILE CREATE --------
    Profile.objects.create(
        user=instance,
        age=18,
        gender="O"
    )

    # -------- SAFETY CHECK --------
    if not instance.email:
        return

    if not settings.DEFAULT_FROM_EMAIL:
        return

    # -------- EMAIL CONTENT --------
    subject = "Welcome to ChessHub"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [instance.email]

    html_content = f"""
    <div style="font-family:Arial;padding:20px;">
        <h2>Welcome to ChessHub, {instance.first_name or "Player"}!</h2>
        <p>Your account has been successfully created.</p>
        <p>You can now:</p>
        <ul>
            <li>Book tournaments</li>
            <li>Manage slots</li>
            <li>Track holidays</li>
        </ul>
        <br>
        <strong>Team ChessHub</strong>
    </div>
    """

    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body="Welcome to ChessHub",
            from_email=from_email,
            to=to,
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=True)

    except Exception as e:
        print("WELCOME MAIL ERROR:", e)
