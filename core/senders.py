from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template


def send_email(template, subject, context, to):
    try:
        html = get_template('mail/'+template+'.html').render(context)
        msg = EmailMessage(
            subject,
            html,
            'dongpardaz@gmail.com',
            to if isinstance(to, list) else [to],
        )
        msg.content_subtype = 'html'
        msg.send(fail_silently=False)
    except Exception as e:
        print(e)
