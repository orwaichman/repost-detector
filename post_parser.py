from lxml import html

from google_search.const import GOOGLE_IMAGE_URL_SEARCH_URL

import utils
from const import NinegagXpaths
from post_analysis import PostAnalysis
from post_info import PostInfo


class PostParser(object):
    @classmethod
    def analyze_page(cls, src):
        root = html.fromstring(src)
        site_json_script = root.xpath(NinegagXpaths.JSON)[0].text_content()
        posts_info = {item['id']: item for item in utils.parse_site_json(site_json_script)}

        parsed_posts = {}
        for article in root.xpath(NinegagXpaths.POST):
            parsed_posts[cls.post_id_from_article(article)] = cls.analyze_article(article, posts_info)
        return parsed_posts

        # return {cls.post_id_from_article(article): cls.analyze_article(article, posts_info) for article in root.xpath(NinegagXpaths.POST)}

    @classmethod
    def post_id_from_article(cls, article):
        return article.attrib['id'].replace('jsid-post-', '')

    @classmethod
    def analyze_article(cls, article, posts_info):
        post_id = cls.post_id_from_article(article)
        try:
            if isinstance(posts_info, PostInfo):
                post_info = posts_info
            else:
                post_info = posts_info[post_id]
        except KeyError:
            return None

        if post_info.not_analyzable():
            return None

        post_classes = article.xpath(NinegagXpaths.Post.TYPE_DIV)[0].attrib['class'].split()
        post_classes.remove('post-view')
        post_type = post_classes.pop().replace('-post', '')

        image_search_reference = GOOGLE_IMAGE_URL_SEARCH_URL.format(image_url=post_info.image_url)

        # try:
        image_results = utils.get_image_search_results(post_info.image_url)
        # except Exception:
            # image_results = None

        return PostAnalysis(post_id, post_type, image_results, image_search_reference)
