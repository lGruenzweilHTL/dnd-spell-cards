import os
from psd_tools import PSDImage


def analyze_psd(file_path):
    psd = PSDImage.open(file_path)
    print(f"--- Analyzing {os.path.basename(file_path)} ---")
    print(f"Size: {psd.size}")

    def print_layers(layer, indent=0):
        print(
            "  " * indent
            + f"- {layer.name} (type: {layer.kind}, visible: {layer.visible}, bbox: {layer.bbox})"
        )
        if layer.is_group():
            for child in layer:
                print_layers(child, indent + 1)

    for layer in psd:
        print_layers(layer)


analyze_psd("nBeebz's 5e Spell Cards/Templates/_ABJURATION.psd")
