from datetime import datetime
from typing import List, Optional

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


class Address(Model):
    street: str = CharField(max_length=255)
    city: str = CharField(max_length=100)
    state: str = CharField(max_length=100)
    postal_code: str = CharField(max_length=20)
    country: str = CharField(max_length=100)

    def __str__(self):
        return (
            f"{self.street}, {self.city}, {self.state} "
            f"{self.postal_code}, {self.country}"
        )


class UserProfile(Model):
    user: User = OneToOneField(User, on_delete=CASCADE)
    avatar: ImageField = ImageField(upload_to=f"users/{user.email}/selfie/")
    phone: str = CharField(max_length=20, blank=True)
    address: Optional[Address] = ForeignKey(
        Address,
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.get_full_name()


class Category(Model):
    name: str = CharField(max_length=100)
    description: str = TextField(blank=True)

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
    name: str = CharField(max_length=255)
    description: str = TextField()
    address: Optional[Address] = ForeignKey(
        Address,
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    contact_number: str = CharField(max_length=20)
    owner: User = ForeignKey(User, on_delete=CASCADE)
    business_type: str = CharField(
        max_length=20,
        choices=BUSINESS_TYPE_CHOICES,
    )
    logo: ImageField = ImageField(upload_to="business_logos/")
    created_at: datetime = DateTimeField(auto_now_add=True)
    updated_at: datetime = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(Model):
    name: str = CharField(max_length=255)
    description: str = TextField()
    price: float = DecimalField(max_digits=10, decimal_places=2)
    business: Business = ForeignKey(Business, on_delete=CASCADE)
    image: ImageField = ImageField(upload_to="product_images/")
    categories: List[Category] = ManyToManyField(Category, related_name="products")
    created_at: datetime = DateTimeField(auto_now_add=True)
    updated_at: datetime = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Promotion(Model):
    name: str = CharField(max_length=100)
    description: str = TextField()
    business: Business = ForeignKey(Business, on_delete=CASCADE)
    start_date: datetime = DateTimeField()
    end_date: datetime = DateTimeField()
    discount: float = DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class ProductVariation(Model):
    product: Product = ForeignKey(Product, on_delete=CASCADE)
    name: str = CharField(max_length=100)
    price: float = DecimalField(max_digits=10, decimal_places=2)
    is_available: bool = BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(Model):
    STATUS_CHOICES = (
        ("PREPARING", "Preparing"),
        ("READY", "Ready"),
        ("ONTHEWAY", "On the way"),
        ("DELIVERED", "Delivered"),
    )

    id: PositiveIntegerField = PositiveIntegerField(primary_key=True)
    customer: User = ForeignKey(User, on_delete=CASCADE)
    business: Business = ForeignKey(Business, on_delete=CASCADE)
    driver: Optional[User] = ForeignKey(User, on_delete=SET_NULL, blank=True, null=True)
    address: Optional[Address] = ForeignKey(
        Address, on_delete=SET_NULL, null=True, blank=True
    )
    total_price: float = DecimalField(max_digits=10, decimal_places=2)
    status: str = CharField(max_length=20, choices=STATUS_CHOICES)
    created_at: datetime = DateTimeField(auto_now_add=True)
    updated_at: datetime = DateTimeField(auto_now=True)
    picked_at: Optional[datetime] = DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(Model):
    order: Order = ForeignKey(Order, on_delete=CASCADE)
    product: Product = ForeignKey(Product, on_delete=CASCADE)
    quantity: PositiveIntegerField = PositiveIntegerField()
    subtotal: float = DecimalField(max_digits=10, decimal_places=2)
    created_at: datetime = DateTimeField(auto_now_add=True)
    updated_at: datetime = DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order Item for Order #{self.order}"


class DriverLocation(Model):
    driver: User = ForeignKey(User, on_delete=CASCADE)
    latitude: float = DecimalField(max_digits=9, decimal_places=6)
    longitude: float = DecimalField(max_digits=9, decimal_places=6)
    timestamp: datetime = DateTimeField(auto_now=True)


class Payment(Model):
    PAYMENT_METHOD_CHOICES = (
        ("credit_card", "Credit Card"),
        ("debit_card", "Debit Card"),
        ("paypal", "PayPal"),
        ("apple_pay", "Apple Pay"),
        ("google_pay", "Google Pay"),
    )

    user: User = ForeignKey(User, on_delete=CASCADE)
    payment_method: str = CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    billing_info: str = TextField()
    created_at: datetime = DateTimeField(auto_now_add=True)
    updated_at: datetime = DateTimeField(auto_now=True)


class Review(Model):
    reviewer: User = ForeignKey(User, on_delete=CASCADE)
    business: Business = ForeignKey(Business, on_delete=CASCADE)
    rating: PositiveIntegerField = PositiveIntegerField()
    comments: str = TextField()
    created_at: datetime = DateTimeField(auto_now_add=True)
    updated_at: datetime = DateTimeField(auto_now=True)
