NINEGAG_URL = "https://9gag.com"


class NinegagXpaths:
    POST = '//article[contains(@id, "jsid-post")]'
    JSON = '//script[starts-with(text(), "window._config")]'

    class Post:
        LINK = './/h1/parent::a'
        TYPE_DIV = './/div[contains(@class, "post-container")]//a/div'
