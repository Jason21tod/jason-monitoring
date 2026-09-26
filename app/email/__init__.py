from requests import post
import os


JASON_WATCHER_URL = str(os.environ.get("JASON_WATCHER_URL"))
EMAIL_APP_PASSWORD = str(os.environ.get("EMAIL_APP_PASSWORD"))
JASON_WATCHER_KEY = str(os.environ.get("JASON_WATCHER_KEY"))

if JASON_WATCHER_KEY == "None":
    raise ValueError("Could not found Watcher Key")
if JASON_WATCHER_URL == "None":
    raise ValueError("Could not found Watcher Url")
if EMAIL_APP_PASSWORD == "None":
    raise ValueError("Could not found Email App Pw")


def report_error_by_email(subject: str, body: str):
    print("sending error to subscribed watchers...")
    data = {
            "subject": subject,
            "error": body,
            "email_pw": EMAIL_APP_PASSWORD,
            "jason_wk": JASON_WATCHER_KEY
        }
    post(url=JASON_WATCHER_URL, data=data)