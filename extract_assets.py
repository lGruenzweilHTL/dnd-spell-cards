import os
from psd_tools import PSDImage


def extract_assets(template_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "backgrounds"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "schools"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "indicators"), exist_ok=True)

    # We only need to extract the indicators once, from any file
    first_file = True

    for filename in os.listdir(template_dir):
        if not filename.endswith(".psd"):
            continue

        school_name = filename.replace("_", "").replace(".psd", "").lower()
        filepath = os.path.join(template_dir, filename)

        print(f"Processing {filename}...")
        psd = PSDImage.open(filepath)

        # We need the background (everything except text and indicators)
        # To do this safely, we hide Text and Indicators groups, then export the PSD composite

        for layer in psd:
            if layer.name in ["Text", "Indicators"]:
                layer.visible = False
            else:
                layer.visible = True

        # Re-composite the image with those layers hidden
        bg_image = psd.composite()
        bg_image.save(os.path.join(output_dir, "backgrounds", f"{school_name}.png"))

        # Now let's extract the school icon (from the first layer group -> Abjuration, Evocation etc)
        # It's usually inside "Template" group
        template_group = next((l for l in psd if l.name == "Template"), None)
        if template_group:
            for layer in template_group:
                # E.g. "Abjuration", "Evocation"
                if layer.name.lower() == school_name:
                    icon_img = layer.topil()
                    if icon_img:
                        icon_img.save(
                            os.path.join(output_dir, "schools", f"{school_name}.png")
                        )

        # Only extract the shared indicators (V, S, M, Classes) from the first file
        if first_file:
            indicators_group = next((l for l in psd if l.name == "Indicators"), None)
            if indicators_group:
                for layer in indicators_group:
                    # E.g. "Verbal", "Wizard", "Concentration"
                    img = layer.topil()
                    if img:
                        # Clean up name
                        name = layer.name.lower()
                        img.save(os.path.join(output_dir, "indicators", f"{name}.png"))
            first_file = False

    print("Extraction complete.")


if __name__ == "__main__":
    extract_assets("nBeebz's 5e Spell Cards/Templates/", "assets")
