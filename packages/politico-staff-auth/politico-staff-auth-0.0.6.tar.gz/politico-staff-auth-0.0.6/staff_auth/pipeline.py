# Imports from Django.  # NOQA
from django.conf import settings


# Imports from other dependencies.
from social_core.exceptions import AuthException


def associate_by_email(backend, details, user=None, *args, **kwargs):
    """"""
    # If there's already a user, we're not going to add anything here.
    if user:
        return None

    email = details.get('email')

    if email:
        # Are there existing accounts registered with the same email address?
        # Raise AuthException if multiple objects are observed.
        users = list(backend.strategy.storage.user.get_users_by_email(email))

        # Make sure user is active and their account is tied with another
        # Slack-provided auth instance.
        active_users = [
            user for user in users
            if user.is_active
            and user.social_auth.filter(provider="slack").count() > 0
        ]

        if len(active_users) == 0:
            return None
        elif len(active_users) > 1:
            raise AuthException(
                backend,
                " ".join(
                    [
                        "The given email address is associated with",
                        "multiple existing accounts."
                    ]
                )
            )
        else:
            return dict(user=active_users[0], is_new=False)


def promote_staffer_to_staff(backend, user, response, *args, **kwargs):
    """"""
    if backend.name == "slack" and kwargs["is_new"]:
        user.is_staff = True


def promote_manager_to_superuser(backend, user, response, *args, **kwargs):
    """"""
    if not hasattr(settings, "MANAGERS"):
        return

    manager_emails = [mgr_email for mgr_name, mgr_email in settings.MANAGERS]

    if user.email in manager_emails:
        user.is_staff = True
        user.is_superuser = True
