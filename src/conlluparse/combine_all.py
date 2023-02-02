def conllu(input_dir, output_file):
    with open(output_file, 'w') as out_file:
        id = 1
        for file in os.listdir(input_dir):
            if file.endswith('.conllu'):
                with open(os.path.join(input_dir, file), 'r') as in_file:
                    lines = in_file.readlines()
                    new_lines = []
                    for line in lines:
                        if line.startswith('# id = '):
                            line = '# id = ' + str(id) + '\n'
                            id += 1
                        if not line.startswith('# global.columns'):
                            new_lines.append(line)
                    out_file.writelines(new_lines)
                    out_file.write('\n')

def dupl_check(input_file):
    texts = {}
    with open(input_file, 'r') as in_file:
        lines = in_file.readlines()
        id = None
        for line in lines:
            if line.startswith('# id = '):
                id = line[7:].strip()
            elif line.startswith('# text = '):
                text = line[9:].strip()
                if text in texts:
                    texts[text].append(id)
                else:
                    texts[text] = [id]
    duplicates = False
    for text, ids in texts.items():
        if len(ids) > 1:
            duplicates = True
            print('id:', ', '.join(ids))
    if duplicates:
        # delete all duplicates except the first one and update the ids in the file 
        for text, ids in texts.items():
            if len(ids) > 1:
                for id in ids[1:]:

                    with open(input_file, 'r') as in_file:
                        lines = in_file.readlines()

                    with open(input_file, 'w') as out_file:
                        skip_lines = False
                        for line in lines:
                            if line.startswith('# id = '):
                                # check if the id matches the id we want to delete and set the flag to skip the lines if it does match 
                                if line[7:].strip() == id:
                                    # set the flag to skip all lines until the next '# id = ' line is found 
                                    skip_lines = True
                                    print("Id deleted:", id)
                                else:
                                    # reset the flag if the id doesn't match the id we want to delete 
                                    skip_lines = False
                            # write the line if the flag isn't set  
                            if not skip_lines:
                                out_file.write(line)
        # reset the counter
        counter = 1

        with open(input_file, 'w') as out_file:
            for line in lines:
                # if the line starts with '# id = ', update the id with the current counter value and increase the counter by 1 
                if line.startswith('# id = '):
                    out_file.write('# id = ' + str(counter) + '\n')
                    counter += 1
                else:
                    out_file.write(line)
        return 'Yes'
    else:
        return 'No'
