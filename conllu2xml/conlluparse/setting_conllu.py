# setting_conllu.py
# This script is used to set the id of the conllu file and delete unnecessary hash lines

def read_conllu(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return lines

def write_conllu(file_path, lines):
    with open(file_path,'w') as f:
        f.writelines(lines)

def del_id(lines):
    for line in lines:
        if line.startswith('# sent_id'):
            lines.remove(line)
    return lines

def del_hashlines(lines):
    new_lines = []
    for line in lines:
        if not line.startswith(('# newdoc', '# sent_id', '# text_en', '# genre', '# author', '# work',
                               '# global.Entity',  '# orig_file_sentence', '# english_text', '# newpar',
                                '# sound_url', '# macrosyntax', '# status', '# title', '# speaker'
                                '# review-category', '# review-place', '# review-date', 
                                '# review-likes', '# review-dislikes')):
            new_lines.append(line)
    return new_lines

def set_id(lines):
    new_lines = []
    id = 1
    for line in lines:
        if line.startswith('# text ='):
            new_lines.append('# id = ' + str(id) + '\n')
            id += 1
        new_lines.append(line)
    return new_lines

# Change all | dividers to : dividers only in the colunm 5 (LEMMA) and 6 (MORPH)
def change_divider(lines):
    new_lines = []
    for line in lines:
        if line.startswith('#'):
            new_lines.append(line)
        else:
            new_line = line.split('\t')
            if len(new_line) >= 6:
                new_line[5] = new_line[5].replace('|', ':')
            new_lines.append('\t'.join(new_line))
    return new_lines