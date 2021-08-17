import datetime


class PostInfo(object):
    def __init__(self, obj_json, up_to_date=None):
        self._dict = obj_json
        self.up_to_date = up_to_date if up_to_date else datetime.datetime.now()

    def __getitem__(self, key):
        try:
            return self._dict[key]
        except AttributeError:
            return KeyError(key)

    def __setitem__(self, key, newvalue):
        self.__getitem__(key)
        raise RuntimeError('PostInfo is read only')

    def __str__(self):
        return str(self._dict)

    def to_dict(self):
        return self._dict

    def __getattribute__(self, item):
        if item in ('id', 'url', 'title'):
            # Unchanged attributes, take as-is from json
            return self._dict[item]
        else:
            return super().__getattribute__(item)

    @property
    def type(self):
        """
        Options for type attribute:
        * Photo - standard post
        * Animated - GIF or video (no way of knowing which without checking the html)
        * Article - a board
        """
        return self._dict['type']

    @property
    def comments_count(self):
        return self._dict['commentsCount']

    @property
    def upvotes(self):
        return self._dict['upVoteCount']

    @property
    def downvotes(self):
        return self._dict['downVoteCount']

    @property
    def date_created(self):
        return datetime.datetime.fromtimestamp(self._dict['creationTs'])

    @property
    def image_url(self):
        return self._dict['images']['image700']['url']

    @property
    def section(self):
        return self._dict['postSection']['name'].strip()

    @property
    def tags(self):
        return [item['key'] for item in self._dict['tags']]

    def not_analyzable(self):
        return any((
            self._dict['type'] != 'Photo',
            self.is_board(),
            self._dict['nsfw'] == 1,
            self._dict['promoted'] == 1,
            self._dict['hasLongPostCover'] == 1
        ))

    def is_board(self):
        return 'board' in self._dict
