from scrapy.exporters import JsonItemExporter
from __future__ import absolute_import
import re
import json
import marshal
import tempfile
import unittest
from io import BytesIO
from datetime import datetime

import lxml.etree
import six

from scrapy.item import Item, Field
from scrapy.utils.python import to_unicode
from scrapy.exporters import (
    BaseItemExporter, PprintItemExporter, PickleItemExporter, CsvItemExporter,
    XmlItemExporter, JsonLinesItemExporter, JsonItemExporter,
    PythonItemExporter, MarshalItemExporter
)


class TestItem(Item):
    name = Field()
    age = Field()

class BaseItemExporterTest(unittest.TestCase):

    def setUp(self):
        self.i = TestItem(name=u'John\xa3', age=u'22')
        self.output = BytesIO()
        self.ie = self._get_exporter()

    def _get_exporter(self, **kwargs):
        return BaseItemExporter(**kwargs)

    def _check_output(self):
        pass

    def _assert_expected_item(self, exported_dict):
        for k, v in exported_dict.items():
            exported_dict[k] = to_unicode(v)
        self.assertEqual(self.i, exported_dict)

    def _get_nonstring_types_item(self):
        return {
            'boolean': False,
            'number': 22,
            'time': datetime(2015, 1, 1, 1, 1, 1),
            'float': 3.14,
        }

    def assertItemExportWorks(self, item):
        self.ie.start_exporting()
        try:
            self.ie.export_item(item)
        except NotImplementedError:
            if self.ie.__class__ is not BaseItemExporter:
                raise
        self.ie.finish_exporting()
        self._check_output()

    def test_export_item(self):
        self.assertItemExportWorks(self.i)

    def test_export_dict_item(self):
        self.assertItemExportWorks(dict(self.i))

    def test_serialize_field(self):
        res = self.ie.serialize_field(self.i.fields['name'], 'name', self.i['name'])
        self.assertEqual(res, u'John\xa3')

        res = self.ie.serialize_field(self.i.fields['age'], 'age', self.i['age'])
        self.assertEqual(res, u'22')

    def test_fields_to_export(self):
        ie = self._get_exporter(fields_to_export=['name'])
        self.assertEqual(list(ie._get_serialized_fields(self.i)), [('name', u'John\xa3')])

        ie = self._get_exporter(fields_to_export=['name'], encoding='latin-1')
        _, name = list(ie._get_serialized_fields(self.i))[0]
        assert isinstance(name, six.text_type)
        self.assertEqual(name, u'John\xa3')

    def test_field_custom_serializer(self):
        def custom_serializer(value):
            return str(int(value) + 2)

        class CustomFieldItem(Item):
            name = Field()
            age = Field(serializer=custom_serializer)

        i = CustomFieldItem(name=u'John\xa3', age=u'22')

        ie = self._get_exporter()
        self.assertEqual(ie.serialize_field(i.fields['name'], 'name', i['name']), u'John\xa3')
        self.assertEqual(ie.serialize_field(i.fields['age'], 'age', i['age']), '24')


class JsonExporterPipeline(object):

    def __init__(self):
        #open a json file
        self.file = open('articleexport.json','wb')
        #create a JsonExporter Instance
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        #start exporting
        self.exporter.start_exporting()

    def close_spider(self,spider):
        #finish exporting
        self.exporter.finish_exporting()
        #close file
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
