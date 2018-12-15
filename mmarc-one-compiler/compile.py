import binascii
from bitstring import *

instruction_dictionary = {
    "BIZI": "0b000",
    "SAAD": "0b001",
    "STOR": "0b010",
    "SUBA": "0b011",
    "ADDI": "0b100",
    "BRAM": "0b101",
    "MOVI": "0b110",
    "LAAD": "0b111"
}


def preprocess(lines):
    processed_lines = []
    equate_dict = {}
    label_dict = {}

    # extract equates into dictionary
    no_equates = []
    for line in lines:
        if len(line) > 0:
            if line[0] in ["#", "\n", "@"]:
                if "@EQUATE" in line:
                    parts = line.split()
                    key = parts[1]
                    value = parts[2]
                    equate_dict[key] = value
                if "@LABEL" in line:
                    no_equates.append(line)
            else:
                no_equates.append(line)

    # remove newline characters
    for i in range(0, len(no_equates)):
        no_equates[i] = no_equates[i].replace("\n", "")

    # replace equates with values
    replace_equates = []
    for i in range(0, len(no_equates)):
        line = no_equates[i]
        replace_equates.append(line)
        items = line.split()
        if items[1] in equate_dict.keys():
            items[1] = equate_dict[items[1]]
            replace_equates[i] = items[0] + " " + items[1]

    # extract labels into dictionary
    no_labels = []
    for i in range(0, len(replace_equates)):
        line = replace_equates[i]
        items = line.split()
        if items[0] == "@LABEL":
            label_dict[items[1]] = i - len(label_dict.keys())
        else:
            no_labels.append(line)

    for i in range(0, len(no_labels)):
        line = no_labels[i]
        items = line.split()
        if items[1] in label_dict.keys():
            if items[0] == "MOVI":
                items[1] = hex(label_dict[items[1]])
            else:
                items[1] = hex(label_dict[items[1]] - i - 1)
            processed_lines.append(items[0] + " " + items[1])
        else:
            processed_lines.append(no_labels[i])

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
    #in_filename = input("Enter a file name: ")
    in_filename = "sample/stack.txt"
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
