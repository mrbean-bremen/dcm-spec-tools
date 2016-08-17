import os
import unittest

import pyfakefs.fake_filesystem_unittest

from tools.spec_reader.part6_reader import Part6Reader


class Part6ReaderTest(pyfakefs.fake_filesystem_unittest.TestCase):
    doc_contents = None

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'part06_excerpt.xml'), 'rb') as f:
            cls.doc_contents = f.read()

    def setUp(self):
        super(Part6ReaderTest, self).setUp()
        self.setUpPyfakefs()
        spec_path = os.path.join('dicom', 'specs')
        part6_path = os.path.join(spec_path, 'part06.xml')
        self.fs.CreateFile(part6_path, contents=self.doc_contents)
        self.reader = Part6Reader(spec_path)

    def test_undefined_id(self):
        self.assertIsNone(self.reader.data_element('(0011,0011)'))

    def test_data_element(self):
        element = self.reader.data_element('(0008,0005)')
        self.assertIsNotNone(element)
        self.assertEqual('Specific Character Set', element['name'])
        self.assertEqual('CS', element['vr'])
        self.assertEqual('1-n', element['vm'])

    def test_data_elements(self):
        elements = self.reader.data_elements()
        self.assertEqual(4, len(elements))

    def test_sop_class_uids(self):
        sop_class_uids = self.reader.sop_class_uids()
        self.assertEqual(3, len(sop_class_uids))
        self.assertIn('1.2.840.10008.1.1', sop_class_uids)
        self.assertEqual('Verification SOP Class', sop_class_uids['1.2.840.10008.1.1'])

    def test_uid_type(self):
        xfer_syntax_uids = self.reader.uids('Transfer Syntax')
        self.assertEqual(2, len(xfer_syntax_uids))
        self.assertIn('1.2.840.10008.1.2.4.80', xfer_syntax_uids)
        self.assertEqual('JPEG-LS Lossless Image Compression', xfer_syntax_uids['1.2.840.10008.1.2.4.80'])

    def test_sop_class_name(self):
        self.assertEqual('Enhanced US Volume Storage', self.reader.sop_class_name('1.2.840.10008.5.1.4.1.1.6.2'))

    def test_sop_class_uid(self):
        self.assertEqual('1.2.840.10008.5.1.4.1.1.2', self.reader.sop_class_uid('CT Image Storage'))

if __name__ == '__main__':
    unittest.main()