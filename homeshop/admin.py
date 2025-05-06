from django.contrib import admin
from .models import Collection, Product, Category, Order, Sales, ProductInstruction, Cart, CartItem, UserAddress, About, Footerinfo, SearchedQuery

admin.site.site_header = 'Scottie Hampton'
admin.site.index_title = 'Welcome to "Scottie Hampton Dashboard"' 
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'quantity']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['quantity']
    search_fields = ['name']
    
@admin.register(ProductInstruction)
class ProductInstructionAdmin(admin.ModelAdmin):
    list_display = ['id', 'careinstructions', 'Fittype', 'color', 'cloth', 'sleeves', 'design', 'wash']
    search_fields = ['id']
    list_editable = ['careinstructions', 'Fittype', 'color', 'cloth', 'sleeves', 'design', 'wash']
    list_per_page = 30

class ProductInstructionInline(admin.StackedInline):
    model = ProductInstruction
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'quantity', 'price', 'collection', 'collection__quantity']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['quantity', 'price']
    list_filter = ['collection', 'quantity']
    search_fields = ['name', 'description']
    autocomplete_fields = ['collection', 'category']
    list_per_page = 30
    inlines = [ProductInstructionInline]

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    exclude = ['description', 'collection', 'slug']
    readonly_fields = ['name', 'quantity', 'price']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['Category', 'Quantity']
    search_fields = ['Category']
    list_filter = ['Category', 'Quantity']
    list_per_page = 30
    inlines = [ProductInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'created_at']
    autocomplete_fields = ['product']
    list_per_page = 30
    list_filter = ['created_at']

@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ['product__name', 'sales', 'product__price']
    autocomplete_fields = ['product']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user','id', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['id']
    list_per_page = 30

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart__user', 'cart__id', 'product__name', 'product__price', 'quantity', ]
    autocomplete_fields = [ 'cart', 'product']

@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'state', 'city', 'pin']
    list_per_page = 30

@admin.register(SearchedQuery)
class Searched_Queries(admin.ModelAdmin):
    list_display = ['user', 'search_query', 'searched_at']
    list_per_page = 30

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['id', 'centre1city', 'centre2city', 'centre3city']
    
@admin.register(Footerinfo)
class FooterinfoAdmin(admin.ModelAdmin):
    list_display = ['short_About', 'phone', 'telephone', 'email', 'City']