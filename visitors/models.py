from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


phone_validator = RegexValidator(
    regex=r'^\+?\d{7,15}$',
    message="Enter a valid phone number (7-15 digits, optional leading +)."
)


class Visitor(models.Model):
    """A person who visits the premises. Stores reusable identity info
    so repeat visitors don't need to be re-entered each time."""

    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=16, validators=[phone_validator])
    email = models.EmailField(blank=True)
    company_name = models.CharField(max_length=150, blank=True)
    id_proof_type = models.CharField(
        max_length=20,
        choices=[
            ('AADHAR', 'Aadhar Card'),
            ('PAN', 'PAN Card'),
            ('DL', 'Driving License'),
            ('PASSPORT', 'Passport'),
            ('OTHER', 'Other'),
        ],
        blank=True,
    )
    id_proof_number = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to='visitor_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"


class Host(models.Model):
    """The employee/staff member a visitor has come to meet."""

    name = models.CharField(max_length=150)
    department = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=16, blank=True, validators=[phone_validator])
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Visit(models.Model):
    """A single visit record - links a Visitor to a Host with
    check-in/check-out timestamps and purpose."""

    PURPOSE_CHOICES = [
        ('MEETING', 'Meeting'),
        ('INTERVIEW', 'Interview'),
        ('DELIVERY', 'Delivery'),
        ('VENDOR', 'Vendor Visit'),
        ('PERSONAL', 'Personal'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('CHECKED_IN', 'Checked In'),
        ('CHECKED_OUT', 'Checked Out'),
    ]

    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='visits')
    host = models.ForeignKey(Host, on_delete=models.SET_NULL, null=True, related_name='visits')
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default='MEETING')
    purpose_notes = models.CharField(max_length=255, blank=True)
    check_in_time = models.DateTimeField(default=timezone.now)
    check_out_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='CHECKED_IN')
    badge_number = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['-check_in_time']

    def __str__(self):
        return f"{self.visitor.full_name} -> {self.host or 'N/A'} on {self.check_in_time:%Y-%m-%d %H:%M}"

    def duration(self):
        if self.check_out_time:
            return self.check_out_time - self.check_in_time
        return None
