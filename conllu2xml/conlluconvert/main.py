import argparse
import os
from conllu2xml import conllu2xml
from xml2trf import xml2trf, parse_trf


def main(input_dir, intermediate_dir, output_dir):
    # Convert .conllu files to .xml files
    conllu2xml(input_dir, intermediate_dir)

    # Iterate over all the .xml files in the intermediate directory
    for filename in os.listdir(intermediate_dir):
        if not filename.endswith('.xml'):
            continue

        # Construct the full file path
        xml_file_path = os.path.join(intermediate_dir, filename)

        # Convert the .xml file to .trf file
        trf_file_path = xml2trf(xml_file_path)

        # Parse the .trf file and save the modified version
        modified_trf = parse_trf(open(trf_file_path).read())
        output_filename = filename.replace('.xml', '.trf')
        output_file_path = os.path.join(output_dir, output_filename)
        with open(output_file_path, 'w') as f:
            f.write(modified_trf)

        # Remove the intermediate .xml file
        os.remove(xml_file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', help='Input directory containing .conllu files')
    parser.add_argument('intermediate_dir', help='Intermediate directory for .xml files')
    parser.add_argument('output_dir', help='Output directory for .trf files')
    args = parser.parse_args()

    main(args.input_dir, args.intermediate_dir, args.output_dir)
