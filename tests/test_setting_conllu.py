import os
import tempfile
from conllu2xml.conlluparse.setting_conllu import read_conllu, write_conllu, del_id, del_hashlines, set_id, change_divider

def test_read_conllu_write_conllu():
    # Create a temporary file and write the sample content
    content = "Sample conllu content\n"
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file:
        tmp_file.write(content)

    # Check if the content is read correctly
    lines = read_conllu(tmp_file.name)
    assert lines == content.splitlines(True), f"Expected {content}, but got {lines}"

    # Create another temporary file for writing the content using write_conllu()
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file2:
        write_conllu(tmp_file2.name, lines)

        # Read the content back from the file
        tmp_file2.seek(0)
        written_content = tmp_file2.read()

    # Check if the content is written correctly
    assert written_content == content, f"Expected {content}, but got {written_content}"

    # Clean up temporary files
    os.remove(tmp_file.name)
    os.remove(tmp_file2.name)

def test_del_id():
    lines = [
        "# sent_id = 1\n",
        "This is a test.\n",
        "# sent_id = 2\n",
        "This is another test.\n"
    ]
    expected_output = [
        "This is a test.\n",
        "This is another test.\n"
    ]
    result = del_id(lines)
    assert result == expected_output, f"Expected {expected_output}, but got {result}"

def test_del_hashlines():
    lines = [
        "# newdoc\n",
        "# sent_id = 1\n",
        "This is a test.\n",
        "# sent_id = 2\n",
        "This is another test.\n"
    ]
    expected_output = [
        "This is a test.\n",
        "This is another test.\n"
    ]
    result = del_hashlines(lines)
    assert result == expected_output, f"Expected {expected_output}, but got {result}"

def test_set_id():
    lines = [
        "# text = This is a test.\n",
        "This is a test.\n",
        "# text = This is another test.\n",
        "This is another test.\n"
    ]
    expected_output = [
        "# id = 1\n",
        "# text = This is a test.\n",
        "This is a test.\n",
        "# id = 2\n",
        "# text = This is another test.\n",
        "This is another test.\n"
    ]
    result = set_id(lines)
    assert result == expected_output, f"Expected {expected_output}, but got {result}"

def test_change_divider():
    lines = [
        "# id = 1\n",
        "le\t_\tle\tDET\t_\tDefinite=Def|Gender=Masc|Number=Sing|PronType=Art\t7\tdet\t_\t_\n",
        "# id = 2\n",
        "XIIe\tXIIe\tADJ\t_\tNumType=Ord\t9\tamod\t_\t_\n"
    ]
    expected_output = [
        "# id = 1\n",
        "le\t_\tle\tDET\t_\tDefinite=Def:Gender=Masc:Number=Sing:PronType=Art\t7\tdet\t_\t_\n",
        "# id = 2\n",
        "XIIe\tXIIe\tADJ\t_\tNumType=Ord\t9\tamod\t_\t_\n"
    ]
    result = change_divider(lines)
    assert result == expected_output, f"Expected {expected_output}, but got {result}"