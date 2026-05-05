import os
from psd_tools import PSDImage

def print_text_layers(layer, indent=0):
    if layer.kind == 'type':
        print(f"--- {layer.name} ---")
        try:
            style = layer.engine_dict.get('StyleRun', {}).get('RunArray', [{}])[0].get('StyleSheet', {}).get('StyleSheetData', {})
            leading = style.get('Leading', 'Auto')
            auto_leading = style.get('AutoLeading', 'Auto')
            print(f"Font size: {style.get('FontSize', 'N/A')}")
            print(f"Leading (line-height): {leading}, AutoLeading: {auto_leading}")
            paragraph = layer.engine_dict.get('ParagraphRun', {}).get('RunArray', [{}])[0].get('ParagraphSheet', {}).get('Properties', {})
            print(f"Justification: {paragraph.get('Justification', 'N/A')}")
        except Exception as e:
            pass

psd = PSDImage.open("nBeebz's 5e Spell Cards/Templates/_EVOCATION.psd")
for layer in psd:
    if layer.is_group():
        for child in layer:
            print_text_layers(child)
    else:
        print_text_layers(layer)
