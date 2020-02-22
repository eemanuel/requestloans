import requests

from requestloans.settings import URL_SCORING_SERVICE


class LoanRequester(object):

    def request(self, data):
        return requests.get(URL_SCORING_SERVICE, params=data)
