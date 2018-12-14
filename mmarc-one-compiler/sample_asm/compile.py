import binascii
from bitstring import *

instruction_dictionary = {
    "BIZI": "0b000",
    "SAAD": "0b001",
    "STOR": "0b010",
    "SUBA": "0b011",
    "ADDI": "0b100",
    "ADDA": "0b101",
    "MOVI": "0b110",
    "LAAD": "0b111"
}


def make_binary():
    in_filename = input("Enter a file name: ")
    input_file = open(in_filename, "r")

    out_filename = in_filename.replace(".txt", ".mmarc1")
    output_file = open(out_filename,"w")

    for instruction in input_file.readlines():
        if not instruction[0] == "#":
            parts = instruction.split()
            if len(parts) > 1:
                opcode = parts[0]
                param = parts[1]

                param_binary = int(param, 0)
                opcode_binary = instruction_dictionary.get(opcode)

                bin_value = BitArray(int=param_binary, length=13)

                bin_value.prepend(opcode_binary)

                output_file.write(bin_value.hex)
                output_file.write(" ")

    input_file.close()
    output_file.close()


make_binary()
