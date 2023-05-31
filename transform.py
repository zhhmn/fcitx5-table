import os
import argparse
import ruamel.yaml as yaml

parser = argparse.ArgumentParser()
parser.add_argument("folder")


def transform_dict(args):
    # 虎单
    with open(os.path.join(args.folder, "tiger.dict.yaml")) as f:
        mappings = f.read().split("...")[1]
    with open(os.path.join(args.folder, "core2022.dict.yaml")) as f:
        core = f.read().split("...")[1]
    core_chars = {x.split("\t")[0] for x in core.splitlines()}

    current_freq = 99999999999
    dicts = [
        ";fcitx Version 0x03 Table file",
        "KeyCode=abcdefghijklmnopqrstuvwxyz",
        "Length=4",
        "[Rule]",
        "e2=p11+p12+p21+p22",
        "e3=p11+p21+p31+p32",
        "a4=p11+p21+p31+n11",
        "[Data]",
    ]
    # check frequencies & forming dict
    for mapping in mappings.splitlines():
        if mapping.strip() == "":
            continue
        try:
            char, code, freq = mapping.strip().split("\t")
            freq = int(freq)
            if freq > current_freq:
                print(char, code, freq)
            current_freq = freq
            if char in core_chars:
                dicts.append(f"{code} {char}")
        except Exception as e:
            print(mapping, repr(e))

    with open("huma.txt", "w") as f:
        f.write("\n".join(dicts))


def main():
    args = parser.parse_args()
    transform_dict(args)


if __name__ == "__main__":
    main()
