from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from models import *
from forms import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal

# Create your views here.

def offer_page(request, template_name='offer_list.html'):
    offers = Offers.objects.all()
    context = {
        'offers':offers,
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))


def offer_create(request, template_name='offer.html'):
    success = False
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            jv = form.save(commit=False)
            jv.save()
            success = True
    else:
        form = OfferForm()
    context = {
        'form': form,
        'success': success,
        'title':'Create'
    }
    response = render_to_response(template_name, context, context_instance=RequestContext(request))
    response['AjaxContent'] = True
    return response


def offer_edit(request, id=None, template_name='offer.html'):
    
    try:
        object = Offers.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise Http404("Invalid Request")

    success = False
    if request.method == 'POST':
        form = OfferForm(request.POST, instance=object)
        if form.is_valid():
            jv = form.save(commit=False)
            jv.save()
            success = True
    else:
        form = OfferForm(instance=object)
    context = {
        'form': form,
        'success': success,
        'title':'Edit'
    }
    response = render_to_response(template_name, context, context_instance=RequestContext(request))
    response['AjaxContent'] = True
    return response


def offer_delete(request):
    if request.method == 'POST':
        sel_id = request.POST.get('sel_id', None)
        if sel_id:
            try:
                offer = Offers.objects.get(pk=sel_id)
                offer.delete()
            except ObjectDoesNotExist:
                raise Http404("Invalid Request")
    return redirect('offer_list')


def check_product_price(request, template_name='search_product.html'):
    if request.method == 'POST':
        form = CheckProductPrice(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            code  = form.cleaned_data['code']
            product_obj = Product.objects.filter(code=code)
            product_price = Decimal(0.0)
            if product_obj:
                product_price = product_obj[0].price
            offer_obj = Offers.objects.filter(code=code)
            offer = None
            for obj in offer_obj:
                if obj.start <= date <= obj.end:
                    offer = obj
                    break
            if offer and offer.type_of_discount == 'Percentage':
                product_price = product_price - (product_price*offer.discount*Decimal(0.01))

            elif offer:
                product_price = product_price - offer.discount

            product_price = round(product_price,2)
    else:
        form = CheckProductPrice()
        product_price = Decimal(0.0)
    context = {
        'form': form,
        'product_price':product_price
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))