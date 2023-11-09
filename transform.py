import os
from typing import Optional, Set, List
from dataclasses import dataclass
import argparse

import ruamel.yaml as yaml
parser = argparse.ArgumentParser()
parser.add_argument("folder")

@dataclass
class Entry:
    text: str
    code: str
    weight: int


def get_entries(dict: str, filters: Optional[Set[str]] = None) -> List[Entry]:
    with open(dict) as f:
        # TODO: figure out who to blame (tab)
        first_part = f.read().split('...', 1)[0]
        spec = yaml.safe_load(first_part)
        text_idx = -1
        code_idx = -1
        weight_idx = -1
        for idx, col in enumerate(spec['columns']):
            if col == 'text':
                text_idx = idx
            elif col == 'code':
                code_idx = idx
            elif col == 'weight':
                weight_idx = idx
    all_entries = []
    with open(dict) as f:
        mappings = f.read().split("...", 1)[1]
        for mapping in mappings.splitlines():
            mapping = mapping.strip()
            if mapping == "":
                continue
            if mapping.startswith('#'):
                continue
            segs = mapping.strip().split('\t')
            try:
                text = segs[text_idx]
                code = segs[code_idx]
                if code.startswith(';'):
                    continue
                weight = int(segs[weight_idx])
                if filters is not None and text not in filters:
                    continue
                all_entries.append(Entry(text, code, weight))
            except Exception as e:
                import IPython
                IPython.embed()
                print(repr(e), 'mapping:', mapping)
    return all_entries

def transform_dict_single(args, output):
    with open(os.path.join(args.folder, "core2022.dict.yaml")) as f:
        core = f.read().split("...")[1]
        core_chars = {x.split("\t")[0] for x in core.splitlines()}
    entries = get_entries(os.path.join(args.folder, 'tiger.dict.yaml'), core_chars)
    entries = sorted(entries, key=lambda x: -x.weight)
    entries.extend(get_entries(os.path.join(args.folder, 'tiger.extended.dict.yaml')))
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
    for entry in entries:
        dicts.append(f'{entry.code} {entry.text}')

    with open(output, "w") as f:
        f.write("\n".join(dicts))

def transform_dict_ci(args, output):
    with open(os.path.join(args.folder, "core2022.dict.yaml")) as f:
        core = f.read().split("...")[1]
        core_chars = {x.split("\t")[0] for x in core.splitlines()}
    entries = get_entries(os.path.join(args.folder, 'tigress.dict.yaml'), core_chars)
    entries.extend(get_entries(os.path.join(args.folder, 'tigress_ci.dict.yaml')))
    # entries.extend(get_entries(os.path.join(args.folder, 'tigress_simp_ci.dict.yaml')))
    entries = sorted(entries, key=lambda x: -x.weight)
    entries.extend(get_entries(os.path.join(args.folder, 'tiger.extended.dict.yaml')))
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
    for entry in entries:
        dicts.append(f'{entry.code} {entry.text}')

    with open(output, "w") as f:
        f.write("\n".join(dicts))


def main():
    args = parser.parse_args()
    transform_dict_single(args, 'huma.txt')
    transform_dict_ci(args, 'huma-ci.txt')


if __name__ == "__main__":
    main()
