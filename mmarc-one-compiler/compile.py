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


def preprocess(lines):
    processed_lines = []
    equate_dict = {}
    for line in lines:
        if len(line) > 0:
            if line[0] in ["#", "\n"]:
                if "#EQUATE" in line:
                    parts = line.split()
                    key = parts[1]
                    value = parts[2]
                    equate_dict[key] = value
            else:
                processed_lines.append(line)

    for i in range(0, len(processed_lines)):
        line = processed_lines[i]
        items = line.split()
        if items[1] in equate_dict.keys():
            items[1] = equate_dict[items[1]]
            processed_lines[i] = items[0] + " " + items[1]

    return processed_lines


def make_binary(lines):
    bin_lines = []

    for instruction in lines:
        parts = instruction.split()
        opcode = parts[0]
        param = parts[1]

        param_binary = int(param, 0)
        opcode_binary = instruction_dictionary.get(opcode)

        bin_value = BitArray(int=param_binary, length=13)

        bin_value.prepend(opcode_binary)

        bin_lines.append(bin_value.hex)

    return bin_lines


def main():
    in_filename = input("Enter a file name: ")
    input_file = open(in_filename, "r")

    out_filename = in_filename.replace(".txt", ".mmarc1")
    output_file = open(out_filename,"w")

    lines = input_file.readlines()

    lines = preprocess(lines)

    lines = make_binary(lines)

    for line in lines:
        output_file.write(line)
        output_file.write(" ")

    input_file.close()
    output_file.close()


main()
