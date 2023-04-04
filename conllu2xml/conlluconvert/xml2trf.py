import os
import re
from lxml import etree

def xml2trf(xml_file):
    # Get the TRF file name from the XML file name
    trf_file = os.path.splitext(xml_file)[0] + ".trf"

    # Open the XML file and ignore errors
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(xml_file, parser=parser)
    root = tree.getroot()

    # Open the TRF file
    with open(trf_file, "w", encoding="utf-8") as trf:

        # Write the TRF header
        trf.write('<?xml version=\'1.0\' encoding=\'UTF8\' ?>\n')
        trf.write("<format>3.0</format>\n")

        # Initialize the ID counter
        id_counter = 1

        # Get the qitext elements
        qitext_elements = root.findall("./qitext")

        # Iterate over the qitext elements
        for qitext_element in qitext_elements:
            # Get the text for the qitext element
            text_element = qitext_element.find("plain")
            if text_element is not None:
                text = text_element.text
            else:
                text = ""

            # Get the length of the text
            length = len(text) if text is not None else 0

            # Write the qitext element
            trf.write("<qitext id='{}' l='{}'>\n".format(id_counter, length))
            trf.write("<plain>{}</plain>\n".format(text))

            # Get the qitoken elements
            qitoken_elements = qitext_element.findall("qitoken")

            for token in qitoken_elements:
                start = token.attrib['start']
                end = token.attrib['end']
                sentence = token.attrib.get('sentence', '1')
                trf.write("<qitoken start='{}' end='{}' sentence='{}'>{} WORD {}</qitoken>\n".format(start, end, sentence, token.text, token.attrib.get('class', 'OTHER')))

            # Write the end of the qitext element
            trf.write("</qitext>\n")

            # Increment the ID counter
            id_counter += 1

    # Return the path to the TRF file
    return trf_file


def parse_trf(trf_file):
    # Use regular expressions to find all instances of "qitoken" tags and remove ":_" from the 2nd argument
    trf_file = re.sub(r'qitoken(.*?) (\w+):_', r'qitoken\1 \2', trf_file)

    # Return the modified TRF file
    return trf_file


if __name__ == '__main__':
    # Get the XML file name from the command line argument
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('xml_file', help='Input XML file name')
    args = parser.parse_args()

    # Convert the XML file to TRF format
    trf_file = xml2trf(args.xml_file)

    # Parse the TRF file and save the modified version
    modified_trf = parse_trf(open(trf_file).read())
    with open(trf_file, 'w') as f:
        f.write(modified_trf)