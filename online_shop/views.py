from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from .models import *
from django.views.generic import ListView, CreateView, DetailView, TemplateView
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json


class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
    context_object_name = 'book_list'


@method_decorator(login_required, name='dispatch')
class BookCreateView(CreateView):
    model = Book
    fields = '__all__'
    template_name = "add_book.html"
    success_url = reverse_lazy("logout")


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")


class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        return context


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request, id):

    request_data = json.loads(request.body)
    chosen_book = get_object_or_404(Book, pk=id)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    domain_url = 'http://localhost:8000/'
    checkout_session = stripe.checkout.Session.create(
        customer_email=request_data['email'],
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': chosen_book.name,
                    },
                    'unit_amount': int(chosen_book.price * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=domain_url + 'failed/',
    )

    order = OrderDetail()
    order.customer_email = request_data['email']
    order.book = chosen_book
    print(vars(checkout_session))
    print(checkout_session)
    order.amount = int(chosen_book.price * 100)
    order.save()

    chosen_book.quantity = chosen_book.quantity - 1
    chosen_book.save()

    # return JsonResponse({'data': checkout_session})
    return JsonResponse({'sessionId': checkout_session.id})


class PaymentSuccessView(TemplateView):
    template_name = "success.html"


class PaymentFailedView(TemplateView):
    template_name = "failure.html"

class OrderHistoryListView(ListView):
    model = OrderDetail
    template_name = "order_history.html"
