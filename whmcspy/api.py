import requests

from whmcspy import exceptions


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

        Args:
            action (str): The action to perform.

        Keyword Args:
            params: The parameters to include in the call.

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
            **kwargs: Arbitrary parameters.

        """
        params.update(
            orderid= order_id,
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
            **kwargs: Arbitrary parameters.

        Keyword Args:
            domains (list): A list of domains to include in the order.
            paymentmethod (str): The payment method for the order.
            products: A list of products (dict) with an id and a domain name
                (`pid`, `domain`).

        Returns:
            The response of the successfully created order.

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

    def get_domains(
            self,
            active=None,
            offset=0):
        """
        Get domains (registrations).

        Keyword Args:
            active (bool): Filter on active or inactive domains.
            offset (int): How many items to skip.

        Yields:
            The domains.

        """
        while True:
            response = self.call(
                'GetClientsDomains',
                limitstart=offset)
            if not response['numreturned']:
                break
            for domain in response['domains']['domain']:
                if (active is True and domain['status'] != 'Active'
                        or active is False and domain['status'] == 'Active'):
                    continue
                yield domain
            offset += response['numreturned']

    def get_client_products(
            self,
            active=None,
            domain=None,
            offset=0,
            productid=None,
            **params):
        """
        Get client products.

        Keyword Args:
            active (bool): Filter on active or inactive domains.
            offset (int): How many items to skip.
            productid (int): Only get products with this product id.

        Yields:
            The products.

        """
        while True:
            params.update(
                limitstart=offset,
            )
            if productid:
                params['pid'] = productid
            response = self.call(
                'GetClientsProducts',
                **params)
            if not response['numreturned']:
                break
            for product in response['products']['product']:
                if (active is True and product['status'] != 'Active'
                        or active is False and product['status'] == 'Active'):
                    continue
                yield product
            offset += response['numreturned']

    def update_client_product(
            self,
            productid,
            **params):
        """
        Update a client's product.

        Args:
            productid (int): The id of the client product.

        Keyword Args:
            Passed as params to the API.

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
