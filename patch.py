import os
import math
from functions import *

def create_patch_files(patch_folder, ratio_value, scaling_factor, visual_fixes):

    visual_fixesa = visual_fixes[0]
    visual_fixesb = visual_fixes[1]
    visual_fixesc = visual_fixes[2]
    scaling_factor = float(scaling_factor)
    ratio_value = float(ratio_value)
    print(f"The scaling factor is {scaling_factor}.")
    hex_value = make_hex(ratio_value, 0)
    hex_value2 = make_hex(ratio_value, 3)
    special_hex1, special_hex2 = make_specials(ratio_value)
    version_variables = ["1.0.0", "1.2.0", "1.3.0"]
    for version_variable in version_variables:
        file_name = f"main-{version_variable}.pchtxt"
        file_path = os.path.join(patch_folder, file_name)

        if version_variable == "1.0.0":
            nsobidid = "3CA12DFAAF9C82DA064D1698DF79CDA1"
            replacement_value = "009CF340"
            replacement2_value = "00A63D5C"
            visual_fix = visual_fixesa
            
        if version_variable == "1.2.0":
            nsobidid = "F5DCCDDB37E97724EBDBCCCDBEB965FF"
            replacement_value = "00A12A50"
            replacement2_value = "00AA7494"
            visual_fix = visual_fixesc

        if version_variable == "1.3.0":
            nsobidid = "B424BE150A8E7D78701CBE7A439D9EBF"
            visual_fix = visual_fixesb
            patch_stuff = f'''0096816c {special_hex1}
00968170 {special_hex2}
0073de88 1F2003D5'''
        else:
            patch_stuff = f'''{replacement_value} {hex_value}
{replacement2_value} {hex_value2}'''

        patch_content = f'''@nsobid-{nsobidid}

@flag print_values
@flag offset_shift 0x100

@enabled
{patch_stuff}
@disabled

{visual_fix}

// Generated using SMO-AAR by Fayaz (github.com/fayaz12g/smo-aar)'''
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as patch_file:
            patch_file.write(patch_content)
        print(f"Patch file created: {file_path}")
