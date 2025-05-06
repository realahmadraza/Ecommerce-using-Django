from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import View
from django.shortcuts import redirect
from .models import Product, ProductInstruction, CartItem, UserAddress, SearchedQuery
from django.db.models import Count, Q
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .forms import CartItemForm, DeliveryAddressForm
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Sum

class index(generic.ListView):
    model = Product
    template_name = 'homeshop/Index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Product.objects.annotate(Popular = Count('sales')).order_by('-Popular')[:8]
        queryset_men_dress = Product.objects.filter(category__Category__iexact='men').annotate(Popular = Count('sales')).order_by('-Popular')[:4]
        queryset_women_dress = Product.objects.filter(category__Category__iexact='women').annotate(Popular = Count('sales')).order_by('-Popular')[:4]
        queryset_child_dress = Product.objects.filter(category__Category__iexact='child').annotate(Popular = Count('sales')).order_by('-Popular')[:4]
        context['product'] = queryset
        context['mendress'] = queryset_men_dress
        context['womendress'] = queryset_women_dress
        context['childdress'] = queryset_child_dress
        return context

class AllProductsView(generic.ListView):
    model = Product
    template_name = 'homeshop/productlist.html'    
    context_object_name = 'products'
    paginate_by = 30

class AllPopularProductsView(generic.ListView):
    model = Product
    template_name = 'homeshop/productlist.html'    
    paginate_by = 16
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Product.objects.annotate(popular=Count('sales')).order_by('-popular')
        context['products'] = queryset
        
        return context
    
class WeddingCollection(generic.ListView):
    model = Product
    template_name = 'homeshop/productlist.html'
    paginate_by = 30
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Product.objects.filter(Q(collection__name__icontains='Wedding') | Q(collection__description__icontains='Wedding'))
        context['products'] = queryset
        return context

class Men_dress_collection(generic.ListView):
    model = Product
    template_name = 'homeshop/productlist.html'
    paginate_by = 30
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Product.objects.filter(category__Category__iexact='men')
        context['products'] = queryset
        return context

class women_dress_collection(generic.ListView):
    model = Product
    template_name = 'homeshop/productlist.html'
    paginate_by = 30
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Product.objects.filter(category__Category__iexact='women')
        context['products'] = queryset
        return context
    
class Child_dress_collection(generic.ListView):
    model = Product
    template_name = 'homeshop/productlist.html'
    paginate_by = 30
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Product.objects.filter(category__Category__iexact='child')
        context['products'] = queryset
        return context
    
class Specialoffer(generic.ListView):
    model = Product
    template_name = 'homeshop/productlist.html'
    paginate_by = 30
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Product.objects.annotate(offer=F('offer_price') / F('price') * 100).filter(offer__lte=80).order_by('offer')
        context['products'] = queryset
        return context
    
class DetailView(generic.DetailView):
    model = Product
    template_name = 'homeshop/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['details'] = product
        context['productinstruction'] = ProductInstruction.objects.filter(product=product)
        context['similarproducts'] = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:12]

        return context

    
class AddToCart(generic.CreateView):
    form_class = CartItemForm
    model = CartItem
    template_name = 'homeshop/cartform.html'
    success_url = reverse_lazy('homeshop:cart') 
    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        form.instance.product = product
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, 'Item added to cart')
        return super().form_valid(form)


class Cart(generic.ListView):
    model = CartItem
    template_name = 'homeshop/cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cartproduct'] = CartItem.objects.filter(user=self.request.user)
        context['totalprice'] = CartItem.objects.filter(user=self.request.user).aggregate(total_price=Sum(F('product__price') * F('quantity')))
        return context

class ModelDeleteView(View):
    def get(self, request, pk):
        cartitem = CartItem.objects.get(pk=pk)
        cartitem.delete()
        return redirect('homeshop:cart')

class SearchResultsView(generic.ListView):
    model = Product
    template_name = 'homeshop/productlist.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            # Save the search query to the database
            SearchedQuery.objects.create(search_query=query)  

            # Perform the search using Q objects for multiple fields
            search_results = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(category__Category__icontains=query) | Q(collection__name__icontains=query)).distinct()
            return search_results
        return Product.objects.none()  # Return an empty queryset if no query is provided

class RecommendedView(generic.ListView):
    model = Product
    template_name = 'homeshop/productlist.html'
    context_object_name = 'products'
    

    def get_context_data(self, **kwargs):
        user = self.request.user
        

        if user.is_authenticated:
            user_queries = SearchedQuery.objects.filter(user=user).values_list('search_query', flat=True).distinct()

            q_obj = Q()
            for query in user_queries:
                q_obj |= Q(name__icontains=query)
                q_obj |= Q(description__icontains=query)
                q_obj |= Q(category__Category__icontains=query)
                q_obj |= Q(collection__name__icontains=query)

            if q_obj:
                recommended_products = Product.objects.filter(q_obj).distinct()[:4]
            return recommended_products[:4]
        if not recommended_products.exists():

            # If the user is not authenticated, return an empty queryset or handle as needed
            recommended1_products = Product.objects.all()[:4]
        return recommended1_products


class PriceFilterView(generic.ListView):
    model = Product
    template_name = 'homeshop/productlist.html'
    context_object_name = 'products'
    paginate_by = 30
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Product.objects.filter(price__gte=300, price__lte=400).distinct()
        context['products'] = queryset
        return context

# Razorpay payment view

def BuyNow(request):
    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Delivery Address added successfully')
            return redirect('homeshop:buynow')
    else:
        form = DeliveryAddressForm()

    cartitem = CartItem.objects.filter(user=request.user)
    if not cartitem.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('homeshop:cart')
    
    useraddress = UserAddress.objects.filter(user=request.user).first()
    

    context = {'cartproduct': cartitem, 'useraddress': useraddress, 'form': form}
    return render(request, 'homeshop/payment.html', context)

# Razorpay client settigs "Initialize client once"
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def razorpay_checkout(request):
    """
    Called when the user clicks 'Continue' under UPI
    Create a razorpay order and re-renders the same template
    with the checkout parameters in context.
    """

    cart = CartItem.objects.filter(user=request.user)
    total_paise = sum(item.product.price*item.quantity for item in cart) * 100
    total = int(total_paise)  # Convert to integer
    # Creates Order
    razorpay_order = razorpay_client.order.create({
        'amount': total,  # amount in paise
        'currency': 'INR',
        'payment_capture': '1',  # auto capture
    })

    # Context to pass into template
    context = {
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'razorpay_order_id': razorpay_order['id'],
        'amount': total//100,  # amount in rupees to show on template 

        #Keeping existed context so accordion still shows
        'cartproduct': cart,
        'useraddress': UserAddress.objects.filter(user=request.user).first(),
        'form': DeliveryAddressForm(),
    }
    return render(request, 'homeshop/payment.html', context)

@csrf_exempt
def paymenthandler(request):
    if request.method == 'POST':

        # verify the payment signature
        params = {
        'razorpay_signature': request.POST['razorpay_signature'],
        'razorpay_order_id': request.POST['razorpay_order_id'],
        'razorpay_payment_id': request.POST['razorpay_payment_id'],
        }
        # verify the payment signature using Razorpay's API
        try:
            razorpay_client.utility.verify_payment_signature(params)
            messages.success(request, 'Payment successful!')
            return redirect('homeshop:cart')
        except Exception as e:
            e.messages.error(request, 'Payment verification failed!')
            return redirect('homeshop:cart')
        
