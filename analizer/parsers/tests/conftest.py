import pytest


@pytest.fixture(scope='class')
def xml_data():
    data = '''<?xml version="1.0" encoding="utf-8"?>
    <sales_data date="2024-01-01">
    <products>
    <product>
    <id>1</id>
    <name>Product A</name>
    <quantity>100</quantity>
    <price>1500.00</price>
    <category>Electronics</category>
    </product>
    </products>
    </sales_data>'''
    return data


@pytest.fixture(scope='class')
def load_xml(tmpdir_factory, xml_data):
    tmp_path = tmpdir_factory.mktemp('data').join('data_xml.xml')
    with tmp_path.open(mode='w+', encoding='utf-8') as file_:
        file_.write(xml_data)
    return tmp_path


@pytest.fixture(scope='class')
def file_xml(load_xml):
    with load_xml.open(encoding='utf-8') as file_:
        xml = file_.read()
    return xml
