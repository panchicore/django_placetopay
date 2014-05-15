__author__ = 'panchicore'
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
import hashlib
from django.views.decorators.csrf import csrf_exempt
import settings
import urllib


def cart(request):
    """
    Emulate a products page.
    A button to pay will redirect to the checkout process.
    """
    return render(request, "django_p2p/cart.html", {})


def checkout(request):
    """
    Ask for payer information.
    Create the form to be posted to p2p.
    """

    PRICE_TOTAL = 130000
    PRICE_TAXES = PRICE_TOTAL * 0.16
    PRICE = PRICE_TOTAL + PRICE_TAXES

    MY_P2P_KEY = settings.P2P_KEY
    CUSTOMER_SITE_ID = settings.P2P_CUSTOMER_SITE_ID
    REFERENCE_CODE = 123456789

    text = '%s|%s|%s|%s|%s' % (
        MY_P2P_KEY, CUSTOMER_SITE_ID, REFERENCE_CODE, 'COP', PRICE_TOTAL
    )
    SIGNATURE = hashlib.sha1(text).hexdigest()

    if settings.PAYMENTS_DEBUG:
        URL_POST = '<P2P DOES NOT HAVE A DEBUG URL, THEY HAVE A "DEVELOPMENT ENVIROMENT SWITCH">'
    else:
        URL_POST = 'https://www.placetopay.com/payment.php'

    # COMPLETE URL CALLBACK TO THIS PLATFORM, POST FROM P2P WILL BE RECEIVED AND ROUTED TO CALLBACK VIEW
    SITE_URL_CALLBACK = '%s%s' % (settings.SITE_URL, reverse("p2p_callback"))

    data = {
        'REFERENCE_CODE': REFERENCE_CODE,
        'URL_POST': URL_POST,
        'CUSTOMER_SITE_ID': CUSTOMER_SITE_ID,
        'SIGNATURE': SIGNATURE,
        'PRICE_TOTAL': PRICE_TOTAL,
        'PRICE_TAXES': PRICE_TAXES,
        'PRICE': PRICE,
        'SITE_URL_CALLBACK': SITE_URL_CALLBACK
    }

    return render(request, "django_p2p/checkout.html", data)


@csrf_exempt
def p2p_callback(request):
    """ Specific for PLACE TO PAY callback.

    POSTed params looks like:
    ErrorCode=00&ErrorMessage=test&TaxAmount=0&Receipt=test&Franchise=test&
    FranchiseName=test&HashString=test&Authorization=test&
    Date=test&TotalAmount=99999&Reference=test&BankName=test&
    ShopperName=test&ShopperEmail=test@test.com

    cURL it like:
    curl http://localhost:8000/checkout/callback-receiver/ -X POST --data "ErrorCode=00&ErrorMessage=test&TaxAmount=0&Receipt=test&Franchise=test&FranchiseName=test&HashString=test&Authorization=test&Date=test&TotalAmount=99999&Reference=test&BankName=test&ShopperName=test&ShopperEmail=test@test.com"

    """

    if request.method == 'POST':

        # get error vars
        error_code = request.POST.get('ErrorCode')
        error_message = request.POST.get('ErrorMessage')

        # get payment vars
        tax_amount = request.POST.get('TaxAmount')
        receipt = request.POST.get('Receipt')
        franchise = request.POST.get('Franchise')
        franchise_name = request.POST.get('FranchiseName')
        hash_string = request.POST.get('HashString')
        extra_data = request.POST.get('ExtraData', 0)
        auth = request.POST.get('Authorization')
        transaction_date = request.POST.get('Date')
        total = request.POST.get('TotalAmount')
        reference = request.POST.get('Reference')
        bank_name = request.POST.get('BankName')
        shopper_name = request.POST.get('ShopperName')
        shopper_email = request.POST.get('ShopperEmail')

        # process the payment here in your app
        # save this in DB, will be used in the next view
        pass

        # redirect page to its correspondent view
        params = {
            'reference': reference
        }

        if error_code in ['00', '09']:

            # SUCCESS!
            params['result'] = 'success'

        elif error_code.startswith('X') or error_code in ['?5', '01']:

             # FAILED
             params['result'] = 'failed'
             params['message'] = error_message

        elif error_code in ['?-']:

            # PAYMENT NEEDS TO BE VERIFIED by p2p
            params['result'] = 'waiting'

        else:

            # fallback... FAILED FOR UNKNOWN REASONS?
            params['result'] = 'failed'
            params['message'] = 'no pudo interpretar codigo de error de place to pay'

        # redirect to something like /thank-you/result=error&messagesaldo-insuficiente
        redirect_to = '{0}?{1}'.format(reverse("thankyou"), urllib.urlencode(params))

        print redirect_to

        return redirect(redirect_to)

    else:
        return HttpResponse("PlaceToPay deberia retornar POST method. " +
                            request.META.get('HTTP_REFERER', ''))


def thankyou(request):
    """
    this page will be displayed after the payment process
    """
    reference = request.GET.get("reference")
    result = request.GET.get("result")
    message = request.GET.get("message", "no hay mensaje")

    # here get reference from DB for display more information in template.
    # ojo, displaying all transactional data is required by p2p
    pass

    data = {
        'result': result,
        'message': message,
        'reference': reference
    }
    return render(request, "django_p2p/thank_you.html", data)


