import pytest
from adsense import ADSENSE_REGEX, get_tpl, Tpl


def test_get_head_adsense():
    match = ADSENSE_REGEX.findall(
        "<p>[adsense:client=ca-pub-123456,slot=123456,type_ad=head]</p>")[0]

    assert match[1] == "ca-pub-123456"
    assert match[2] == "123456"
    assert match[3] == "head"


def test_get_adsense_error():
    match = ADSENSE_REGEX.findall(
        "<p>[adsense:client=ca-pub-123456,slot=123456]</p>")

    assert len(match) == 0


def test_get_tpl_head():
    tpl = get_tpl("head")
    assert tpl == Tpl.HEAD


def test_get_tpl_link():
    tpl = get_tpl("link")
    assert tpl == Tpl.LINK


def test_does_not_tpl_exists():
    with pytest.raises(AttributeError):
        get_tpl("anything")
