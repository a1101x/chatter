from django.contrib.auth import get_user_model

User = get_user_model()


class EmailOrUsernameModelBackend(object):
    """
    Custom backend for authentication.
    Can login with username or email.
    """
    def authenticate(self, username=None, password=None):
        """
        Auth method using both username and email.
        """
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)

            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Get user with user id.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
