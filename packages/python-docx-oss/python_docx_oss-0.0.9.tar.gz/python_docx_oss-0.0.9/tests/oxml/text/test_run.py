"""
Test suite for the docx.oxml.text.run module.
"""
import pytest

from ...unitutil.cxml import element, xml


class DescribeCT_R(object):
    def it_can_add_a_t_preserving_edge_whitespace(self, add_t_fixture):
        r, text, expected_xml = add_t_fixture
        r.add_t(text)
        assert r.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            ("w:r", "foobar", 'w:r/w:t"foobar"'),
            ("w:r", "foobar ", 'w:r/w:t{xml:space=preserve}"foobar "'),
            (
                "w:r/(w:rPr/w:rStyle{w:val=emphasis}, w:cr)",
                "foobar",
                'w:r/(w:rPr/w:rStyle{w:val=emphasis}, w:cr, w:t"foobar")',
            ),
        ]
    )
    def add_t_fixture(self, request):
        initial_cxml, text, expected_cxml = request.param
        r = element(initial_cxml)
        expected_xml = xml(expected_cxml)
        return r, text, expected_xml


class TestCT_R:
    def test_texts(self, texts_item):
        element, ret = texts_item
        assert element.texts == ret

    def test_itertext(self, itertext_item):
        element, ret = itertext_item
        assert "".join(element.itertext()) == ret

    def load_params(self, request):
        xml, expected_text = request.param
        ctr = element(xml)
        return ctr, expected_text

    @pytest.fixture(
        params=[
            ('w:r/w:t"foobar"', "foobar"),
            ('w:r/(w:t"abc", w:tab, w:t"def", w:cr)', "abcdef"),
        ]
    )
    def itertext_item(self, request):
        return self.load_params(request)

    @pytest.fixture(
        params=[
            ('w:r/w:t"foobar"', "foobar"),
            ('w:r/(w:t"abc", w:tab, w:t"def", w:cr)', "abc\tdef\n"),
        ]
    )
    def texts_item(self, request):
        return self.load_params(request)
