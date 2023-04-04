import os
import tempfile
from conllu2xml.conlluparse.combine_all import conllu, dupl_check

def test_conllu():
    # Create a temporary input directory with two conllu files
    with tempfile.TemporaryDirectory() as temp_input_dir:
        with open(os.path.join(temp_input_dir, 'sequoia-ud_1.conllu'), 'w') as f1:
            f1.write("# id = 1\n# text = Pourquoi ce thème ?\n1\tPourquoi\tpourquoi\tADV\t_\tPronType=Int\t3\tadvmod\t_\t_\n2\tce\tce\tDET\t_\tGender=Masc|Number=Sing|PronType=Dem\t3\tdet\t_\t_\n3\tthème\tthème\tNOUN\t_\tGender=Masc|Number=Sing\t_\t_\t_\t_\n4\t?\t?\tPUNCT\t_\t_\t3\tpunct\t_\t_\n\n")
        with open(os.path.join(temp_input_dir, 'sequoia-ud_2.conllu'), 'w') as f2:
            f2.write("# id = 1\n# text = Gutenberg\n1\tGutenberg\tGutenberg\tPROPN\t_\t_\t_\t_\t_\t_\n\n")

        # Create a temporary output file
        with tempfile.NamedTemporaryFile(delete=False) as temp_output_file:
            output_file = temp_output_file.name

            # Call the conllu function
            conllu(temp_input_dir, output_file)

            with open(output_file, 'r') as out_file:
                result = out_file.read()
                expected_output = "# id = 1\n# text = Pourquoi ce thème ?\n1\tPourquoi\tpourquoi\tADV\t_\tPronType=Int\t3\tadvmod\t_\t_\n2\tce\tce\tDET\t_\tGender=Masc|Number=Sing|PronType=Dem\t3\tdet\t_\t_\n3\tthème\tthème\tNOUN\t_\tGender=Masc|Number=Sing\t_\t_\t_\t_\n4\t?\t?\tPUNCT\t_\t_\t3\tpunct\t_\t_\n\n# id = 2\n# text = Gutenberg\n1\tGutenberg\tGutenberg\tPROPN\t_\t_\t_\t_\t_\t_\n\n"
                assert result == expected_output, f"Expected: {expected_output}, but got: {result}"   

def test_dupl_check():
    # Create a temporary input file with duplicate sentences
    with tempfile.NamedTemporaryFile(delete=False) as temp_input_file:
        input_file = temp_input_file.name
        temp_input_file.write("# id = 1\n# text = Gutenberg\n1\tGutenberg\tGutenberg\tPROPN\t_\t_\t_\t_\t_\t_\n\n# id = 2\n# text = Pourquoi ce thème ?\n1\tPourquoi\tpourquoi\tADV\t_\tPronType=Int\t3\tadvmod\t_\t_\n2\tce\tce\tDET\t_\tGender=Masc|Number=Sing|PronType=Dem\t3\tdet\t_\t_\n3\tthème\tthème\tNOUN\t_\tGender=Masc|Number=Sing\t_\t_\t_\t_\n4\t?\t?\tPUNCT\t_\t_\t3\tpunct\t_\t_\n\n# id = 3\n# text = Gutenberg\n1\tGutenberg\tGutenberg\tPROPN\t_\t_\t_\t_\t_\t_\n\n")
        temp_input_file.flush()

        # Call the dupl_check function
        result = dupl_check(input_file)

        # Check that the duplicates were removed
        with open(input_file, 'r') as out_file:
            result_lines = out_file.readlines()
            expected_lines = ["# id = 1\n# text = Gutenberg\n1\tGutenberg\tGutenberg\tPROPN\t_\t_\t_\t_\t_\t_\n\n# id = 2\n# text = Pourquoi ce thème ?\n1\tPourquoi\tpourquoi\tADV\t_\tPronType=Int\t3\tadvmod\t_\t_\n2\tce\tce\tDET\t_\tGender=Masc|Number=Sing|PronType=Dem\t3\tdet\t_\t_\n3\tthème\tthème\tNOUN\t_\tGender=Masc|Number=Sing\t_\t_\t_\t_\n4\t?\t?\tPUNCT\t_\t_\t3\tpunct\t_\t_\n\n"]
            assert result_lines == expected_lines, f"Expected: {expected_lines}, but got: {result_lines}"

        # Check that the function returns 'Yes' for duplicates found
        assert result == 'Yes', f"Expected 'Yes', but got {result}"
