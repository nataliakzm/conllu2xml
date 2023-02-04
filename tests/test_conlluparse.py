import os
import sys
import unittest
import conlluparse

class TestConlluParse(unittest.TestCase):
    def setUp(self):
        # Create an input directory and a sample input file in it with the following contents: 
        self.input_dir = 'input'
        os.makedirs(self.input_dir, exist_ok=True)
        with open(os.path.join(self.input_dir, 'sample.conllu'), 'w') as f:
            f.write("# text = This is a sample input file.\n1\tThis\tthis\tDET\tDT\tDefinite=Def|PronType=Dem\n2\tis\tis\tVERB\tVBZ\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin\n3\ta\ta\tDET\tDT\tDefinite=Ind|PronType=Ind\n4\tsample\tsample\tNOUN\tNN\tNumber=Sing\n5\tinput\tinput\tNOUN\tNN\tNumber=Sing\n6\tfile\tfile\tNOUN\tNN\tNumber=Sing\n")

        # Create an output directory to store the output file in it 
        self.output_dir = 'output'
        os.makedirs(self.output_dir, exist_ok=True)

    def test_main(self):
        conlluparse.main(self.input_dir, self.output_dir)

        # Check if the output file has been created in the output directory 
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, 'sample_Modified.conllu')))

        # Read the output file and check if the contents are as expected 
        with open(os.path.join(self.output_dir, 'sample_Modified.conllu')) as f:
            output_contents = f.read()
            self.assertEqual(output_contents, "1\tThis\tthis\tDET\tDT\tDefinite=Def|PronType=Dem\n2\tis\tis\tVERB\tVBZ\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin\n3\ta\ta\tDET\tDT\tDefinite=Ind|PronType=Ind\n4\tsample\tsample\tNOUN\tNN\tNumber=Sing\n5\tinput\tinput\tNOUN\tNN\tNumber=Sing\n6\tfile\tfile\tNOUN\tNN\tNumber=Sing\n")
        
    def tearDown(self):
        # Delete the input and output directories 
        os.rmdir(self.input_dir)
        os.rmdir(self.output_dir)

if __name__ == '__main__':
    unittest.main()
