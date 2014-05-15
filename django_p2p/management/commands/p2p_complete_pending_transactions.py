from django.core.management.base import BaseCommand
from suds.client import Client
from datetime import datetime
import hashlib



class Command(BaseCommand):
    help = "Complete payments that results as PENDING by consuming a " \
           "webservice"

    def query_transaction_call(self, reference, currency, total_amount):
        """ Consume p2p webservice in order to update PENDING payments.
        """
        WSDL = 'https://www.placetopay.com/soap/placetopay/?wsdl'
        LOGIN = 'LOGIN HERE'
        SEED = datetime.today().isoformat()
        TRANKEY = hashlib.sha1(SEED + 'TRANKEY HERE').hexdigest()

        c = Client(WSDL)

        auth = c.factory.create('Authentication')
        auth.login = LOGIN
        auth.tranKey = TRANKEY
        auth.seed = SEED

        query_request = c.factory.create('QueryRequest')
        query_request.reference = reference
        query_request.currency = currency
        query_request.totalAmount = total_amount
        response = c.service.queryTransaction(auth, query_request)
        return response

    def handle(self, *args, **options):

        # ask for those 2 references
        pending_payments = [123456678, 678345234]

        for pending_payment in pending_payments:

            print 'looking up transaction #', pending_payment

            reference = pending_payment
            currency = 'COP'
            total_amount = 136000
            response = self.query_transaction_call(reference,
                                                   currency, total_amount)

            # for debug porpouses lets save the response in logger
            print response
            print '*' * 100

            if len(response.item):
                transaction = response.item[0]
                transaction_state = transaction.transactionState

                if transaction_state == 'OK':
                    # 1. successful transaction
                    pass
                elif transaction_state in ['NOT_AUTHORIZED', 'FAILED']:
                    # 2. failed transaction
                    pass
                elif transaction_state == 'PENDING':
                    # 3. transaction stills in pending process
                    # dont do nothing, at least that we want to track
                    # how many time is p2p taking to approve transactions.
                    pass

        print 'OK.'
