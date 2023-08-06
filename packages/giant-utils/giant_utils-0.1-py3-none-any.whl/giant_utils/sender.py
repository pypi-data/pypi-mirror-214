from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email_from_template(
    to,
    email_subject: str,
    txt_template: str,
    html_template: str = None,
    pk: int = None,
    model_class: object = None,
    scheme: str = "",
    host: str = "",
):
    """
    A core template method which sends an email given the following parameters:
        obj: Usually set as self, but is the instance of the model you are using
        to: The recipient of the mail
        txt_template: this is the path to the txt version of the template
        html_template: this is the path to the html version of the template
        pk: The model instance's pk to be pulled through into the email templates.
        model_class: The model class to be pulled through into the email templates.
        host: The site's host domain to be pulled through into the email templates
            for correct image url.
    """
    context = {
        "subject": email_subject,
        "scheme": scheme,
        "host": host,
    }

    if model_class and pk:
        instance = model_class.objects.get(pk=pk)
        context = {"object": instance, "model": model_class, **context}

    txt_result = render_to_string(txt_template, context=context)

    email = EmailMultiAlternatives(
        subject=context["subject"],
        body=txt_result,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to,
    )

    if html_template:
        html_result = render_to_string(html_template, context=context)
        email.attach_alternative(
            content=html_result,
            mimetype="text/html",
        )

    email.send()
