import sys
import requests
import json


POST_URL_SEARCH_PHP_PARAMETER = 'api_search.php?callback=jQuery2130710897661425719_1686994670460'
POST_URL_SEARCH_JSON_PARAMETER = 'search.json?page={}&page_size={}&search_term=a'


class REQUEST_DATA_FIELDS:
    QUERY = "q"
    PAGE = "page"


class RESPONSE_FIELDS:
    DATA = "data"
    RESPONSE = "response"


def _get_response_json_from_response_text(response_json_response_text):
    response_tracks_json_text = "{" + response_json_response_text.split("{", 2)[2]
    response_tracks_json_text = response_tracks_json_text[:len(
        response_tracks_json_text) - 4]
    return json.loads(response_tracks_json_text)


def _get_first_string_between_two_strings(string, string1, string2):
    return string.split(string1, 1)[1].split(string2, 1)[0]


def _is_response_text_valid(response_text):
    return _get_first_string_between_two_strings(response_text, RESPONSE_FIELDS.RESPONSE + "\":", "});") == "null"


def search(baseurl, query, page):

    post_data_to_send_to_scrapped_website = {
        REQUEST_DATA_FIELDS.QUERY: query,
        REQUEST_DATA_FIELDS.PAGE: str(page)
    }

    response_is_invalid = True
    while response_is_invalid:
        response = requests.post(
            url=baseurl + POST_URL_SEARCH_PHP_PARAMETER + POST_URL_SEARCH_JSON_PARAMETER,
            data=post_data_to_send_to_scrapped_website)
        if response.status_code != 200:
            raise Exception("Error while searching: " + response.reason)
        response_is_invalid = _is_response_text_valid(response.text)
    response_json_raw = _get_response_json_from_response_text(response.text)
    return get_cleaned_response_json(response_json_raw)   

    
def get_cleaned_response_json(response_json_raw):
    return response_json_raw[RESPONSE_FIELDS.RESPONSE][1:]


if __name__=="__main__":
    search(sys.argv[1], sys.argv[2], sys.argv[3])
