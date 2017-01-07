import os
import tempfile
import unittest

from coalib.output.ConfWriter import ConfWriter
from coalib.parsing.ConfParser import ConfParser


class ConfWriterTest(unittest.TestCase):
    example_file = ('to be ignored \n'
                    '    save=true\n'
                    '    a_default, another = val \n'
                    '    TEST = tobeignored  # thats a comment \n'
                    '    test = push \n'
                    '    t = \n'
                    '    [Section] \n'
                    '    [MakeFiles] \n'
                    '     j  , ANother = a \n'
                    '                   multiline \n'
                    '                   value \n'
                    '    ; just a omment \n'
                    '    ; just a omment \n'
                    '    key\\ space = value space\n'
                    '    key\\=equal = value=equal\n'
                    '    key\\\\backslash = value\\\\backslash\n'
                    '    key\\,comma = value,comma\n'
                    '    key\\#hash = value\\#hash\n'
                    '    key\\.dot = value.dot\n')

    def setUp(self):
        self.file = os.path.join(tempfile.gettempdir(), 'ConfParserTestFile')
        with open(self.file, 'w', encoding='utf-8') as file:
            file.write(self.example_file)

        self.conf_parser = ConfParser()
        self.write_file_name = os.path.join(tempfile.gettempdir(),
                                            'ConfWriterTestFile')
        self.write_dir_name = os.path.join(tempfile.gettempdir(),
                                           '')
        self.uut = ConfWriter(self.write_file_name)
        self.uut_dir = ConfWriter(self.write_dir_name)

    def tearDown(self):
        self.uut.close()
        os.remove(self.file)
        os.remove(self.write_file_name)
        self.uut_dir.close()
        os.remove(self.write_dir_name + '/.coafile')

    def test_exceptions(self):
        self.assertRaises(TypeError, self.uut.write_section, 5)

    def test_exceptions_dir(self):
        self.assertRaises(TypeError, self.uut_dir.write_section, 5)

    def test_write(self):
        result_file = ['[Default]\n',
                       'save = true\n',
                       'a_default, another = val\n',
                       '# thats a comment\n',
                       'test = push\n',
                       't = \n',
                       '[Section]\n',
                       '[MakeFiles]\n',
                       'j, ANother = a\n',
                       'multiline\n',
                       'value\n',
                       '; just a omment\n',
                       '; just a omment\n',
                       'key\\ space = value space\n',
                       'key\\=equal = value=equal\n',
                       'key\\\\backslash = value\\\\backslash\n',
                       'key\\,comma = value,comma\n',
                       'key\\#hash = value\\#hash\n',
                       'key\\.dot = value.dot\n']
        self.uut.write_sections(self.conf_parser.parse(self.file))
        self.uut.close()

        with open(self.write_file_name, 'r') as f:
            lines = f.readlines()

        self.assertEqual(result_file, lines)

    def test_write_with_dir(self):
        result_file = ['[Default]\n',
                       'save = true\n',
                       'a_default, another = val\n',
                       '# thats a comment\n',
                       'test = push\n',
                       't = \n',
                       '[Section]\n',
                       '[MakeFiles]\n',
                       'j, ANother = a\n',
                       'multiline\n',
                       'value\n',
                       '; just a omment\n',
                       '; just a omment\n',
                       'key\\ space = value space\n',
                       'key\\=equal = value=equal\n',
                       'key\\\\backslash = value\\\\backslash\n',
                       'key\\,comma = value,comma\n',
                       'key\\#hash = value\\#hash\n',
                       'key\\.dot = value.dot\n']
        self.uut_dir.write_sections(self.conf_parser.parse(self.file))
        self.uut_dir.close()

        with open(self.write_dir_name + '/.coafile', 'r') as f:
            lines = f.readlines()

        self.assertEqual(result_file, lines)
