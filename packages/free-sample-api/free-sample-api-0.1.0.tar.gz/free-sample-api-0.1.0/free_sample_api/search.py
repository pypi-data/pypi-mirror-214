import requests
import json


POST_URL_SEARCH_PHP_PARAMETER = 'api_search.php?callback=jQuery2130710897661425719_1686994670460'
POST_URL_SEARCH_JSON_PARAMETER = 'search.json?page={}&page_size={}&search_term=a'


class REQUEST_DATA_FIELDS:
    QUERY = "q"
    PAGE = "page"


class RESPONSE_FIELDS:
    DATA = "data"
    APPLE = "apple"


RESPONSE_FIELD_TO_IGNORE = RESPONSE_FIELDS.APPLE


def _getResponseJsonFromResponseText(responseJsonResponseText):
    responseTracksJsonText = "{" + responseJsonResponseText.split("{", 2)[2]
    responseTracksJsonText = responseTracksJsonText[:len(
        responseTracksJsonText) - 4]
    return json.loads(responseTracksJsonText)


def _getFirstStringBetweenTwoStrings(string, string1, string2):
    return string.split(string1, 1)[1].split(string2, 1)[0]


def _isResponseTextIsValid(responseText):
    return _getFirstStringBetweenTwoStrings(responseText, "response\":", "});") == "null"


def search(baseurl, query, page):

    postDataToSendToScrappedWebsite = {
        REQUEST_DATA_FIELDS.QUERY: query,
        REQUEST_DATA_FIELDS.PAGE: str(page)
    }

    responseIsInvalid = True
    while responseIsInvalid:
        response = requests.post(
            url=baseurl + POST_URL_SEARCH_PHP_PARAMETER + POST_URL_SEARCH_JSON_PARAMETER,
            data=postDataToSendToScrappedWebsite)
        if response.status_code != 200:
            raise Exception("Error while searching: " + response.reason)
        responseIsInvalid = _isResponseTextIsValid(response.text)
    return _getResponseJsonFromResponseText(response.text)
