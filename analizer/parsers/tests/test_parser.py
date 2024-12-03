import pytest
import datetime
from collections import abc

from parsers import FileXMLParser, StringXMLParser


class TestParser:
    """
    Тесты парсера
    """

    @pytest.mark.parser
    def test_leng_xml_parse(self, file_xml):
        parser = StringXMLParser(file_xml, 'product')
        assert len(parser.get_list()) == 1

    @pytest.mark.parser
    def test_parse_item_with_str(self, file_xml):
        parser = StringXMLParser(file_xml, 'product')
        assert parser.get_list()[0] == dict(id=1,
                                            name='Product A',
                                            quantity=100,
                                            price=1500.00,
                                            category='Electronics',
                                            )

    @pytest.mark.parser
    def test_parse_item_with_file(self, load_xml):
        with load_xml.open(encoding='utf-8') as _file:
            parser = FileXMLParser(_file, 'product')
        assert parser.get_list()[0] == dict(id=1,
                                            name='Product A',
                                            quantity=100,
                                            price=1500.00,
                                            category='Electronics',
                                            )

    @pytest.mark.parser
    def test_parse_item_with_path_file(self, load_xml):
        parser = FileXMLParser(load_xml, 'product')
        assert parser.get_list()[0] == dict(id=1,
                                            name='Product A',
                                            quantity=100,
                                            price=1500.00,
                                            category='Electronics',
                                            )

    def test_parse_item_with_str_generator(self, file_xml):
        parser = StringXMLParser(file_xml, 'product')
        assert isinstance(parser.get_generator(), abc.Generator)

    @pytest.mark.parser
    def test_parse_attrs(self, file_xml):
        parser = StringXMLParser(file_xml, 'product', attrs=('date',))
        assert parser.attrs['date'] == datetime.date(2024, 1, 1)

    @pytest.mark.parser
    def test_parse_items_without_converter(self, file_xml):
        parser = StringXMLParser(file_xml, 'product', type_converter=None)
        assert parser.get_list()[0] == dict(id='1',
                                            name='Product A',
                                            quantity='100',
                                            price='1500.00',
                                            category='Electronics',
                                            )

    @pytest.mark.parser
    def test_parse_items_without_int_converter(self, file_xml):
        parser = StringXMLParser(file_xml, 'product', convert_int=False)
        assert parser.get_list()[0]['quantity'] == '100'

    @pytest.mark.parser
    def test_parse_items_without_float_converter(self, file_xml):
        parser = StringXMLParser(file_xml, 'product', convert_float=False)
        assert parser.get_list()[0]['price'] == '1500.00'

    @pytest.mark.parser
    def test_parse_items_without_date_converter(self, file_xml):
        parser = StringXMLParser(file_xml,
                                 'product',
                                 attrs=('date',),
                                 convert_date=False,
                                 )
        assert parser.attrs['date'] == '2024-01-01'
