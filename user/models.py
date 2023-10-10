from django.db import models
from django.contrib.auth.models import User, AbstractUser
from books.models import Request


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    class Role(models.IntegerChoices):
        ADMIN = 1, "Admin",
        LIBRARIAN = 2, "Librarian",
        USER = 3, "User"
    role = models.PositiveSmallIntegerField(
        choices=Role.choices, default=Role.USER)

    def issued_books(self):
        return Request.objects.filter(user=self, status=Request.Status.ISSUED).count()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Gender(models.IntegerChoices):
        MALE = 1, "Male"
        FEMALE = 2, "Female"
        OTHER = 3, "Others"
    gender = models.IntegerField(choices=Gender.choices, default=Gender.MALE)
    phone_number = models.CharField(max_length=13, unique=True) #, validators=[RegexValidator(r'^03\d{11}$')])

    def __str__(self):
        return self.user.username
