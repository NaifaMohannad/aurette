import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurette_project.settings')
django.setup()

from store.models import Category, Brand, Product

# ─── DELETE OLD DATA ──────────────────────────────────────
Product.objects.all().delete()
Category.objects.all().delete()
Brand.objects.all().delete()

# ─── CREATE CATEGORIES ────────────────────────────────────
necklaces = Category.objects.create(name='Necklaces', gender='female')
rings = Category.objects.create(name='Rings', gender='unisex')
earrings = Category.objects.create(name='Earrings', gender='female')
bangles = Category.objects.create(name='Bangles', gender='female')
bracelets = Category.objects.create(name='Bracelets', gender='unisex')
bridal = Category.objects.create(name='Bridal Sets', gender='female')
mens_rings = Category.objects.create(name="Men's Rings", gender='male')
mens_bracelets = Category.objects.create(name="Men's Bracelets", gender='male')
# ─── CREATE BRANDS ────────────────────────────────────────
diamonique = Brand.objects.create(name='Diamonique', tagline='Timeless Diamond Elegance')
roseva = Brand.objects.create(name='Roseva', tagline='Blush in Rose Gold')
goldara = Brand.objects.create(name='Goldara', tagline='Pure Gold Craftsmanship')
velvetine = Brand.objects.create(name='Velvetine', tagline='Royal Bridal Collections')
luminos = Brand.objects.create(name='Luminos', tagline='Vibrant Gemstone Jewellery')
silvique = Brand.objects.create(name='Silvique', tagline='Modern Silver Minimalism')

# ─── CREATE 30 PRODUCTS ───────────────────────────────────
products = [
    # NECKLACES (5)
    {
        'title': 'Diamond Solitaire Necklace',
        'description': 'A stunning solitaire diamond pendant on a delicate gold chain. Perfect for any occasion.',
        'price': 299.99,
        'image_url': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=600',
        'category': necklaces, 'brand': diamonique, 'stock': 15, 'is_featured': True
    },
    {
        'title': 'Gold Layered Chain Necklace',
        'description': 'Elegant multi-layered gold chain necklace that adds sophistication to any outfit.',
        'price': 189.99,
        'image_url': 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=600',
        'category': necklaces, 'brand': goldara, 'stock': 20, 'is_featured': True
    },
    {
        'title': 'Rose Gold Heart Pendant',
        'description': 'A romantic rose gold heart pendant with a sparkling diamond accent.',
        'price': 159.99,
        'image_url': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=600',
        'category': necklaces, 'brand': roseva, 'stock': 18, 'is_featured': False
    },
    {
        'title': 'Emerald Drop Necklace',
        'description': 'Luxurious emerald drop necklace set in 18k gold. A statement piece for special occasions.',
        'price': 459.99,
        'image_url': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600',
        'category': necklaces, 'brand': luminos, 'stock': 8, 'is_featured': True
    },
    {
        'title': 'Silver Minimalist Bar Necklace',
        'description': 'Clean and modern silver bar necklace. Perfect for everyday minimalist style.',
        'price': 89.99,
        'image_url': 'https://images.unsplash.com/photo-1573408301185-9519bf0a4e01?w=600',
        'category': necklaces, 'brand': silvique, 'stock': 25, 'is_featured': False
    },

    # RINGS (5)
    {
        'title': 'Diamond Engagement Ring',
        'description': 'Classic round brilliant diamond engagement ring in 18k white gold. Timeless and elegant.',
        'price': 899.99,
        'image_url': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=600',
        'category': rings, 'brand': diamonique, 'stock': 10, 'is_featured': True
    },
    {
        'title': 'Rose Gold Stackable Ring',
        'description': 'Delicate rose gold stackable ring with tiny diamond accents. Mix and match beautifully.',
        'price': 129.99,
        'image_url': 'https://images.unsplash.com/photo-1603561591411-07134e71a2a9?w=600',
        'category': rings, 'brand': roseva, 'stock': 30, 'is_featured': False
    },
    {
        'title': 'Gold Signet Ring',
        'description': 'Bold and sophisticated gold signet ring. A timeless classic reimagined for modern women.',
        'price': 199.99,
        'image_url': 'https://images.unsplash.com/photo-1602751584552-8ba73aad10e1?w=600',
        'category': rings, 'brand': goldara, 'stock': 12, 'is_featured': False
    },
    {
        'title': 'Ruby Cocktail Ring',
        'description': 'Stunning ruby cocktail ring surrounded by brilliant diamonds in a gold setting.',
        'price': 549.99,
        'image_url': 'https://images.unsplash.com/photo-1567427017947-545c5f8d16ad?w=600',
        'category': rings, 'brand': luminos, 'stock': 7, 'is_featured': True
    },
    {
        'title': 'Silver Twist Band Ring',
        'description': 'Modern twisted silver band ring. Simple yet striking minimalist design.',
        'price': 79.99,
        'image_url': 'https://images.unsplash.com/photo-1544816155-12df9643f363?w=600',
        'category': rings, 'brand': silvique, 'stock': 22, 'is_featured': False
    },

    # EARRINGS (5)
    {
        'title': 'Diamond Stud Earrings',
        'description': 'Classic diamond stud earrings in 18k white gold. A must-have for every jewellery collection.',
        'price': 349.99,
        'image_url': 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=600',
        'category': earrings, 'brand': diamonique, 'stock': 20, 'is_featured': True
    },
    {
        'title': 'Rose Gold Hoop Earrings',
        'description': 'Elegant medium-sized rose gold hoop earrings. Versatile enough for day or evening wear.',
        'price': 119.99,
        'image_url': 'https://images.unsplash.com/photo-1630019852942-f89202989a59?w=600',
        'category': earrings, 'brand': roseva, 'stock': 18, 'is_featured': False
    },
    {
        'title': 'Gold Chandelier Earrings',
        'description': 'Dramatic gold chandelier earrings with intricate filigree design. Perfect for weddings.',
        'price': 229.99,
        'image_url': 'https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?w=600',
        'category': earrings, 'brand': goldara, 'stock': 14, 'is_featured': True
    },
    {
        'title': 'Sapphire Drop Earrings',
        'description': 'Stunning deep blue sapphire drop earrings set in 18k gold. A showstopping statement.',
        'price': 399.99,
        'image_url': 'https://images.unsplash.com/photo-1596944924591-2cb982e08c7e?w=600',
        'category': earrings, 'brand': luminos, 'stock': 9, 'is_featured': False
    },
    {
        'title': 'Silver Geometric Earrings',
        'description': 'Modern geometric silver earrings with clean lines. Perfect for the contemporary woman.',
        'price': 69.99,
        'image_url': 'https://images.unsplash.com/photo-1589128777073-263566ae5e4d?w=600',
        'category': earrings, 'brand': silvique, 'stock': 25, 'is_featured': False
    },

    # BANGLES (5)
    {
        'title': 'Diamond Tennis Bangle',
        'description': 'Luxurious diamond tennis bangle in 18k white gold. The ultimate luxury accessory.',
        'price': 1299.99,
        'image_url': 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=600',
        'category': bangles, 'brand': diamonique, 'stock': 5, 'is_featured': True
    },
    {
        'title': 'Rose Gold Bangle Set',
        'description': 'Set of 3 delicate rose gold bangles. Stack them together for a stunning layered look.',
        'price': 179.99,
        'image_url': 'https://images.unsplash.com/photo-1573408301185-9519bf0a4e01?w=600',
        'category': bangles, 'brand': roseva, 'stock': 16, 'is_featured': False
    },
    {
        'title': 'Gold Kada Bangle',
        'description': 'Traditional gold kada bangle with modern engraved pattern. Timeless Indian elegance.',
        'price': 389.99,
        'image_url': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600',
        'category': bangles, 'brand': goldara, 'stock': 11, 'is_featured': True
    },
    {
        'title': 'Emerald Gold Bangle',
        'description': 'Stunning bangle with emerald gemstone accents set in 22k gold. Regal and beautiful.',
        'price': 599.99,
        'image_url': 'https://images.unsplash.com/photo-1567427017947-545c5f8d16ad?w=600',
        'category': bangles, 'brand': luminos, 'stock': 6, 'is_featured': False
    },
    {
        'title': 'Silver Cuff Bangle',
        'description': 'Bold open-ended silver cuff bangle. Minimalist design with maximum impact.',
        'price': 99.99,
        'image_url': 'https://images.unsplash.com/photo-1602751584552-8ba73aad10e1?w=600',
        'category': bangles, 'brand': silvique, 'stock': 20, 'is_featured': False
    },

    # BRACELETS (5)
    {
        'title': 'Diamond Chain Bracelet',
        'description': 'Delicate diamond chain bracelet in 18k white gold. Effortlessly elegant.',
        'price': 449.99,
        'image_url': 'https://images.unsplash.com/photo-1544816155-12df9643f363?w=600',
        'category': bracelets, 'brand': diamonique, 'stock': 12, 'is_featured': True
    },
    {
        'title': 'Rose Gold Charm Bracelet',
        'description': 'Beautiful rose gold charm bracelet with heart and star charms. Sweet and feminine.',
        'price': 149.99,
        'image_url': 'https://images.unsplash.com/photo-1603561591411-07134e71a2a9?w=600',
        'category': bracelets, 'brand': roseva, 'stock': 18, 'is_featured': False
    },
    {
        'title': 'Gold Link Bracelet',
        'description': 'Classic chunky gold link bracelet. Bold and sophisticated statement jewellery.',
        'price': 269.99,
        'image_url': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=600',
        'category': bracelets, 'brand': goldara, 'stock': 14, 'is_featured': False
    },
    {
        'title': 'Amethyst Beaded Bracelet',
        'description': 'Natural amethyst gemstone beaded bracelet with gold accents. Spiritual and stunning.',
        'price': 119.99,
        'image_url': 'https://images.unsplash.com/photo-1630019852942-f89202989a59?w=600',
        'category': bracelets, 'brand': luminos, 'stock': 20, 'is_featured': False
    },
    {
        'title': 'Silver Tennis Bracelet',
        'description': 'Classic silver tennis bracelet with cubic zirconia stones. Elegant and affordable luxury.',
        'price': 139.99,
        'image_url': 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=600',
        'category': bracelets, 'brand': silvique, 'stock': 22, 'is_featured': True
    },

    # BRIDAL SETS (5)
    {
        'title': 'Royal Diamond Bridal Set',
        'description': 'Complete bridal jewellery set including necklace, earrings, and bangles in diamond and gold.',
        'price': 2999.99,
        'image_url': 'https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?w=600',
        'category': bridal, 'brand': velvetine, 'stock': 3, 'is_featured': True
    },
    {
        'title': 'Kundan Bridal Necklace Set',
        'description': 'Traditional Kundan bridal necklace set with matching earrings. Exquisite craftsmanship.',
        'price': 1899.99,
        'image_url': 'https://images.unsplash.com/photo-1596944924591-2cb982e08c7e?w=600',
        'category': bridal, 'brand': velvetine, 'stock': 4, 'is_featured': True
    },
    {
        'title': 'Rose Gold Bridal Choker Set',
        'description': 'Modern rose gold bridal choker set. Perfect for the contemporary bride.',
        'price': 1499.99,
        'image_url': 'https://images.unsplash.com/photo-1589128777073-263566ae5e4d?w=600',
        'category': bridal, 'brand': velvetine, 'stock': 5, 'is_featured': False
    },
    {
        'title': 'Pearl Bridal Jewellery Set',
        'description': 'Elegant freshwater pearl bridal set with gold accents. Classic and timeless beauty.',
        'price': 1299.99,
        'image_url': 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=600',
        'category': bridal, 'brand': velvetine, 'stock': 6, 'is_featured': False
    },
    {
        'title': 'Emerald Bridal Grand Set',
        'description': 'Magnificent emerald and diamond grand bridal set. For the bride who wants to dazzle.',
        'price': 3499.99,
        'image_url': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600',
        'category': bridal, 'brand': velvetine, 'stock': 2, 'is_featured': True
    },
]

# ─── SAVE ALL PRODUCTS ────────────────────────────────────
for p in products:
    Product.objects.create(**p)

print(f"✅ Successfully created:")
print(f"   - 6 Categories")
print(f"   - 6 Brands")
print(f"   - {Product.objects.count()} Products")