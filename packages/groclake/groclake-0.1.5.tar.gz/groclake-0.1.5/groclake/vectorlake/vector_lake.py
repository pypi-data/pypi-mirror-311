
from ..groc_default.groc_base import Groc


class GrocVector(Groc):

    def __init__(self, vectorlake_id=''):
        super().__init__()
        self.vectorlake_id = vectorlake_id

    def get_payload_from_product_object(self, payload):
        if type(self) is not VectorLakeCreate and self.vectorlake_id:
            payload.update({'vectorlake_id': self.vectorlake_id})
        return payload


class VectorLakeFetch(GrocVector):
    api_endpoint = '/vector/fetch'

    def fetch(self, query):
        return self.call_api({'query': query})


class VectorLakePush(GrocVector):
    api_endpoint = '/vector/push'

    def push(self, payload):
        return self.call_api(payload)


class VectorLakeSearch(GrocVector):
    api_endpoint = '/vector/search'

    def search(self, payload):
        return self.call_api(payload)


class VectorLakeCreate(GrocVector):
    api_endpoint = '/vector/create'

    def create(self):
        return self.call_api({})


class VectorLake:
    def __init__(self, vectorlake_id=''):
        self.vectorlake_id = vectorlake_id
        self._fetcher = None
        self._pusher = None
        self._searcher = None
        self._creator = None

    def _get_fetcher(self):
        if self._fetcher is None:
            self._fetcher = VectorLakeFetch(self.vectorlake_id)
        return self._fetcher

    def _get_pusher(self):
        if self._pusher is None:
            self._pusher = VectorLakePush(self.vectorlake_id)
        return self._pusher

    def _get_searcher(self):
        if self._searcher is None:
            self._searcher = VectorLakeSearch(self.vectorlake_id)
        return self._searcher

    def _get_creator(self):
        if self._creator is None:
            self._creator = VectorLakeCreate(self.vectorlake_id)
        return self._creator

    def fetch(self, query):
        return self._get_fetcher().fetch(query)

    def push(self, payload):
        return self._get_pusher().push(payload)

    def search(self, payload):
        return self._get_searcher().search(payload)

    def create(self):
        create_response = self._get_creator().create()
        if create_response.get('vectorlake_id'):
            self.vectorlake_id = create_response.get('vectorlake_id')
        return create_response
