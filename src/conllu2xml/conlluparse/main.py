import argparse
import os
import setting_conllu
import combine_all
import clean_all
 
def main(input_dir, output_dir):
    # Iterate over all the .conllu files in the input directory
    for filename in os.listdir(input_dir):
        # Skip the file if clit's not a .conllu file
        name, ext = os.path.splitext(filename)
        if ext != '.conllu':
            continue

        # Construct the input and output file paths for the current file  
        input_file = os.path.join(input_dir, filename)
        output_filename = name + '_Modified' + ext
        output_file = os.path.join(output_dir, output_filename)

        # Read the file and apply the setting_conllu functions 
        lines = setting_conllu.read_conllu(input_file)
        lines = setting_conllu.del_id(lines)
        lines = setting_conllu.del_hashlines(lines)
        lines = setting_conllu.set_id(lines)
        
        # Write the output after setting_conllu functions
        setting_conllu.write_conllu(output_file, lines)
        
        # Call combine_all to combine conllu files in the input directory 
        combine_all.conllu(input_dir, output_file)

        # Check duplicates after combining all files in the input directory 
        duplicates = combine_all.dupl_check(output_file)
        print('Duplicates found:', duplicates)
        
        # Read the combined file and apply cleaning functions 
        lines = setting_conllu.read_conllu(output_file)
        lines = clean_all.change_upos(lines)        
        lines = setting_conllu.change_divider(lines)
        lines = clean_all.change_feats(lines)
        lines = clean_all.check_abbr(lines)
        lines = clean_all.del_gaps(lines)
        lines = clean_all.swap_values4verb(lines)
        lines = clean_all.change_pos4participle(lines)
        lines = clean_all.check_multitoken(lines)
        lines = clean_all.del_multitoken(lines)
        # OPTIONAL:
        lines = clean_all.check_part_de(lines) # for German
        lines = clean_all.check_part_es(lines) # for Spanish
        lines = clean_all.check_part_ru(lines) # for Russian
        lines = clean_all.check_extra_ru(lines) # for Russian
        lines = clean_all.del_gaps2(lines)  
        lines = clean_all.change_feats2(lines)  
        lines = clean_all.del_gaps3(lines)

        # Write the final cleaned file 
        setting_conllu.write_conllu(output_file, lines)

if __name__ == '__main__':
    # Construct the argument parser and parse the arguments 
    # Example of usage: python main.py -i input -o output
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input_dir', required=True, help='Path to the input directory')
    ap.add_argument('-o', '--output_dir', required=True, help='Path to the output directory')
    args = vars(ap.parse_args())

    # Call the main function 
    main(args['input_dir'], args['output_dir'])