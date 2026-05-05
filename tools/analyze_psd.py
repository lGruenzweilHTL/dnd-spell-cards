import os
from psd_tools import PSDImage


def analyze_all_psds(template_dir):
    for filename in os.listdir(template_dir):
        if not filename.endswith(".psd"):
            continue
        file_path = os.path.join(template_dir, filename)
        psd = PSDImage.open(file_path)
        print(f"--- Analyzing {filename} ---")

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


analyze_all_psds("nBeebz's 5e Spell Cards/Templates/")
