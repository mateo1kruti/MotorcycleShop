from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.db.models import Sum, F


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)

        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255, default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name for user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.email


class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.status_text


class Motorcycle(models.Model):
    cylinder_num = (
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('6', 6),
    )
    type_category = (
        ('S', 'Scooter'),
        ('Ch', 'Chopper'),
        ('C', 'Cross'),
        ('D', 'Dirt Bike'),
        ('Sp', 'Sport'),
        ('St', 'Street'),
        ('E', 'Enduro'),
        ('Tu', 'Touring'),
        ('Tr', '3 Wheeler'),
        ('Fr', '4 Wheeler')
    )

    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    engine_size = models.FloatField(default=0)
    number_of_cylinders = models.CharField(max_length=1, choices=cylinder_num, default='')
    horse_power = models.IntegerField(default=0)
    motorcycle_category = models.CharField(max_length=2, choices=type_category, default='')
    weight = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)


class Invoice(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        # sum = 0
        # for item in self.invoiceitem_set.all():
        #     sum += item.total
        # return sum
        return self.invoiceitem_set.all().aggregate(total=Sum(F('quantity') * F('price')))

    def __str__(self):
        return f'{self.client} / {self.date}'


class InvoiceItem(models.Model):
    product = models.ForeignKey('profiles_api.Motorcycle', on_delete=models.CASCADE)
    invoice = models.ForeignKey('profiles_api.Invoice', on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)

    @property
    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.product} - {self.invoice}'
