from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# ─── CATEGORY TABLE ───────────────────────────────────────
class Category(models.Model):
    GENDER_CHOICES = [
        ('female', 'Female'),
        ('male', 'Male'),
        ('unisex', 'Unisex'),
    ]
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='female')
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

# ─── BRAND TABLE ──────────────────────────────────────────
class Brand(models.Model):
    name = models.CharField(max_length=100)      # e.g. Diamonique
    tagline = models.CharField(max_length=200)   # e.g. "Timeless Diamond Elegance"
    logo_url = models.URLField(blank=True)        # optional logo image

    def __str__(self):
        return self.name


# ─── PRODUCT TABLE ────────────────────────────────────────

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percentage = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    stock = models.IntegerField(default=10)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ─── REVIEW TABLE ─────────────────────────────────────────
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    image1 = models.ImageField(upload_to='reviews/', blank=True, null=True)
    image2 = models.ImageField(upload_to='reviews/', blank=True, null=True)
    image3 = models.ImageField(upload_to='reviews/', blank=True, null=True)
    video = models.FileField(upload_to='reviews/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"
# ─── CART TABLE ───────────────────────────────────────────
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"

    def get_total(self):
        return self.product.price * self.quantity  # calculates total for this item


# ─── ORDER TABLE ──────────────────────────────────────────
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


# ─── ORDER ITEM TABLE ─────────────────────────────────────
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"


# ─── PRODUCT VARIANT TABLE ────────────────────────────────
class ProductVariant(models.Model):
    VARIANT_TYPE_CHOICES = [
        ('material', 'Material'),
        ('size', 'Size'),
        ('color', 'Color'),
    ]
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )
    variant_type = models.CharField(max_length=20, choices=VARIANT_TYPE_CHOICES)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.title} - {self.variant_type}: {self.value}"
    
# ─── CONTACT MESSAGE TABLE ────────────────────────────────
class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']

# ─── WISHLIST TABLE ───────────────────────────────────────
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"