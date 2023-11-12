from django import forms

from .models import (
    Address,
    Business,
    Category,
    DriverLocation,
    Order,
    OrderItem,
    Payment,
    Product,
    ProductVariation,
    Promotion,
    Review,
    UserProfile,
)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = "__all__"


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = "__all__"


class ProductVariationForm(forms.ModelForm):
    class Meta:
        model = ProductVariation
        fields = "__all__"


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = "__all__"


class DriverLocationForm(forms.ModelForm):
    class Meta:
        model = DriverLocation
        fields = "__all__"


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"
