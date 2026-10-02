"""
SPDX-FileCopyrightText: 2016-2024 Unisoc (Shanghai) Technologies Co., Ltd
SPDX-License-Identifier: LicenseRef-Unisoc-General-1.0
"""
"""
UNISOC: Transaction caller tracer
AR.001689.008124.045434
Generate transaction caller trace file with tag
"""
import datetime
import os
import sys

def process_line(line, offset):
    parts = line.split(" ")
    if parts[0].isdigit():
        nanoseconds = int(parts[0]) + offset
        start = datetime.datetime(year=1970, month=1, day=1)
        formatted_timestamp = start + datetime.timedelta(microseconds=(nanoseconds // 1000))
        return '\n' + ' '.join([str(formatted_timestamp)] + parts[1:])
    else:
        return line

def copy_file_with_offset(input_file, output_file, offset):
    with open(input_file, 'r') as in_file, open(output_file, 'w') as out_file:
        for line in in_file:
            processed_line = process_line(line, offset)
            out_file.write(processed_line)

def fetch_offset(input_file):
    with open(input_file, 'r') as file:
        first_line = file.readline().replace('\n', '')
        parts = first_line.split('=')
        if parts[1].isdigit():
            return int(parts[1])

def get_tct_files(directory):
    txt_files = []
    for filename in os.listdir(directory):
        if 'tct-' in filename and filename.endswith('.txt'):
            txt_files.append(filename)
    return txt_files

def parse_file(input_file):
    offset = fetch_offset(input_file)
    copy_file_with_offset(input_file, 'parsed-' + input_file, offset)



if len(sys.argv) == 1:
    directory = os.getcwd()
else:
    directory = sys.argv[1]

tct_files = get_tct_files(directory)

for input_file in tct_files:
    parse_file(input_file)