import re

with open('user_auth/api/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(
    r'      token = default_token_generator\.make_token\(user\).*?</html>\",',
    r'''      token = default_token_generator.make_token(user)
      uid = urlsafe_base64_encode(force_bytes(user.pk))
      
      reset_link = f"http://localhost:5500/reset_password.html?uid={uid}&token={token}"   
      send_mail(
          subject="Password Reset Request for Videoflix",
          message=f"Hello,\n\nClick the following link to reset your password:\n\n{reset_link}",
          from_email="noreply@videoflix.com",
          recipient_list=[email],
          html_message=f"<html><body><h2>Password Reset</h2><p>Click <a href='{reset_link}'>here</a> to reset your password.</p></body></html>",
      )
      return Response({"detail": "If an account with this email exists, a password reset email has been sent."}, status=status.HTTP_200_OK)''',
    text,
    flags=re.DOTALL
)

with open('user_auth/api/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
