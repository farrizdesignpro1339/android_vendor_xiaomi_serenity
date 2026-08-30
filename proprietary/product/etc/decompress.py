#!/usr/bin/python
# coding: utf-8

# Test case:
#   1. Python 2.7.6 and 3.7.1 test pass on ubuntu.
#   2. Python 2.7.1 test pass on windows.

import os,fnmatch
import struct
import mmap
import sys
import gzip
import zlib
import platform
import re
from ctypes import *
# for generate_elfhdr
# typedef struct elf32_hdr{
#   unsigned char e_ident[EI_NIDENT];
#   Elf32_Half    e_type;
#   Elf32_Half    e_machine;
#   Elf32_Word    e_version;
#   Elf32_Addr    e_entry;                  /* Entry point */
#   Elf32_Off     e_phoff;
#   Elf32_Off     e_shoff;
#   Elf32_Word    e_flags;
#   Elf32_Half    e_ehsize;
#   Elf32_Half    e_phentsize;
#   Elf32_Half    e_phnum;
#   Elf32_Half    e_shentsize;
#   Elf32_Half    e_shnum;
#   Elf32_Half    e_shstrndx;
# } Elf32_Ehdr;

# typedef struct elf64_hdr{
#   unsigned char e_ident[EI_NIDENT];       /* ELF "magic number" */
#   Elf64_Half    e_type;
#   Elf64_Half    e_machine;
#   Elf64_Word    e_version;
#   Elf64_Addr    e_entry;                  /* Entry point virtual address */
#   Elf64_Off     e_phoff;                  /* Program header table file offset */
#   Elf64_Off     e_shoff;                  /* Section header table file offset */
#   Elf64_Word    e_flags;
#   Elf64_Half    e_ehsize;
#   Elf64_Half    e_phentsize;
#   Elf64_Half    e_phnum;
#   Elf64_Half    e_shentsize;
#   Elf64_Half    e_shnum;
#   Elf64_Half    e_shstrndx;
# } Elf64_Ehdr;

# typedef struct elf32_phdr{
#   Elf32_Word    p_type;
#   Elf32_Off     p_offset;
#   Elf32_Addr    p_vaddr;
#   Elf32_Addr    p_paddr;
#   Elf32_Word    p_filesz;
#   Elf32_Word    p_memsz;
#   Elf32_Word    p_flags;
#   Elf32_Word    p_align;
# } Elf32_Phdr;

# typedef struct elf64_phdr {
#   Elf64_Word  p_type;
#   Elf64_Word p_flags;
#   Elf64_Off p_offset;           /* Segment file offset */
#   Elf64_Addr p_vaddr;           /* Segment virtual address */
#   Elf64_Addr p_paddr;           /* Segment physical address */
#   Elf64_Xword p_filesz;         /* Segment size in file */
#   Elf64_Xword p_memsz;          /* Segment size in memory */
#   Elf64_Xword p_align;          /* Segment alignment, file & memory */
# } Elf64_Phdr;

# /* 32-bit ELF base types. */
# typedef __u32   Elf32_Addr;
# typedef __u16   Elf32_Half;
# typedef __u32   Elf32_Off;
# typedef __s32   Elf32_Sword;
# typedef __u32   Elf32_Word;

# /* 64-bit ELF base types. */
# typedef __u64   Elf64_Addr;
# typedef __u16   Elf64_Half;
# typedef __s16   Elf64_SHalf;
# typedef __u64   Elf64_Off;
# typedef __s32   Elf64_Sword;
# typedef __u32   Elf64_Word;
# typedef __u64   Elf64_Xword;
# typedef __s64   Elf64_Sxword;



ELFMAG = "\177ELF"
SELFMAG = 4
ELFCLASS32 = 1
ELFCLASS64 = 2
ELFDATA2MSB = 2
ELFDATA2LSB = 1
EV_CURRENT = 1
ELF_OSABI = 0

EI_CLASS = 4
EI_DATA = 5
EI_VERSION = 6
EI_OSABI = 7
EI_PAD = 8
EI_NIDENT = 16

ET_CORE = 4

EM_ARM64 = 0xb7
EM_ARM = 0x28

ELF_CORE_EFLAGS = 0

PT_LOAD = 1
PT_NOTE = 4

PF_R = 0x4
PF_W = 0x2
PF_X = 0x1



class ELE32_HEADER(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('e_ident0',    c_char * 4),
        ('e_ident1',    c_uint8),
        ('e_ident2',    c_uint8),
        ('e_ident3',    c_uint8),
        ('e_ident4',    c_uint8),
        ('e_ident5',    c_uint64),
        ('e_type',      c_uint16),
        ('e_machine',   c_uint16),
        ('e_version',   c_uint32),
        ('e_entry',     c_uint32),
        ('e_phoff',     c_uint32),
        ('e_shoff',     c_uint32),
        ('e_flags',     c_uint32),
        ('e_ehsize',    c_uint16),
        ('e_phentsize', c_uint16),
        ('e_phnum',     c_uint16),
        ('e_shentsize', c_uint16),
        ('e_shnum',     c_uint16),
        ('e_shstrndx',  c_uint16),
    ]
    def encode(self):
        return string_at(addressof(self), sizeof(self))
    def decode(self, data):
        memmove(addressof(self), data, sizeof(self))
        return len(data)

class ELE32_P_HEADER(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('p_type',      c_uint32),
        ('p_offset',    c_uint32),
        ('p_vaddr',     c_uint32),
        ('p_paddr',     c_uint32),
        ('p_filesz',    c_uint32),
        ('p_memsz',     c_uint32),
        ('p_flags',     c_uint32),
        ('p_align',     c_uint32),
    ]
    def encode(self):
        return string_at(addressof(self), sizeof(self))
    def decode(self, data):
        memmove(addressof(self), data, sizeof(self))
        return len(data)

class ELE64_HEADER(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('e_ident0',    c_char * 4),
        ('e_ident1',    c_uint8),
        ('e_ident2',    c_uint8),
        ('e_ident3',    c_uint8),
        ('e_ident4',    c_uint8),
        ('e_ident5',    c_uint64),
        ('e_type',      c_uint16),
        ('e_machine',   c_uint16),
        ('e_version',   c_uint32),
        ('e_entry',     c_uint64),
        ('e_phoff',     c_uint64),
        ('e_shoff',     c_uint64),
        ('e_flags',     c_uint32),
        ('e_ehsize',    c_uint16),
        ('e_phentsize', c_uint16),
        ('e_phnum',     c_uint16),
        ('e_shentsize', c_uint16),
        ('e_shnum',     c_uint16),
        ('e_shstrndx',  c_uint16),
    ]
    def encode(self):
        return string_at(addressof(self), sizeof(self))
    def decode(self, data):
        memmove(addressof(self), data, sizeof(self))
        return len(data)

class ELE64_P_HEADER(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('p_type',      c_uint32),
        ('p_flags',     c_uint32),
        ('p_offset',    c_uint64),
        ('p_vaddr',     c_uint64),
        ('p_paddr',     c_uint64),
        ('p_filesz',    c_uint64),
        ('p_memsz',     c_uint64),
        ('p_align',     c_uint64),
    ]
    def encode(self):
        return string_at(addressof(self), sizeof(self))
    def decode(self, data):
        memmove(addressof(self), data, sizeof(self))
        return len(data)

# struct sysdump_mem {
#        unsigned long paddr;
#        unsigned long vaddr;
#        unsigned long soff;
#        unsigned long size;
#        unsigned long type;
# };

class Minidump_Mem_Arm32(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('paddr',       c_uint32),
        ('vaddr',       c_uint32),
        ('soff',        c_uint32),
        ('size',        c_uint32),
        ('type',        c_uint32),
    ]
    def encode(self):
        return string_at(addressof(self), sizeof(self))
    def decode(self, data):
        memmove(addressof(self), data, sizeof(self))
        return len(data)


class Minidump_Mem_Arm64(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('paddr',       c_uint64),
        ('vaddr',       c_uint64),
        ('soff',        c_uint64),
        ('size',        c_uint64),
        ('type',        c_uint64),
    ]
    def encode(self):
        return string_at(addressof(self), sizeof(self))
    def decode(self, data):
        memmove(addressof(self), data, sizeof(self))
        return len(data)


MINIDUMP_MEM_MAX = 251
DATA_OFFSET = 0x2000


#arm32
ELF32_HEADER_SIZE = 54
ELF32_P_HEADER_SIZE = 32
MINIDUMP_MEM32_SIZE = 20

#arm64
ELF64_HEADER_SIZE = 64
ELF64_P_HEADER_SIZE = 56
MINIDUMP_MEM64_SIZE = 40

#for generate_elfhdr end



# Reference kernel/printk/printk.c
PRINKT_LOG_STRUCT_FORMAT      = '<Q3H3BI'
PRINKT_LOG_STRUCT_SIZE = 20
TASK_COMM_LEN          = 16

DUMP_FILE = 'minidump'
KMSG_FILE = 'last_kmsg.log'
COMPRESSED_INFO = 'compress_record_file'
bootloader_version = 0
MSEC = 1000000000

dump_dir = os.getcwd()


def uncompress_zlib_files(dirname):
    offset = 0
    dump_files=fnmatch.filter(os.listdir(dirname), '*.zlib')
    compressed_info_files=open(os.path.join(dirname, COMPRESSED_INFO))
    for dump_file in dump_files:
        fd = open(os.path.join(dirname, dump_file), 'rb')
        dump_file_out = open(os.path.join(dirname, dump_file).rsplit('.',1)[0],"wb")
        name_list1 = dump_file.rsplit('.', 1)[0]
        compressed_info_files.seek(0)
        for line in compressed_info_files:
            line_list1 = line.split(':')[0]
            if name_list1 == line_list1:
                compressed_len_list = line_list1 = line.split(':')[1].split(' ')
                for compressed_len in compressed_len_list:
                    length = int(compressed_len)
                    if length == -1:
                        offset = 0
                        break
                    compress_block = fd.read(length)
                    uncompress_block = zlib.decompress(compress_block, 15)
                    dump_file_out.write(uncompress_block)
                    offset += length
                    fd.seek(offset)
                break
        dump_file_out.close()
        fd.close()
        os.remove(os.path.join(dirname, dump_file))

    compressed_info_files.close()


def uncompress_gzip_files(dirname):
    dump_files = fnmatch.filter(os.listdir(dirname), '*.gz')
    for dump_file in dump_files:
        out_dump_file = dump_file[:-3]
        f = gzip.open(os.path.join(dirname, dump_file), 'rb')
        f_out=open(os.path.join(dirname, out_dump_file),"wb")
        file_content = f.read()
        f_out.write(file_content)
        f.close()
        f_out.close()
        os.remove(os.path.join(dirname, dump_file))



def merge_file(dirname):
    dump_files = fnmatch.filter(os.listdir(dirname), '*_minidump_*')
    if len(dump_files) == 0:
        print('Don\'t exist dump file!!!')
        return
    dump_files.sort(key = lambda x: int(x.split('_',1)[0]))
    with open(os.path.join(dirname, DUMP_FILE),'wb') as outfile:
        for dump_file in dump_files:
            for line in open(os.path.join(dirname, dump_file), 'rb'):
                outfile.write(line)



def create_new_file(path, size):
    with open(path, 'wb') as f:
        f.seek(int(size)-1)
        f.write(b'\x00')
        f.close()

def Generate_elf32_files(dirname):
    file_name = '000_minidump_elfhdr'
    file_size = '8192'
    file_path = os.path.join(dirname, file_name)
    create_new_file(file_path, file_size)
    fd = open(os.path.join(dirname, file_name), 'rb+')
    fd.seek(0)
    elfhdr_offset = 0
    elf32_h = ELE32_HEADER()
    elf32_nh = ELE32_HEADER()

    elf32_h.e_ident0 = ELFMAG.encode()
    elf32_h.e_ident1 = ELFCLASS32
    elf32_h.e_ident2 = ELFDATA2LSB
    elf32_h.e_ident3 = EV_CURRENT
    elf32_h.e_ident4 = ELF_OSABI
    elf32_h.e_ident5 = 0
    elf32_h.e_type = ET_CORE
    elf32_h.e_machine = EM_ARM
    elf32_h.e_version = EV_CURRENT
    elf32_h.e_entry = 0
    elf32_h.e_phoff = ELF32_HEADER_SIZE
    elf32_h.e_shoff = 0;
    elf32_h.e_flags = ELF_CORE_EFLAGS
    elf32_h.e_ehsize = ELF32_HEADER_SIZE
    print(elf32_h.e_ehsize)
    elf32_h.e_phentsize = ELF32_P_HEADER_SIZE
    elf32_h.e_phnum = 0
    elf32_h.e_shentsize = 0;
    elf32_h.e_shnum = 0;
    elf32_h.e_shstrndx = 0;

    fd.write(elf32_h)
    elfhdr_offset += ELF32_HEADER_SIZE
    fd.seek(elfhdr_offset)
    #--------------PT_NOTE--------------------

    #--------------PT_LOAD--------------------
    f_offset = DATA_OFFSET
    elf32_p = ELE32_P_HEADER()
    minidump_mem = Minidump_Mem_Arm32()
    minidump_mem_name_l = fnmatch.filter(os.listdir(dirname), '*_kernel_mem_info')
    minidump_mem_file = open(os.path.join(dirname, minidump_mem_name_l[0]), 'rb')
    minidump_mem_offset = 0
    minidump_mem_section = minidump_mem_file.read(MINIDUMP_MEM32_SIZE)
    minidump_mem_num = 0
    while minidump_mem_num < MINIDUMP_MEM_MAX:
        minidump_mem.decode(minidump_mem_section)
        #return when all section added
        if minidump_mem.paddr == 0 or minidump_mem.paddr&0xfffffff000000000 :
            break
        elf32_p.p_type = PT_LOAD
        elf32_p.p_flags = PF_R|PF_W|PF_X
        elf32_p.p_offset = f_offset
        elf32_p.p_vaddr = minidump_mem.vaddr
        elf32_p.p_paddr = minidump_mem.paddr
        elf32_p.p_filesz = elf32_p.p_memsz = minidump_mem.size
        elf32_p.p_align = 0
        f_offset += minidump_mem.size

        #update offset for fd
        fd.write(elf32_p)
        elfhdr_offset += ELF32_P_HEADER_SIZE
        fd.seek(elfhdr_offset)

        #update offset for minidump_mem_file
        minidump_mem_offset += MINIDUMP_MEM32_SIZE
        minidump_mem_file.seek(minidump_mem_offset)
        minidump_mem_section = minidump_mem_file.read(MINIDUMP_MEM32_SIZE)
        minidump_mem_num += 1

    elf32_h.e_phnum = minidump_mem_num
    fd.seek(0)
    fd.write(elf32_h)
    minidump_mem_file.close()
    fd.close()

def Generate_elf64_files(dirname):
    file_name = '000_minidump_elfhdr'
    file_size = '8192'
    file_path = os.path.join(dirname, file_name)
    create_new_file(file_path, file_size)
    fd = open(os.path.join(dirname, file_name), 'rb+')
    fd.seek(0)
    elfhdr_offset = 0

    elf64_h = ELE64_HEADER()
    elf64_nh = ELE64_HEADER()

    elf64_h.e_ident0 = ELFMAG.encode()
    elf64_h.e_ident1 = ELFCLASS64
    elf64_h.e_ident2 = ELFDATA2LSB
    elf64_h.e_ident3 = EV_CURRENT
    elf64_h.e_ident4 = ELF_OSABI
    elf64_h.e_ident5 = 0
    elf64_h.e_type = ET_CORE
    elf64_h.e_machine = EM_ARM64
    elf64_h.e_version = EV_CURRENT
    elf64_h.e_entry = 0
    elf64_h.e_phoff = ELF64_HEADER_SIZE
    elf64_h.e_shoff = 0;
    elf64_h.e_flags = ELF_CORE_EFLAGS
    elf64_h.e_ehsize = ELF64_HEADER_SIZE
    elf64_h.e_phentsize = ELF64_P_HEADER_SIZE
    elf64_h.e_phnum = 0
    elf64_h.e_shentsize = 0;
    elf64_h.e_shnum = 0;
    elf64_h.e_shstrndx = 0;

    fd.write(elf64_h)
    elfhdr_offset += ELF64_HEADER_SIZE
    fd.seek(elfhdr_offset)
    #--------------PT_NOTE--------------------
    elf64_nhdr = ELE64_P_HEADER()
    elf64_nhdr.p_type = PT_NOTE
    elf64_nhdr.p_offset = 0
    elf64_nhdr.p_vaddr = 0
    elf64_nhdr.p_paddr = 0
    elf64_nhdr.p_filesz = 0
    elf64_nhdr.p_memsz = 0
    elf64_nhdr.p_flags = 0
    elf64_nhdr.p_align = 0

    fd.write(elf64_nhdr)
    elfhdr_offset += ELF64_P_HEADER_SIZE
    fd.seek(elfhdr_offset)

    #--------------PT_LOAD--------------------
    f_offset = DATA_OFFSET
    elf64_p = ELE64_P_HEADER()
    minidump_mem = Minidump_Mem_Arm64()
    minidump_mem_name_l = fnmatch.filter(os.listdir(dirname), '*_kernel_mem_info')
    minidump_mem_file = open(os.path.join(dirname, minidump_mem_name_l[0]), 'rb')
    minidump_mem_offset = 0
    minidump_mem_section = minidump_mem_file.read(MINIDUMP_MEM64_SIZE)
    minidump_mem_num = 0
    while minidump_mem_num < MINIDUMP_MEM_MAX:
        minidump_mem.decode(minidump_mem_section)
        #return when all section added
        if minidump_mem.paddr == 0 or minidump_mem.paddr&0xfffffff000000000 :
            break
        elf64_p.p_type = PT_LOAD
        elf64_p.p_flags = PF_R|PF_W|PF_X
        elf64_p.p_offset = f_offset
        elf64_p.p_vaddr = minidump_mem.vaddr
        elf64_p.p_paddr = minidump_mem.paddr
        print(hex(elf64_p.p_paddr))
        elf64_p.p_filesz = elf64_p.p_memsz = minidump_mem.size
        elf64_p.p_align = 0
        f_offset += minidump_mem.size

        #update offset for fd
        fd.write(elf64_p)
        elfhdr_offset += ELF64_P_HEADER_SIZE
        fd.seek(elfhdr_offset)

        #update offset for minidump_mem_file
        minidump_mem_offset += MINIDUMP_MEM64_SIZE
        minidump_mem_file.seek(minidump_mem_offset)
        minidump_mem_section = minidump_mem_file.read(MINIDUMP_MEM64_SIZE)
        minidump_mem_num += 1


    elf64_h.e_phnum = minidump_mem_num
    print(minidump_mem_num)
    fd.seek(0)
    fd.write(elf64_h)
    minidump_mem_file.close()
    fd.close()

def handle_elf(dirname):
    kimage_string = "kimage_voffset"
    kimage_string = kimage_string.encode()
    dump_files = fnmatch.filter(os.listdir(dirname), '*_minidump_*')
    print(dump_files)
    if len(dump_files) == 0:
        print('Don\'t exist kernel file!!!')
        return
    file_list = fnmatch.filter(os.listdir(dirname), '*vmcore*')
    print(file_list[0])
    vmcoreinfo_file = file_list[0]
    infofd = open(os.path.join(dirname, vmcoreinfo_file), 'rb+')
    for line in infofd.readlines():
        if kimage_string in line:
            Generate_elf64_files(dirname)
            return
    Generate_elf32_files(dirname)

def get_bootloader_version(dirname):
    global bootloader_version
    zlib_files=fnmatch.filter(os.listdir(dirname), '*.zlib')
    if len(zlib_files) != 0:
        bootloader_version = 1

# for parse kernel log buf #
desc_mask = 0

desc_miss       =  -1 # ID mismatch (pseudo state)
desc_reserved   = 0x0 # reserved, in use by writer
desc_committed  = 0x1 # committed by writer, could get reopened
desc_finalized  = 0x2 # committed, no further modification allowed
desc_reusable   = 0x3 # free, not yet used by any writer

KMSG_FILE = 'last_kmsg.log'
MSEC = 1000000000
TIME_LEVEL = 20
head_id_offset = 0
tail_id_offset = 0
text_data_ring_offset = 0
desc_count_bits_offset = 0
begin_offset = 0
next_offset = 0
prb_desc_size = 0
printk_info_size = 0
ulong_size = 4
count_bits = 0
log_buf_len = 0

def get_python_version():
    if sys.version_info.major == 2:
        reload(sys)
        sys.setdefaultencoding('utf8')

def get_state_var(e, f):
    if e != (f & desc_mask):
        return desc_miss
    return 3 & (f >> (ulong_size*8 - 2))


def dump_record(outfd, infd, id):
    # get prb_desc #
    offset = (id % count_bits) * prb_desc_size;
    descsfd.seek(offset, 0)

    # get state_var to check whther the log is valid #
    temp = descsfd.read(ulong_size)
    if ulong_size==8:
        temp = struct.unpack('Q', temp)
    else:
        temp = struct.unpack('I', temp)
    statevar = temp[0]
    statevar = get_state_var(id,statevar)
    if statevar != desc_committed and statevar != desc_finalized :
        return

    # get begin and next in log_buf #
    temp = descsfd.read(ulong_size)
    if ulong_size==8:
        temp = struct.unpack('Q', temp)
    else:
        temp = struct.unpack('I', temp)
    begin = temp[0]
    temp = descsfd.read(ulong_size)
    if ulong_size==8:
        temp = struct.unpack('Q', temp)
    else:
        temp = struct.unpack('I', temp)
    next = temp[0]
    begin = begin % log_buf_len
    next = next % log_buf_len
    if begin == next :
        return

    # get printk_info offset #
    offset = (id % count_bits) * printk_info_size
    infosfd.seek(offset, 0)

    # get ts #
    infosfd.seek(8,1)
    temp = infosfd.read(8)
    temp = struct.unpack('Q',temp)
    ts = temp[0]
    nanos = ts / 1000000000;
    rem = ts % 1000000000;

    # get text_len #
    temp = infosfd.read(2)
    temp = struct.unpack('H',temp)
    text_len = temp[0]

    # get level #
    temp = infosfd.seek(1,1)
    temp = infosfd.read(1)
    temp = struct.unpack('B',temp)
    level = temp[0]
    level = level >> 5

    # get caller_id #
    temp = infosfd.read(4)
    temp = struct.unpack('I',temp)
    caller_id = temp[0]
    if (caller_id & (1 << 30)):
        caller_id = 'T' + str(caller_id & 0x3fffff) + '@C' + str((caller_id >> 22) & 0xf)
    else:
        if caller_id & 0x80000000:
            CPU = caller_id & ~0x80000000
            caller_id = 'C' + str(CPU)
        else :
            task = caller_id & ~0x80000000
            caller_id = 'T' + str(task)

    if (begin > next) :
        begin = 0
    begin += ulong_size;
    if (next - begin < text_len) :
        text_len = next - begin

    infd.seek(begin, 0)
    log_text = infd.read(text_len)
    try:
        log_text = log_text.decode()
        for text in log_text.split('\n'):
            log_str = '<%x>[%5lu.%06lu] %s %s\n' % (level, nanos, rem, caller_id, text)
            outfd.write(log_str)
    except:
        return


# get head_id and tail_id #
def get_id(self):
    global head_id
    global tail_id
    file_list = fnmatch.filter(os.listdir(self), '*data-bss')
    if len(file_list) == 0:
        print('Don\'t exist data-bss file!!!')
        return -1
    databss_file = file_list[0]
    infofd = open(os.path.join(self, databss_file), 'rb+')
    prb_offset = prb_addr - data_bss

    offset1 = prb_offset + head_id_offset

    infofd.seek(offset1,0)
    temp0 = infofd.read(ulong_size)
    if ulong_size==8:
        temp0 = struct.unpack('Q', temp0)
    else:
        temp0 = struct.unpack('I', temp0)

    head_id = temp0[0]

    offset2 = prb_offset + tail_id_offset
    infofd.seek(offset2,0)
    temp1 = infofd.read(ulong_size)
    if ulong_size==8:
        temp1 = struct.unpack('Q', temp1)
    else:
        temp1 = struct.unpack('I', temp1)

    tail_id = temp1[0]


    infofd.close()

def get_index(self):
    global desc_mask
    global head_id_offset
    global tail_id_offset
    global text_data_ring_offset
    global prb_offset
    global prb_desc_size
    global printk_info_size
    global begin_offset
    global next_offset
    global ulong_size
    global log_buf_len
    global count_bits
    global prb_addr
    global data_bss

    desc_mask_str = "DESC_ID_MASK"
    head_id_offset_str = "prb_desc_ring.head_id"
    tail_id_offset_str = "prb_desc_ring.tail_id"
    text_data_ring_offset_str = "printk_ringbuffer.text_data_ring"
    prb_addr_str = "SYMBOL(prb)"
    prb_desc_size_str = "SIZE(prb_desc)"
    printk_info_size_str = "SIZE(printk_info)"
    data_bss_str = "data-bss"
    begin_offset_str = "prb_data_blk_lpos.begin"
    next_offset_str = "prb_data_blk_lpos.next"
    arch_flag = "kimage_voffset"
    counter_bits_str = "descs_counts"
    log_buf_len_str = "log_buf_len"

    data_bss_str = data_bss_str.encode()
    desc_mask_str = desc_mask_str.encode()
    head_id_offset_str = head_id_offset_str.encode()
    tail_id_offset_str = tail_id_offset_str.encode()
    text_data_ring_offset_str = text_data_ring_offset_str.encode()
    prb_addr_str = prb_addr_str.encode()
    prb_desc_size_str = prb_desc_size_str.encode()
    printk_info_size_str= printk_info_size_str.encode()
    arch_flag = arch_flag.encode()
    counter_bits_str = counter_bits_str.encode()
    log_buf_len_str = log_buf_len_str.encode()
    begin_offset_str = begin_offset_str.encode()
    next_offset_str = next_offset_str.encode()

    file_list = fnmatch.filter(os.listdir(self), '*vmcore*')
    if len(file_list) == 0:
        print('Don\'t exist data-bss file!!!')
        return -1
    vmcore_file = file_list[0]
    infofd = open(os.path.join(self, vmcore_file), 'rb+')
    for line in infofd.readlines():
        if desc_mask_str in line:
            idx_a = re.split(str.encode('='), line)
            desc_mask = int(idx_a[1],16)
        if head_id_offset_str in line:
            idx_b = re.split(str.encode('='), line)
            head_id_offset = int(idx_b[1])
        if tail_id_offset_str in line:
            idx_c = re.split(str.encode('='), line)
            tail_id_offset = int(idx_c[1])

        if text_data_ring_offset_str in line:
            idx_d = re.split(str.encode('='), line)
            text_data_ring_offset = int(idx_d[1])

        if prb_desc_size_str in line:
            idx_e = re.split(str.encode('='), line)
            prb_desc_size = int(idx_e[1])

        if printk_info_size_str in line:
            idx_f = re.split(str.encode('='), line)
            printk_info_size = int(idx_f[1])

        if prb_addr_str in line:
            idx_g = re.split(str.encode('='), line)
            prb_addr = int(idx_g[1],16)

        if data_bss_str in line:
            idx_h = re.split(str.encode('='), line)
            data_bss = int(idx_h[1],16)

        if begin_offset_str in line:
            idx_i = re.split(str.encode('='), line)
            begin_offset = int(idx_i[1])

        if next_offset_str in line:
            idx_j = re.split(str.encode('='), line)
            next_offset = int(idx_j[1])

        if arch_flag in line:
            ulong_size = 8
        if counter_bits_str in line:
            idx_k = re.split(str.encode('='), line)
            count_bits = int(idx_k[1],16)

        if log_buf_len_str in line:
            idx_l = re.split(str.encode('='), line)
            log_buf_len = int(idx_l[1],16)

    infofd.close()

def parse_log_buf(dirname):

    global descsfd
    global infosfd

    path = dirname

    get_python_version()

    if get_index(path) == -1:
        return

    if get_id(path) == -1:
        return

    file_list = fnmatch.filter(os.listdir(path), '*_log_buf')
    if len(file_list) == 0:
        print('Don\'t exist log_buf file!!!')
        return

    log_buf_file = file_list[0]

    file_list = fnmatch.filter(os.listdir(path), '*descs')
    if len(file_list) == 0:
        print('Don\'t exist prb_desc file!!!')
        return

    descs = file_list[0]
    descsfd = open(os.path.join(path, descs), 'rb+')

    file_list = fnmatch.filter(os.listdir(path), '*infos')
    if len(file_list) == 0:
        print('Don\'t exist prb_infos file!!!')
        return

    infos = file_list[0]
    infosfd = open(os.path.join(path, infos), 'rb+')

    id = tail_id

    with open(os.path.join(path, KMSG_FILE), 'w') as outfd:
        with open(os.path.join(path, log_buf_file), 'rb+') as logbuf_fd:
            while (id != head_id) :
                dump_record(outfd, logbuf_fd, id)
                id = (id + 1) & desc_mask
            dump_record(outfd, logbuf_fd, id)

        logbuf_fd.close()
    outfd.close()
    descsfd.close()
    infosfd.close()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        dump_dir = sys.argv[1]
    for dirpath, dirnames, filenames in os.walk(dump_dir):
        for dirname in dirnames:
            j = os.path.join(dirpath, dirname)
            os.chdir(j)
            i = os.getcwd()
            print(i)
            get_bootloader_version(i)
            if bootloader_version == 0:
                uncompress_gzip_files(i)
            elif bootloader_version == 1:
                uncompress_zlib_files(i)
                handle_elf(i)
            merge_file(i)
            parse_log_buf(i)
