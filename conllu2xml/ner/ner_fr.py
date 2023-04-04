#!/usr/bin/env python3

"""
This script reads a .conllu file, processes it with the French Stanza NER pipeline,
and outputs a TSV file containing extracted named entities.
"""

import os
import re
import stanza

stanza.download('fr') # FRENCH
nlp = stanza.Pipeline('fr', processors='tokenize,ner')

def extract_words(lines):
    output_lines = []
    for line in lines:
        if line.startswith("# id = "):
            output_lines.append(line)
        if line.startswith("#") or line.strip() == "":
            continue
        columns = line.strip().split("\t")
        if len(columns) < 4:
            continue
        word = columns[1]
        is_written = False
        if columns[3] != "PROPER_NOUN":
            output_lines.append(word + "\tO\t" + columns[3] + "\n")
            is_written = True
        else:
            doc = nlp(word)
            for sent in doc.sentences:
                for ent in sent.ents:
                    if ent.type in ["PER", "ORG", "LOC"]:
                        output_lines.append(word + "\t" + ent.type  + "\t" +  columns[3] + "\n")
                        is_written = True
        if not is_written:
            output_lines.append(word + "\t???\t" + columns[3] + "\n")
    return output_lines


def eliminate_lines(lines):
    eliminated = []
    output_lines = []
    id = None
    for line in lines:
        if line.startswith("# id = "):
            id = int(line.strip().split(" ")[-1])
            output_lines.append(line)
            continue
        if line.strip().split("\t")[1] != "???":
            output_lines.append(line)
        else:
            if id:
                eliminated.append(id)
            else:
                output_lines.append(line)
    return output_lines, eliminated


def delete_hash_id_lines(lines):
    output_lines = []
    for line in lines:
        if not line.startswith("# id = "):
            output_lines.append(line)
        else:
            output_lines.append("\n")
    return output_lines

def change_tags(lines):
    for i in range(len(lines)):
        lines[i] = re.sub(r'\tPER\t', '\tPERSON\t', lines[i])
        lines[i] = re.sub(r'\tLOC\t', '\tLOCATION\t', lines[i])
        lines[i] = re.sub(r'\tORG\t', '\tORGANIZATION\t', lines[i])
    return lines

def person(lines):
    for i in range(len(lines)):
        if lines[i] == "\n" or lines[i - 1] == "\n" or (i + 1 < len(lines) and lines[i + 1] == "\n"):
            continue
        elif lines[i].split('\t')[1] == 'PERSON' and (i == 0 or lines[i - 1].split('\t')[1] != 'PERSON') and (i + 1) < len(lines) and lines[i + 1].split('\t')[1] == 'PERSON':
            lines[i] = re.sub(r'PERSON', 'PERSON:START', lines[i])
        elif (lines[i].split('\t')[1] == 'PERSON' or lines[i].split('\t')[1] == 'PERSON:START') and (i - 1) >= 0 and (lines[i - 1].split('\t')[1] == 'PERSON' or lines[i - 1].split('\t')[1] == 'PERSON:START') and (i + 1) < len(lines) and lines[i + 1].split('\t')[1] != 'PERSON':
            lines[i] = re.sub(r'PERSON', 'PERSON:END', lines[i])

    empty_start = 1
    while empty_start > 0:
        empty_start = 0
        for i in range(len(lines)):
            if lines[i] == "\n" or (i + 1 < len(lines) and lines[i + 1] == "\n"):
                continue
            elif lines[i].split('\t')[1] == 'PERSON' and (i == 0 or lines[i - 1] == "\n") and (i + 1) < len(lines) and lines[i + 1].split('\t')[1] == 'PERSON':
                lines[i] = re.sub(r'PERSON', 'PERSON:START', lines[i])
                empty_start += 1

    empty_end = 1
    while empty_end > 0:
        empty_end = 0
        for i in range(len(lines)):
            if lines[i] == "\n" or lines[i - 1] == "\n":
                continue
            elif (lines[i].split('\t')[1] == 'PERSON' or lines[i].split('\t')[1] == 'PERSON:START') and (i - 1) >= 0 and (lines[i - 1].split('\t')[1] == 'PERSON' or lines[i - 1].split('\t')[1] == 'PERSON:START') and (i + 1 < len(lines) and lines[i + 1] == "\n"):
                lines[i] = re.sub(r'PERSON', 'PERSON:END', lines[i])
                empty_end += 1

    changes = 1
    while changes > 0:
        changes = 0
        for i in range(len(lines)):
            if lines[i] == "\n" or lines[i - 1] == "\n" or (i + 1 < len(lines) and lines[i + 1] == "\n"):
                continue
            elif (lines[i].split('\t')[1] == 'PERSON:START') and (i - 1) >= 0 and (lines[i - 1].split('\t')[1] == 'PERSON:START') and (i + 1) < len(lines) and (lines[i + 1].split('\t')[1] == 'PERSON:END' or lines[i + 1].split('\t')[1] == 'PERSON:INTERMEDIATE'):
                lines[i] = re.sub(r'PERSON:START', 'PERSON:INTERMEDIATE', lines[i])
                changes += 1

    return lines

def location(lines):
    for i in range(len(lines)):
        if lines[i] == "\n" or lines[i-1] == "\n" or (i+1 < len(lines) and lines[i+1] == "\n"):
            continue
        elif lines[i].split('\t')[1] == 'LOCATION' and (i == 0 or lines[i-1].split('\t')[1] != 'LOCATION') and (i + 1) < len(lines) and lines[i + 1].split('\t')[1] == 'LOCATION':
            lines[i] = re.sub(r'LOCATION', 'LOCATION:START', lines[i])
        elif (lines[i].split('\t')[1] == 'LOCATION' or lines[i].split('\t')[1] == 'LOCATION:START') and (i - 1) >= 0 and (lines[i-1].split('\t')[1] == 'LOCATION' or lines[i-1].split('\t')[1] == 'LOCATION:START') and (i + 1) < len(lines) and lines[i + 1].split('\t')[1] != 'LOCATION':
            lines[i] = re.sub(r'LOCATION', 'LOCATION:END', lines[i])
    
    empty_start = 1
    while empty_start > 0:
        empty_start = 0
        for i in range(len(lines)):
            if lines[i] == "\n" or (i+1 < len(lines) and lines[i+1] == "\n"):
                continue
            elif lines[i].split('\t')[1] == 'LOCATION' and (i == 0 or lines[i-1] == "\n") and (i + 1) < len(lines) and lines[i + 1].split('\t')[1] == 'LOCATION':
              lines[i] = re.sub(r'LOCATION', 'LOCATION:START', lines[i])
              empty_start += 1

    empty_end = 1
    while empty_end > 0:
        empty_end = 0
        for i in range(len(lines)):
            if lines[i] == "\n" or lines[i-1] == "\n":
              continue
            elif (lines[i].split('\t')[1] == 'LOCATION' or lines[i].split('\t')[1] == 'LOCATION:START') and (i - 1) >= 0 and (lines[i-1].split('\t')[1] == 'LOCATION' or lines[i-1].split('\t')[1] == 'LOCATION:START') and (i+1 < len(lines) and lines[i+1] == "\n"):
              lines[i] = re.sub(r'LOCATION', 'LOCATION:END', lines[i])
              empty_end += 1  
    
    changes = 1
    while changes > 0:
        changes = 0
        for i in range(len(lines)):
            if lines[i] == "\n" or lines[i-1] == "\n" or (i+1 < len(lines) and lines[i+1] == "\n"):
              continue
            elif (lines[i].split('\t')[1] == 'LOCATION:START') and (i - 1) >= 0 and (lines[i-1].split('\t')[1] == 'LOCATION:START') and (i + 1) < len(lines) and (lines[i + 1].split('\t')[1] == 'LOCATION:END' or lines[i + 1].split('\t')[1] == 'LOCATION:INTERMEDIATE'):
              lines[i] = re.sub(r'LOCATION:START', 'LOCATION:INTERMEDIATE', lines[i])
              changes += 1      

    return lines

def organization(lines):
    for i in range(len(lines)):
        if lines[i] == "\n" or lines[i-1] == "\n" or (i+1 < len(lines) and lines[i+1] == "\n"):
            continue
        elif lines[i].split('\t')[1] == 'ORGANIZATION' and (i == 0 or lines[i-1].split('\t')[1] != 'ORGANIZATION') and (i + 1) < len(lines) and lines[i + 1].split('\t')[1] == 'ORGANIZATION':
            lines[i] = re.sub(r'ORGANIZATION', 'ORGANIZATION:START', lines[i])
        elif (lines[i].split('\t')[1] == 'ORGANIZATION' or lines[i].split('\t')[1] == 'ORGANIZATION:START') and (i - 1) >= 0 and (lines[i-1].split('\t')[1] == 'ORGANIZATION' or lines[i-1].split('\t')[1] == 'ORGANIZATION:START') and (i + 1) < len(lines) and lines[i + 1].split('\t')[1] != 'ORGANIZATION':
            lines[i] = re.sub(r'ORGANIZATION', 'ORGANIZATION:END', lines[i])
    
    empty_start = 1
    while empty_start > 0:
        empty_start = 0
        for i in range(len(lines)):
            if lines[i] == "\n" or (i+1 < len(lines) and lines[i+1] == "\n"):
              continue
            elif lines[i].split('\t')[1] == 'ORGANIZATION' and (i == 0 or lines[i-1] == "\n") and (i + 1) < len(lines) and lines[i + 1].split('\t')[1] == 'ORGANIZATION':
              lines[i] = re.sub(r'ORGANIZATION', 'ORGANIZATION:START', lines[i])
              empty_start += 1

    empty_end = 1
    while empty_end > 0:
        empty_end = 0
        for i in range(len(lines)):
            if lines[i] == "\n" or lines[i-1] == "\n":
              continue
            elif (lines[i].split('\t')[1] == 'ORGANIZATION' or lines[i].split('\t')[1] == 'ORGANIZATION:START') and (i - 1) >= 0 and (lines[i-1].split('\t')[1] == 'ORGANIZATION' or lines[i-1].split('\t')[1] == 'ORGANIZATION:START') and (i+1 < len(lines) and lines[i+1] == "\n"):
              lines[i] = re.sub(r'ORGANIZATION', 'ORGANIZATION:END', lines[i])
              empty_end += 1 

    changes = 1
    while changes > 0:
        changes = 0
        for i in range(len(lines)):
            if lines[i] == "\n" or lines[i-1] == "\n" or (i+1 < len(lines) and lines[i+1] == "\n"):
              continue
            elif (lines[i].split('\t')[1] == 'ORGANIZATION:START') and (i - 1) >= 0 and (lines[i-1].split('\t')[1] == 'ORGANIZATION:START') and (i + 1) < len(lines) and (lines[i + 1].split('\t')[1] == 'ORGANIZATION:END' or lines[i + 1].split('\t')[1] == 'ORGANIZATION:INTERMEDIATE'):
              lines[i] = re.sub(r'ORGANIZATION:START', 'ORGANIZATION:INTERMEDIATE', lines[i])
              changes += 1

    return lines

def main():
    directory = os.path.abspath("/content/Input")
    odirectory = os.path.abspath("/content/Output")

    for file in os.listdir(directory):
        if file.endswith(".conllu"):
            input_file = os.path.join(directory, file)
            output_file = os.path.join(odirectory, file.replace(".conllu", "_NER.tsv"))

            with open(input_file, "r") as file:
                lines = file.readlines()

            output_lines = extract_words(lines)

            with open(output_file, "w") as outfile:
                outfile.writelines(output_lines)

    input_directory = os.path.abspath("/content/Output")
    output_directory = os.path.abspath("/content/Output/Output2")

    for file in os.listdir(input_directory):
        if file.endswith("_NER.tsv"):
            input_file = os.path.join(input_directory, file)
            output_file = os.path.join(output_directory, file)

            with open(input_file, "r") as file:
                lines = file.readlines()

            output_lines, eliminated = eliminate_lines(lines)
            print(f"{len(eliminated)} # id = lines were eliminated from file '{os.path.basename(input_file)}': {eliminated}")

            output_lines = delete_hash_id_lines(output_lines)
            print(f"All lines starting with '# id = ' have been eliminated from file '{os.path.basename(input_file)}'.")

            with open(output_file, "w") as outfile:
                outfile.writelines(output_lines)

    input_dir = "/content/Output/Output3"
    output_dir = "/content/Output/Output4"

    for file in os.listdir(input_dir):
        if file.endswith(".tsv"):
            filename = file.replace(".tsv", ".tsv")
            with open(os.path.join(input_dir, file), "r", encoding="utf-8") as f:
                lines = f.readlines()

            lines = change_tags(lines)
            lines = person(lines)
            lines = location(lines)
            lines = organization(lines)

            with open(os.path.join(output_dir, filename), 'w') as f:
                f.writelines(lines)

    print("All files have been processed successfully.")

if __name__ == "__main__":
    main()