from django.urls import path
from . import views
from context_processor import about_info
app_name = 'homeshop'

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('all/products/', views.AllProductsView.as_view(), name='allproducts'),
    path('all/product/', views.SearchResultsView.as_view(), name='searchedproducts'),
    path('popular/products/', views.AllPopularProductsView.as_view(), name='popularproducts'),
    path('wedding/clothes/', views.WeddingCollection.as_view(), name='weddingclothes'),
    path('men/clothes/', views.Men_dress_collection.as_view(), name='mendresscollection'),
    path('women/clothes/', views.women_dress_collection.as_view(), name='womendresscollection'),
    path('child/clothes/', views.Child_dress_collection.as_view(), name='childdresscollection'),
    path('300-400/price/', views.PriceFilterView.as_view(), name='pricefilter'),
    path('reccomedation/', views.RecommendedView.as_view(), name='recommended'),
    path('special/offer/', views.Specialoffer.as_view(), name='specialoffer'),
    path('details/<int:pk>/<slug:slug>', views.DetailView.as_view(), name='productdetail'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('add-to-cart/<int:pk>/', views.AddToCart.as_view(), name='add-to-cart'),
    path('checkout/', views.BuyNow, name='buynow'),
    path('remove-from-cart/<int:pk>/', views.ModelDeleteView.as_view(), name='remove-from-cart'),
    path('razorpay-checkout/', views.razorpay_checkout, name='razorpay-checkout'),
    path('payment-handler/', views.paymenthandler, name='payment-handler'),
    path('about/',about_info, name='about'),
]
