from django.db import models
from django.contrib.auth.models import User, AbstractUser
from books.models import Request


class User(AbstractUser):
    """Overriden Abstract User class to include email and role"""
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    class Role(models.IntegerChoices):
        """Role class to signify which role the user currently has permissions to"""
        ADMIN = 1, "Admin",
        LIBRARIAN = 2, "Librarian",
        USER = 3, "User"
    role = models.PositiveSmallIntegerField(
        choices=Role.choices, default=Role.USER)

    def issued_books(self):
        """Returns the current number of books issued to the user, max: 3"""
        return Request.objects.filter(user=self, status=Request.Status.ISSUED).count()


class UserProfile(models.Model):
    """UserProfile model to handle the gender and phone_number fields"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Gender(models.IntegerChoices):
        """Gender class to signify the gender of the userss"""
        MALE = 1, "Male"
        FEMALE = 2, "Female"
        OTHER = 3, "Others"
    gender = models.IntegerField(choices=Gender.choices, default=Gender.MALE)
    # Max 13 length phone number according to Pakistan mobile numbers
    phone_number = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.user.username
