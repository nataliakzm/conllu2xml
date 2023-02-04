import unittest
import sys
import os

sys.path.append('./src')
from conlluparse import setting_conllu

class TestSettingConllu(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test.conllu'
        self.lines = ['# text = Sentence 1\n',
                      '1\tToken 1\tToken 1\tPOS\tLEMMA\tMORPH\n',
                      '2\tToken 2\tToken 2\tPOS\tLEMMA\tMORPH\n']
        with open(self.test_file, 'w') as f:
            f.writelines(self.lines)

    def test_read_conllu(self):
        lines = setting_conllu.read_conllu(self.test_file)
        self.assertEqual(lines, self.lines)

    def test_write_conllu(self):
        new_lines = ['# text = Sentence 2\n',
                      '1\tToken 1\tToken 1\tPOS\tLEMMA\tMORPH\n',
                      '2\tToken 2\tToken 2\tPOS\tLEMMA\tMORPH\n']
        setting_conllu.write_conllu(self.test_file, new_lines)
        lines = setting_conllu.read_conllu(self.test_file)
        self.assertEqual(lines, new_lines)

    def test_del_id(self):
        lines = setting_conllu.del_id(self.lines)
        self.assertEqual(lines, self.lines)

    def test_del_hashlines(self):
        lines = ['# text = Sentence 1\n',
                      '1\tToken 1\tToken 1\tPOS\tLEMMA\tMORPH\n',
                      '2\tToken 2\tToken 2\tPOS\tLEMMA\tMORPH\n']
        new_lines = setting_conllu.del_hashlines(lines)
        self.assertEqual(new_lines, lines)

    def test_set_id(self):
        lines = ['# text = Sentence 1\n',
                      '1\tToken 1\tToken 1\tPOS\tLEMMA\tMORPH\n',
                      '2\tToken 2\tToken 2\tPOS\tLEMMA\tMORPH\n']
        new_lines = setting_conllu.set_id(lines)
        self.assertEqual(new_lines, ['# id = 1\n'] + lines)

    def test_change_divider(self):
        lines = ['1\tToken 1\tToken 1\tPOS\tLEMMA|LEMMA\tMORPH|MORPH\n',
                 '2\tToken 2\tToken 2\tPOS\tLEMMA|LEMMA\tMORPH|MORPH\n']
        new_lines = setting_conllu.change_divider(lines)
        self.assertEqual(new_lines, [ '1\tToken 1\tToken 1\tPOS\tLEMMA:LEMMA\tMORPH:MORPH\n',
                                      '2\tToken 2\tToken 2\tPOS\tLEMMA:LEMMA\tMORPH:MORPH\n'])
    def tearDown(self):
        # Delete the input and output directories 
        os.rmdir(self.input_dir)
        os.rmdir(self.output_dir)

if __name__ == '__main__':
    unittest.main()                                     