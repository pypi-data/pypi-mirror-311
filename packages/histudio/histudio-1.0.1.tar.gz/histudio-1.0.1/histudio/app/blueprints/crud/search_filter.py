from histudio.app.models.search_filter import SearchFilter

from histudio.app.blueprints.crud.base import BaseModelResource, BaseModelsResource


class SearchFiltersResource(BaseModelsResource):
    def __init__(self):
        BaseModelsResource.__init__(self, SearchFilter)


class SearchFilterResource(BaseModelResource):
    def __init__(self):
        BaseModelResource.__init__(self, SearchFilter)
