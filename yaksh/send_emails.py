# Local imports
try:
    from string import letters
except ImportError:
    from string import ascii_letters as letters
from string import digits, punctuation
import hashlib
from textwrap import dedent
import os

# Django imports
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


def generate_activation_key(username):
    """ Generate hashed secret key for email activation """
    chars = letters + digits + punctuation
    secret_key = get_random_string(20, chars)
    return hashlib.sha256((secret_key + username).encode('utf-8')).hexdigest()


def send_user_mail(user_mail, key):
    """ Send mail to user whose email is to be verified
        This function should get two args i.e user_email and secret_key.
        The activation url is generated from settings.PRODUCTION_URL and key.
    """
    try:
        to = user_mail
        subject = 'Yaksh Email Verification'
        message = dedent("""\
                To activate your account and verify your email address,
                please click the following link:
                {0}/exam/activate/{1}
                If clicking the link above does not work,
                copy and paste the URL in a new browser window instead.
                For any issue, please write us on {2}

                Regards,
                {3}
            """.format(settings.PRODUCTION_URL, key, settings.REPLY_EMAIL,
                       settings.SENDER_NAME
                       )
            )

        send_mail(subject, message, settings.SENDER_EMAIL, [to])

        msg = "An activation link is sent to your registered email.\
                        Please activate the link within 20 minutes."
        success = True

    except Exception as exc_msg:
        msg = """Error: {0}. Please check your email address.\
                If email address is correct then
                Please contact {1}.""".format(exc_msg, settings.REPLY_EMAIL)
        success = False

    return success, msg


def send_bulk_mail(subject, email_body, recipients, attachments):
    try:
        text_msg = ""
        msg = EmailMultiAlternatives(subject, text_msg, settings.SENDER_EMAIL,
                                     [settings.SENDER_EMAIL], bcc=recipients
                                     )
        msg.attach_alternative(email_body, "text/html")
        if attachments:
            for file in attachments:
                path = default_storage.save(
                    os.path.join('attachments', file.name),
                    ContentFile(file.read())
                )
                msg.attach_file(os.sep.join((settings.MEDIA_ROOT, path)),
                                mimetype="text/html"
                                )
                default_storage.delete(path)
        msg.send()

        message = "Email Sent Successfully"

    except Exception as exc_msg:
        message = """Error: {0}. Please check email address.\
                If email address is correct then
                Please contact {1}.""".format(exc_msg, settings.REPLY_EMAIL)

    return message


def send_workshop_course_mail(instructor_mail, coordinator_mail, course_name,
                        course_code, new_user=False, instructor_username = None, instructor_password = None):
    """ Send mail to instructor and coordinator regarding course creation 
        This function should get six args i.e
        instructor_mail, coordinator_mail, instructor_username, instructor_password, course_name, course_code,
    """
    try:
        to = instructor_mail
        subject = 'Yaksh Course Creation'
        message = dedent("""\
                We received a request to create a course for you on yaksh portal.
                Your request has been processed and a course {0} is created with the course code :{1}
                You can now login to the yaksh portal and verify the course design.
            """.format(course_name, course_code)
            )
        if new_user:
            message=dedent("""\
                                Your account has been created in the yaksh site,
                                with the following credentials\n USERNAME : {0}\n and PASSWORD : {1}\n\n
                                you can now login to the site and change your password.
                            """.format(instructor_username,instructor_password)
                        ).join(message.splitlines())
        send_mail(subject, message, settings.SENDER_EMAIL, [to])

        to = coordinator_mail
        message = dedent("""\
                We received a request to create a course for your workshop on yaksh portal.
                Ask your students to signup/login to the yaksh site and enroll to the course : {0} 
                by searching with the course code : {1}
            """.format(course_name, course_code)
            )
        send_mail(subject, message, settings.SENDER_EMAIL, [to])
        msg = "An email has been sent to both instructor and coordinator."
        success = True

    except Exception as exc_msg:
        msg = """Error: {0}. Please check your email address.\
                If email address is correct then
                Please contact {1}.""".format(exc_msg, settings.REPLY_EMAIL)
        success = False

    return success, msg
