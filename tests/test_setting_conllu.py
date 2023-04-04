import os
import pytest
from conllu2xml.conlluparse.setting_conllu import read_conllu, write_conllu, del_id, del_hashlines, set_id, change_divider

@pytest.fixture
def sequoia_lines():
    file_path = os.path.join(os.path.dirname(__file__), 'sequoia-ud.conllu')
    return read_conllu(file_path)

def test_read_conllu(sequoia_lines):
    assert len(sequoia_lines) > 0

def test_del_id(sequoia_lines):
    lines = del_id(sequoia_lines)
    for line in lines:
        assert not line.startswith('# sent_id')

def test_del_hashlines(sequoia_lines):
    lines = del_hashlines(sequoia_lines)
    for line in lines:
        assert not line.startswith(tuple('# ' + s for s in ['newdoc', 'sent_id', 'text_en', 'genre', 'author', 'work',
                               'global.Entity',  'orig_file_sentence', 'english_text', 'newpar',
                                'sound_url', 'macrosyntax', 'status', 'title', 'speaker',
                                'review-category', 'review-place', 'review-date', 
                                'review-likes', 'review-dislikes']))

def test_set_id(sequoia_lines):
    lines = set_id(sequoia_lines)
    id_count = 0
    for line in lines:
        if line.startswith('# id ='):
            id_count += 1
            assert line.strip() == f'# id = {id_count}'

def test_change_divider(sequoia_lines):
    lines = change_divider(sequoia_lines)
    for line in lines:
        if not line.startswith('#'):
            columns = line.split('\t')
            if len(columns) >= 6:
                assert '|' not in columns[5]

def test_write_conllu(sequoia_lines):
    lines = del_id(sequoia_lines)
    lines = del_hashlines(lines)
    lines = set_id(lines)
    lines = change_divider(lines)

    output_file_path = os.path.join(os.path.dirname(__file__), 'sequoia-ud_tested.conllu')
    write_conllu(output_file_path, lines)

    # Check if the file is created
    assert os.path.exists(output_file_path)

    # Read the created file and check its content
    new_lines = read_conllu(output_file_path)
    assert len(new_lines) > 0
    assert new_lines == lines

    # Clean up by removing the created file
    #os.remove(output_file_path)