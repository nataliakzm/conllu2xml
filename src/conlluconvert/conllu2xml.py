import argparse
import os
import re
from nltk.tokenize import sent_tokenize
from xml.dom import minidom

def conllu2xml(input_dir: str, output_dir: str):
    for filename in os.listdir(input_dir):
        if not filename.endswith('.conllu'):
            continue

        # Construct the full file path for the input file and open it in read mode 
        file_path = os.path.join(input_dir, filename)
        with open(file_path, 'r') as f:
            conllu_string = f.read()

            # Split the conllu string into a list of lines and remove the empty lines at the end of the file 
            conllu_lines = conllu_string.split('\n')

            # Create the xml document and root element 
            xmldoc = minidom.Document()
            root = xmldoc.createElement('trf')
            xmldoc.appendChild(root)

            # Iterate over the list of lines and extract the values from each line 
            conllu_parsed = []
            sentence = []
            id = 1

            for line in conllu_lines:
                if line.startswith('#'):
                    continue
                elif line == '':
                    conllu_parsed.append(sentence)
                    sentence = []
                else:
                    columns = line.split('\t')
                    form = columns[1]
                    upos = columns[3]
                    feats = columns[5]
                    token = {'form': form, 'upos': upos, 'feats': feats}
                    sentence.append(token)            

            # Iterate over the list of sentences and create the xml elements 
            for i, sentence in enumerate(conllu_parsed):
              
              # Create the text element and set the id attribute
              text = xmldoc.createElement('text')
              text.setAttribute('id', str(id))

              # Create the plain element and add it to the text element
              plain = xmldoc.createElement('plain')
              plain_text = ' '.join([token['form'] for token in sentence])
              plain.appendChild(xmldoc.createTextNode(plain_text))
              text.appendChild(plain)

              # Set the l attribute of the text element to the length of the plain text 
              text.setAttribute('l', str(len(plain_text)))

              # Parse the plain text into a list of sentences using the nlp function sent_tokenize from the nltk library 
              sentences = sent_tokenize(plain_text, language='french')

              # Iterate over the list of tokens and create the token elements 
              start = 0
              sentence_counter = 0    

              for j, token in enumerate(sentence):
                token = xmldoc.createElement('token')
                token_text = f"{token['form']} {token['upos']}:{token['feats']}"
                token_text = re.sub(r'&(?!amp;|lt;|gt;)', '&amp;', token_text)
                token_text = re.sub(r'<http', '&lt;http', token_text)
                token_text = re.sub(r'<', '&lt;', token_text)
                token_text = re.sub(r'>', '&gt;', token_text)
                token_text = re.sub(r'<(?=[a-zA-Z])', '&lt;', token_text)
                token_text = re.sub(r'>(?=[a-zA-Z])', '&gt;', token_text)
                token.appendChild(xmldoc.createTextNode(token_text))
                token.setAttribute('start', str(start))
                start += len(token['form']) + 1
                token.setAttribute('end', str(start - 1))
                token.setAttribute('sentence', str(sentence_counter + 1))
                text.appendChild(token)

                #Increment the sentence counter if the current token is the last in a sentence 
                if sentence_counter < len(sentences) and token['form'] == sentences[sentence_counter][-1]:
                    sentence_counter += 1

              root.appendChild(text)
              id += 1

        # Construct the output file path and name 
        output_filename = filename.replace('.conllu', '.xml')
        output_path = os.path.join(args.output_dir, output_filename)
        with open(output_path, 'w') as f:
            f.write(xmldoc.toprettyxml(indent="  "))

if __name__ == '__main__':
    conllu2xml(args)
