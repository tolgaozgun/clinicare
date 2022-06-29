from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# This function gets two calendar expressions: F
# First expression is an existing expression.
# Second expression is the expression to be excluded from the existing one.
# In the end, it returns a new expression, if there are multiple expressions, they are split by '/' character
#
# Existing expression: + for start, - for end
# Exclude expression: x for start, z for end
#
# There are four cases:
# 1- x + - z >> No expression to return
# 2- + x - z >> Start is +, end is x
# 3- x + z - >> Start is z, end is -
# 4- + x z - >> Two expressions: first's start is +, end is x. Second's start is z, end is -


def fix_collision(existing_expression, exclude_expression):
    existing_split = existing_expression.split('-')
    existing_start = existing_split[0]
    existing_end = existing_split[1]

    exclude_split = exclude_expression.split('-')
    exclude_start = exclude_split[0]
    exclude_end = exclude_split[1]

    expression = ""

    if existing_start > exclude_start:
        if existing_end > exclude_end:
            start = exclude_end
            end = existing_end
            expression += start + "-" + end + "/"
        # in the else case, nothing to do
    else:
        if existing_end > exclude_end:
            first_start = existing_start
            first_end = exclude_start

            second_start = exclude_end
            second_end = existing_end

            expression += first_start + "-" + first_end + "/"
            expression += second_start + "-" + second_end + "/"
        else:
            start = existing_start
            end = exclude_end
            expression += start + "-" + end + "/"

    return expression


def unite_collision(existing_expression, new_expression):
    existing_split = existing_expression.split('-')
    existing_start = existing_split[0]
    existing_end = existing_split[1]

    new_split = new_expression.split('-')
    new_start = new_split[0]
    new_end = new_split[1]

    start = min(new_start, existing_start)
    end = max(new_end, existing_end)

    return start + "-" + end + "/"


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=False, blank=False, unique=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    role = models.SmallIntegerField(default=1)
    department = models.TextField(null=True, blank=True)  # For doctors
    status = models.fields.SmallIntegerField(default=1)
    password = models.CharField(max_length=200)
    is2FAEnabled = models.BooleanField(default=False)
    lastLogin = models.DateTimeField(default=None, null=True)
    photo = models.ImageField(upload_to="profile", null=True, default="profile/avatar.png")
    lastUpdated = models.DateTimeField(auto_now=True, editable=False)
    dateCreated = models.DateTimeField(auto_now_add=True, editable=False)
    availability = models.CharField(max_length=300)
    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def __str__(self):
        if self is None:
            return "None"
        else:
            return self.first_name + " " + self.last_name

    def get_availability(self):
        regex_str = self.availability.split('/')
        days = "ABCDEFG"
        week = ['', '', '', '', '', '', '']
        for expression in regex_str:
            if expression[0] == '!':
                start_str = expression[1]
                end_str = expression[2]
                start = days.find(start_str)
                end = days.find(end_str)
                times = expression[3:]

                for i in range(start, end):
                    try:
                        week[i] = fix_collision(week[i], times)
                    except IndexError:
                        pass
            else:
                start_str = expression[0]
                end_str = expression[1]
                start = days.find(start_str)
                end = days.find(end_str)
                times = expression[2:]
                for i in range(start, end):
                    try:
                        week[i] = unite_collision(week[i], times)
                    except IndexError:
                        pass
        return week
