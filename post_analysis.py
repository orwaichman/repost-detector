PARAGRAPH = '<p>{text}</p>'


class PostAnalysis(object):
    def __init__(self, post_id, post_type, image_results, image_search_reference=None):
        self.post_id = post_id
        self.post_type = post_type
        self.image_results = list(image_results)
        self.image_search_reference = image_search_reference

    def to_html(self):
        return ''.join((PARAGRAPH.format(text=f'ID: {self.post_id}'),
                       PARAGRAPH.format(text=f'Type: {self.post_type}'),
                       '<br>',
                        self._summarize_image_results(self.image_results, self.image_search_reference)))

    @staticmethod
    def _summarize_image_results(image_results, image_search_reference):
        if image_results is None:
            return PARAGRAPH.format(text='Failed to search image')
        elif len(image_results) == 0:
            return PARAGRAPH.format(text='Did not find copies')

        image_search_url_link = f'<a href="{image_search_reference}">{{count}}</a>' if image_search_reference else '{count}'
        text = PARAGRAPH.format(text=f'Copies found: {image_search_url_link.format(count=len(image_results))}')

        for site_name in ('9gag', 'reddit', 'facebook'):
            results_count = len([result for result in image_results if site_name in result.site.lower()])
            if results_count:
                text += PARAGRAPH.format(text=f'&ensp;{site_name.capitalize()}: {results_count}')

        return text
