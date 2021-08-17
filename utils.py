import json

from google_search import Searcher

from post_info import PostInfo


def parse_site_json(raw_text):
    """
    Parses text from a script from a 9GAG's feed's html that contains detailed information about the currently
    displayed posts
    Args:
        raw_text (str): Text from the script

    Returns:
        list: Posts represented as dicts
    """
    # Actual json is obfuscated as argument for function, so we prepare it for parsing
    raw_json = raw_text.split('("', 1)[1].rsplit('")', 1)[0]
    del raw_text
    raw_json = raw_json.replace(r'\"', '"')
    raw_json = raw_json.replace(r'\\', '\\')
    raw_json = raw_json.replace(r'\/', '/')

    parsed_json = json.loads(raw_json)
    del raw_json

    # Extracting post list, and cast objects in it to PostInfo
    return [PostInfo(item) for item in parsed_json['data']['posts']]


def get_image_search_results(image_url):
    with Searcher() as s:
        s.search_image(image_url)
        s.navigate_to_identical_images()
        return s.scan_image_results()