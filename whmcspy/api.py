import requests

from whmcspy import exceptions


def _is_inactive(obj, active):
    """
    Check if the object is considered inactive.

    This method is useful in filtering objects based on their state.

    Args:
        obj (dict): The WHMCS object to check.
        active (bool): The active state to check. If set to True the
            status should be Active, if set to False the status should not be
            Active. If set to None no check occurs and all is not considered
            inactive.

    Returns:
        True if the object is considered active.

    """
    return (
        active is True and obj['status'] != 'Active'
        or active is False and obj['status'] == 'Active')


class WHMCS:
    """
    WHMCS interface.

    """
    def __init__(
            self,
            url,
            identifier,
            secret):
        """
        Create a new instance.

        Args:
            url (str): The URL to the WHMCS api.
            identifier (str): The identifier of the WHMCS credentials.
            secret (str): The secret of the WHMCS credentials.

        """
        self.url = url
        self.identifier = identifier
        self.secret = secret

    def call(
            self,
            action,
            **params):
        """
        Call the WHMCS api.

        This is an abstract way to call the WHMCS API. Basically only the
        action and additional params are required to make a call.

        Args:
            action (str): The action to perform.
            **params: Additional params.

        Returns:
            dict: The result of the call.

        Raises:
            MissingPermission: When access is denied due to a missing
                permission.
            Error: Whenever the call fails.

        """
        payload = {
            'identifier': self.identifier,
            'secret': self.secret,
            'action': action,
            'responsetype': 'json',
        }
        payload.update(params)
        response = requests.post(
            self.url,
            verify=False,
            data=payload)
        response_ = response.json()
        if response_['result'] == 'error':
            if response.status_code == 403:
                raise exceptions.MissingPermission(response_['message'])
            raise exceptions.Error(response_['message'])
        return response_

    def paginated_call(
            self,
            action,
            limitstart=0,
            **params):
        """
        Perform a WHMCS API call, but paginated.

        Instead of returning just a single result a result is yielded for
        every iteration until an empty result returns from WHMCS.
        See :func:`call` for common params.

        Keyword Args:
            limitstart (int): The offset from which to start. Initially this
                is 0.

        Yields:
            An API response.

        """
        while True:
            params.update(
                limitstart=limitstart,
            )
            response = self.call(
                action,
                **params)
            if not response['numreturned']:
                break
            limitstart += response['numreturned']
            yield response

    def get_orders(
            self,
            **params):
        """
        Get orders.

        Args:
            **params: Additional params.

        Yields:
            The matching orders.

        Hint:
            For additional params, see the official API docs:
            https://developers.whmcs.com/api-reference/getorders/

        """
        for response in self.paginated_call(
                'GetOrders',
                **params):
            for order in response['orders']['order']:
                yield order

    def get_tld_pricing(self):
        """
        Get the TLD pricing.

        Returns:
            dict: The TLD pricing info.

        """
        return self.call('GetTLDPricing')

    def accept_order(
            self,
            order_id,
            **params):
        """
        Accept an order.

        Args:
            order_id (int): The id of the order to accept.
            **params: Additional params.

        Hint:
            For additional params, see the official API docs:
            https://developers.whmcs.com/api-reference/acceptorder/

        """
        params.update(
            orderid=order_id,
        )
        response = self.call(
            'AcceptOrder',
            **params)
        return response

    def add_order(
            self,
            clientid,
            domains=None,
            paymentmethod='banktransfer',
            products=None,
            **params):
        """
        Add an order.

        Args:
            clientid (int): The id of the client whom the order is for.
            **params: Additional params.

        Keyword Args:
            domains (list): A list of domains to include in the order.
            paymentmethod (str): The payment method for the order.
            products: A list of products (dict) with an id and a domain name
                (`pid`, `domain`).

        Returns:
            The response of the successfully created order.

        Hint:
            For additional params, see the official API docs:
            https://developers.whmcs.com/api-reference/addorder/

        """
        params.update(
            clientid=clientid,
            paymentmethod=paymentmethod,
        )
        if domains:
            for i, domain in enumerate(domains):
                params[f'domain[{i}]'] = domain
                params[f'domaintype[{i}]'] = 'register'
                params[f'domainpriceoverride[{i}]'] = 0
                params[f'domainrenewoverride[{i}]'] = 0
        if products:
            for i, product in enumerate(products):
                params[f'pid[{i}]'] = product['id']
                params[f'domain[{i}]'] = product['domain']
        response = self.call(
            'AddOrder',
            **params)
        return response

    def add_transaction(
            self,
            paymentmethod,
            **params):
        """
        Add a transaction.

        Args:
            paymentmethod (str): The payment method used to perform the
            transaction.
            **params: Additional params.

        Hint:
            For additional params, see the official API docs:
            https://developers.whmcs.com/api-reference/addtransaction/

        """
        params.update(
            paymentmethod=paymentmethod,
        )
        self.call(
            'AddTransaction',
            **params)

    def cancel_order(
            self,
            orderid,
            **params):
        """
        Cancel a pending order.

        Args:
            orderid (int): The id of the order.
            **params: Additional params.

        Hint:
            For additional params, see the official API docs:
            https://developers.whmcs.com/api-reference/cancelorder/

        """
        params.update(
            orderid=orderid,
        )
        self.call(
            'CancelOrder',
            **params)

    def delete_order(
            self,
            orderid,
            **params):
        """
        Delete a cancelled or fraud order.

        Args:
            orderid (int): The id of the order.

        """
        params.update(
            orderid=orderid,
        )
        self.call(
            'DeleteOrder',
            **params)

    def get_clients_domains(
            self,
            active=None,
            **params):
        """
        Get domains (registrations).

        Args:
            **params: Additional params.

        Keyword Args:
            active (bool): Filter on active or inactive domains.

        Yields:
            The domains.

        Hint:
            For additional params, see the official API docs:
            https://developers.whmcs.com/api-reference/getclientsdomains/

        """
        for response in self.paginated_call(
                'GetClientsDomains',
                **params):
            for domain in response['domains']['domain']:
                if _is_inactive(domain, active):
                    continue
                yield domain

    def get_clients_products(
            self,
            active=None,
            productid=None,
            **params):
        """
        Get client products.


        Args:
            **params: Additional params.

        Keyword Args:
            active (bool): Filter on active or inactive domains.
            productid (int): Only get products with this product id.

        Yields:
            The products.

        Hint:
            For additional params, see the official API docs:
            https://developers.whmcs.com/api-reference/getclientsproducts/

        """
        if productid:
            params['pid'] = productid
        for response in self.paginated_call(
                'GetClientsProducts',
                **params):
            for product in response['products']['product']:
                if _is_inactive(product, active):
                    continue
                yield product

    def get_invoice(
            self,
            invoiceid):
        """
        Get an invoice.

        Args:
            invoiceid (int): The id of the invoice.

        Returns:
            The invoice

        """
        result = self.call(
            'GetInvoice',
            invoiceid=invoiceid)
        return result

    def get_tickets(
            self,
            **params):
        """
        Get support tickets.

        Args:
            **params: Additional params.

        Yields:
            The tickets.

        Hint:
            For additional params, see the official API docs:
            https://developers.whmcs.com/api-reference/gettickets/

        """
        for response in self.paginated_call(
                'GetTickets',
                **params):
            for ticket in response['tickets']['ticket']:
                yield ticket

    def get_transactions(
            self,
            **params):
        """
        Get (find) transactions.

        Args:
            **params: Additional params.

        Returns:
            A list of matching transactions.

        Hint:
            For additional params, see the official API docs:
            https://developers.whmcs.com/api-reference/gettransactions/

        """
        response = self.call(
            'GetTransactions',
            **params)
        return response.get('transactions', {}).get('transaction', [])

    def open_ticket(
            self,
            deptid,
            subject,
            message,
            **params):
        """
        Open a support ticket

        Args:
            deptid (int): The id of the department to open the ticket for.
            subject (str): The subject of the ticket.
            message (str): The initial message of the ticket.
            **params: Additional params.

        Hint:
            For additional params, see the official API docs:
            https://developers.whmcs.com/api-reference/openticket/

        Note:
            Markdown doesn't seem to work when opening a ticket by using
            the API. Maybe it's fixed in later versions of WHMCS. Consider it
            unstable.

        """
        params.update(
            deptid=deptid,
            subject=subject,
            message=message,
        )
        self.call(
            'OpenTicket',
            **params)

    def pending_order(
            self,
            orderid,
            **params):
        """
        Set an order and it's items to Pending.

        Args:
            orderid (int): The id of the order.

        """
        params.update(
            orderid=orderid,
        )
        self.call(
            'PendingOrder',
            **params)

    def send_email(
            self,
            **params):
        """
        Send a client email notification.

        Args:
            **params: Additional params.

        Hint:
            For additional params, see the official API docs:
            https://developers.whmcs.com/api-reference/sendemail/

        """
        result = self.call(
            'SendEmail',
            **params)

    def update_client_domain(
            self,
            domain,
            **params):
        """
        Update a client's domain registration.

        Args:
            domain (dict): The domain to update.
            **params: Additional params.

        Hint:
            For additional params, see the official API docs:
            https://developers.whmcs.com/api-reference/updateclientdomain/

        """
        params.update(
            domainid=domain['id'],
            dnsmanagement=domain['dnsmanagement'],
            emailforwarding=domain['emailforwarding'],
            idprotection=domain['idprotection'],
            donotrenew=domain['donotrenew'],
            type=domain['regtype'],
            regdate=domain['regdate'],
            nextduedate=domain['nextduedate'],
            expirydate=domain['expirydate'],
            domain=domain['domainname'],
            firstpaymentamount=domain['firstpaymentamount'],
            recurringamount=domain['recurringamount'],
            registrar=domain['registrar'],
            regperiod=domain['regperiod'],
            paymentmethod=domain['paymentmethodname'],
            subscriptionid=domain['subscriptionid'],
            status=domain['status'],
            notes=domain['notes'],
            promoid=domain['promoid'],
        )
        response = self.call(
            'UpdateClientDomain',
            **params)
        return response

    def update_client_product(
            self,
            productid,
            **params):
        """
        Update a client's product.

        Args:
            productid (int): The id of the client product.
            **params: Additional params.

        Hint:
            For additional params, see the official API docs:
            https://developers.whmcs.com/api-reference/updateclientproduct/

        """
        params.update(
            serviceid=productid,
        )
        nextduedate = params.get('nextduedate')
        if nextduedate:
            nextduedate = nextduedate.strftime('%Y-%m-%d')
        response = self.call(
            'updateClientProduct',
            **params)
        return response
