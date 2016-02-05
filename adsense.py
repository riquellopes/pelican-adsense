from __future__ import unicode_literals

import re
from pelican import signals
from jinja2 import Template

ADSENSE_REGEX = re.compile(
    r'(<p>\[adsense:client\=([^\]]+),slot\=([0-9]+),type_ad\=([a-zA-Z]+)?\]</p>)')


class Tpl(object):
    HEAD = """
        <ins class="adsbygoogle" style="display:inline-block;width:728px;height:90px"
                     data-ad-client="{{client}}"
                    data-ad-slot="{{slot}}"></ins>
    """.strip()
    LINK = """
        <ins class="adsbygoogle" style="display:inline-block;width:728px;height:15px"
                     data-ad-client="{{client}}"
                     data-ad-slot="{{slot}}"></ins>
    """.strip()


def get_tpl(type_ad):
    return getattr(Tpl, type_ad.upper())


def add_adsense_tag(generator):
    """
        [adsense:client=ca-pub-123456,slot=123456,type_ad=head]
    """

    for article in generator.articles:
        for adsense in ADSENSE_REGEX.findall(article._content):
            tpl = Template(get_tpl(adsense[3]))
            context = generator.context.copy()
            context.update({
                'client': adsense[1],
                'slot': adsense[2],
            })

            replacement = tpl.render(context)
            article._content = article._content.replace(adsense[0], replacement)


def register():
    signals.article_generator_finalized.connect(add_adsense_tag)
