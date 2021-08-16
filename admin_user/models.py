  

from custom_user.models import User, UserManager
from custom_user.models import Role

# Admin manager to create admins
class AdminManager(UserManager):
    def create_admin(self, email):
        admin = self.create_user(email=self.normalize_email(email), role=Role.ADMIN)
        admin.save()
        return admin

#Admin model which extends User model
class Admin(User):
    # add model fields specific to admin if any here

    objects = AdminManager()

    def __str__(self):
        return str(self.email)
