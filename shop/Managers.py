from django.contrib.auth.models import UserManager


class MyUserManager(UserManager):

    def create_user(self, email, password, is_active=True, is_admin=False, is_staff=False, is_superuser=False ):

        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)  # change password to hash
        user.is_active = is_active
        user.is_admin = is_admin
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password,
            is_staff=True,
            is_admin=True,
            is_superuser=True,
        )
        return user
