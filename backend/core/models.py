from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    ImageField,
    ManyToManyField,
    Model,
    OneToOneField,
    PositiveIntegerField,
    TextField,
)


def user_directory(instance):
    return "users/{0}/selfie.png".format(instance.user.id)


def business_directory(instance):
    return "businesses/{0}/logo.png".format(instance.business.id)


def product_directory(instance):
    return "businesses/{0}/products/{1}/image.png".format(
        instance.business.id, instance.id
    )


class Address(Model):
    street = CharField(max_length=255)
    city = CharField(max_length=100)
    state = CharField(max_length=100)
    postal_code = CharField(max_length=20)
    country = CharField(max_length=100)

    def __str__(self):
        return (
            f"{self.street}, {self.city}, {self.state} "
            f"{self.postal_code}, {self.country}"
        )


class UserProfile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    selfie = ImageField(upload_to=user_directory)
    phone = CharField(max_length=20, blank=True)
    address = ForeignKey(
        Address,
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.get_full_name()


class Category(Model):
    name = CharField(max_length=100)
    description = TextField(blank=True)

    def __str__(self):
        return self.name


class Business(Model):
    BUSINESS_TYPE_CHOICES = (
        ("restaurant", "Restaurant"),
        ("grocery", "Grocery"),
        ("pharmacy", "Pharmacy"),
        ("clothing", "Clothing"),
        ("other", "Other"),
    )
    name = CharField(max_length=255)
    description = TextField()
    address = ForeignKey(
        Address,
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    contact_number = CharField(max_length=20)
    owner = ForeignKey(User, on_delete=CASCADE)
    business_type = CharField(
        max_length=20,
        choices=BUSINESS_TYPE_CHOICES,
    )
    logo = ImageField(upload_to=business_directory)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(max_length=255)
    description = TextField()
    price = DecimalField(max_digits=10, decimal_places=2)
    business = ForeignKey(Business, on_delete=CASCADE)
    image = ImageField(upload_to=product_directory)
    categories = ManyToManyField(Category, related_name="products")
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Promotion(Model):
    name = CharField(max_length=100)
    description = TextField()
    business = ForeignKey(Business, on_delete=CASCADE)
    start_date = DateTimeField()
    end_date = DateTimeField()
    discount = DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class ProductVariation(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    name = CharField(max_length=100)
    price = DecimalField(max_digits=10, decimal_places=2)
    is_available = BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(Model):
    STATUS_CHOICES = (
        ("PREPARING", "Preparing"),
        ("READY", "Ready"),
        ("ONTHEWAY", "On the way"),
        ("DELIVERED", "Delivered"),
    )

    business = ForeignKey(Business, on_delete=CASCADE)
    customer = ForeignKey(User, on_delete=CASCADE, related_name="customer_orders")
    driver = ForeignKey(
        User, on_delete=SET_NULL, blank=True, null=True, related_name="driver_orders"
    )
    address = ForeignKey(Address, on_delete=SET_NULL, null=True, blank=True)
    price = DecimalField(max_digits=10, decimal_places=2)
    status = CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    picked_at = DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(Model):
    order = ForeignKey(Order, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)
    quantity = PositiveIntegerField()
    subtotal = DecimalField(max_digits=10, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order Item for Order #{self.order}"


class DriverLocation(Model):
    driver = ForeignKey(User, on_delete=CASCADE)
    latitude = DecimalField(max_digits=9, decimal_places=6)
    longitude = DecimalField(max_digits=9, decimal_places=6)
    timestamp = DateTimeField(auto_now=True)


class Payment(Model):
    PAYMENT_METHOD_CHOICES = (
        ("credit_card", "Credit Card"),
        ("debit_card", "Debit Card"),
        ("paypal", "PayPal"),
        ("apple_pay", "Apple Pay"),
        ("google_pay", "Google Pay"),
    )

    user = ForeignKey(User, on_delete=CASCADE)
    payment_method: str = CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    billing_info: str = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class Review(Model):
    reviewer = ForeignKey(User, on_delete=CASCADE)
    business = ForeignKey(Business, on_delete=CASCADE)
    rating = PositiveIntegerField()
    comments: str = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
