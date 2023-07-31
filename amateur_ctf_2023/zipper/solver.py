#!/usr/bin/python3
import os
import base64
import zipfile

FLAGS_DIR = './targetdir/flag'

def unzip_it():
    with zipfile.ZipFile("flag.zip","r") as zip_ref:
        
        print('Comments:')
        for zip_name in zip_ref.namelist():
            if zip_ref.getinfo(zip_name).comment:
                print(f'  {zip_ref.getinfo(zip_name).comment}')
        
        print('Content with word Part in them:')
        zipinfos = zip_ref.infolist()
        for zipinfo in zipinfos:
            # print(zipinfo)
            zipinfo.filename = './tmp_flag_file'
            zip_ref.extract(zipinfo)
            with open(zipinfo.filename, 'r') as tmp_zip_file:
                for line in tmp_zip_file.readlines():
                    if 'Part' in line:
                        print(f'  {line}')
            os.remove(zipinfo.filename)


def read_them():
    ''' Reads the files from dir, not useful here... '''
    print()
    contents = []
    for files in os.listdir(FLAGS_DIR):
        path = os.path.join(FLAGS_DIR,files)
        with open(path,'r') as tmp_file_h:
            contents.append(tmp_file_h.readlines())
    return contents

def decode_them(contents):
    ''' Decodes base64 , not useful here ... '''
    decoded = []
    for content in contents:
        try:
            merged = ''.join(content)
            base64_bytes = merged.encode("ascii")
            string_bytes = base64.b64decode(base64_bytes)
            contents.append(string_bytes.decode("ascii"))
        except:
            print(merged)
    return decoded

print('Run strings or exiftool on zip file to get 1st part')
unzip_it()
print('Also, flag is missing an _ after the letter 4 ...')

# Part 1: amateursCTF{z1PP3d_
# Part 2: in5id3_4
# Part 3: laY3r_0f
# Part 4: _Zips}
