import argparse
import html
import os
import re
from xml.dom import minidom
from nltk.tokenize import sent_tokenize


def conllu2xml(input_dir, output_dir):
    # Iterate over all the .conllu files in the input directory
    for filename in os.listdir(input_dir):
        if not filename.endswith('.conllu'):
            continue
        
        # Construct the full file path
        file_path = os.path.join(input_dir, filename)

        # Open the file in read mode
        with open(file_path, 'r') as f:
            conllu_string = f.read()
            
            # Split the conllu string into a list of lines
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

              # Create the qitext element and set the id attribute
              qitext = xmldoc.createElement('qitext')
              qitext.setAttribute('id', str(id))

              # Create the plain element and add it to the qitext element
              plain = xmldoc.createElement('plain')
              plain_text = ' '.join([token['form'] for token in sentence])
              plain.appendChild(xmldoc.createTextNode(plain_text))
              qitext.appendChild(plain)

              # Set the l attribute of the qitext element to the length of the plain text
              qitext.setAttribute('l', str(len(plain_text)))

              # Parse the plain text into a list of sentences using the nlp function
              sentences = sent_tokenize(plain_text, language='french')

              # Iterate over the list of tokens and create the qitoken elements
              start = 0
              sentence_counter = 0    

              for j, token in enumerate(sentence):
                qitoken = xmldoc.createElement('qitoken')
                qitoken_text = f"{token['form']} {token['upos']}:{token['feats']}"
                qitoken_text = re.sub(r'&(?!amp;|lt;|gt;)', '&amp;', qitoken_text)
                qitoken_text = re.sub(r'<http', '&lt;http', qitoken_text)
                qitoken_text = re.sub(r'<', '&lt;', qitoken_text)
                qitoken_text = re.sub(r'>', '&gt;', qitoken_text)
                qitoken_text = re.sub(r'<(?=[a-zA-Z])', '&lt;', qitoken_text)
                qitoken_text = re.sub(r'>(?=[a-zA-Z])', '&gt;', qitoken_text)
                qitoken.appendChild(xmldoc.createTextNode(qitoken_text))
                qitoken.setAttribute('start', str(start))
                start += len(token['form']) + 1
                qitoken.setAttribute('end', str(start - 1))
                qitoken.setAttribute('sentence', str(sentence_counter + 1))
                qitext.appendChild(qitoken)
                
                
                # Increment the sentence counter if the current token is the last in a sentence
                if sentence_counter < len(sentences) and token['form'] == sentences[sentence_counter][-1]:
                  sentence_counter += 1

              root.appendChild(qitext)

              # Increment the id counter
              id += 1

            # Construct the output file path
            output_filename = filename.replace('.conllu', '.xml')
            output_path = os.path.join(output_dir, output_filename)
        
            # Write the xml document to the output file
            with open(output_path, 'w') as f:
              f.write(html.unescape(xmldoc.toprettyxml()))

            # Print the number of xml elements created
            print(f'{len(root.getElementsByTagName("qitext"))} qitext elements created')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', help='Input directory containing .conllu files')
    parser.add_argument('output_dir', help='Output directory for .xml files')
    args = parser.parse_args()

    conllu2xml(args.input_dir, args.output_dir)
