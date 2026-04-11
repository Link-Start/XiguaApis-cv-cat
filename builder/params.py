import re
import time
import requests

from builder.header import HeaderBuilder

class Params:
    def __init__(self):
        self.params = {}

    def add_param_by_dict(self, params):
        self.params.update(params)

    def add_param(self, key, value):
        self.params[key] = value

    def get(self):
        return self.params


class ParamsBuilder:
    base_url = 'https://www.ixigua.com/'

    @staticmethod
    def build_get_user_info_param():
        params = Params()
        params.add_param_by_dict({
            "source": "pgc_author_profile",
            "list_entrance": "anyVideo"
        })
        return params

    @staticmethod
    def build_get_work_info_param():
        params = Params()
        params.add_param_by_dict({
            "logTag": "3e14bd419bde49d00475"
        })
        return params
    @staticmethod
    def build_get_user_work_param(user_id, offset=0):
        params = Params()
        params.add_param_by_dict({
            "to_user_id": user_id,
            "offset": str(offset),
            "limit": "30",
            "maxBehotTime": "",
            "order": "new",
            "isHome": "0",
            "aid": "1768",
            "msToken": "",
            "X-Bogus": "",
            "_signature": ""
        })
        return params

    @staticmethod
    def build_get_work_out_comment_param(user_id, offset=0):
        params = Params()
        params.add_param_by_dict({
            "tab_index": "0",
            "count": "10",
            "offset": str(offset),
            "group_id": user_id,
            "item_id": user_id,
            "aid": "1768",
            "msToken": "",
            "X-Bogus": "",
            "_signature": ""
        })
        return params

    @staticmethod
    def build_get_work_inner_comment_param(comment_id, offset=0):
        params = Params()
        params.add_param_by_dict({
            "count": "10",
            "offset": str(offset),
            "aid": "1768",
            "id": comment_id,
            "msToken": "",
            "X-Bogus": "",
            "_signature": ""
        })
        return params

    @staticmethod
    def build_get_search_param():
        params = Params()
        params.add_param_by_dict({
            "search_id": "",
            "fss": "default_search",
            "aid": "1768",
            "msToken": "",
            "X-Bogus": "",
            "_signature": ""
        })
        return params
