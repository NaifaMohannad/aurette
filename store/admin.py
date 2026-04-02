from django.contrib import admin
from .models import Category, Brand, Product, Review, Cart, Order, OrderItem, ProductVariant, ContactMessage, Wishlist

# ─── PRODUCT ADMIN ────────────────────────────────────────
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'original_price', 'discount_percentage', 'category', 'brand', 'stock', 'is_featured']
    list_filter = ['category', 'brand', 'is_featured']
    search_fields = ['title', 'description']
# ─── CATEGORY ADMIN ───────────────────────────────────────
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

# ─── BRAND ADMIN ──────────────────────────────────────────
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'tagline']

# ─── REVIEW ADMIN ─────────────────────────────────────────
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created_at']

# ─── ORDER ADMIN ──────────────────────────────────────────
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total', 'status', 'created_at']
    list_filter = ['status']

# ─── CART ADMIN ───────────────────────────────────────────
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']

# ─── ORDER ITEM ADMIN ─────────────────────────────────────
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']

from .models import Category, Brand, Product, Review, Cart, Order, OrderItem, ProductVariant

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'variant_type', 'value']
    list_filter = ['variant_type', 'product']
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read']
    search_fields = ['name', 'email', 'subject']
    list_editable = ['is_read']
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']