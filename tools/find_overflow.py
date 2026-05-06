import os
from weasyprint import HTML
import psycopg2
from psycopg2.extras import RealDictCursor
from jinja2 import Environment, FileSystemLoader
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '../render'))
from generate import fetch_spells

def main():
    os.chdir(os.path.join(os.path.dirname(__file__), '../render'))
    spells = fetch_spells()
    
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template.html")
    html_out = template.render(spells=spells)
    
    with open('style.css', 'r') as f:
        css = f.read()
    
    css = css.replace('height: 380px;', '/* height: 380px; */').replace('overflow: hidden;', '/* overflow: hidden; */')
    with open('style_test.css', 'w') as f:
        f.write(css)
        
    html_out = html_out.replace('style.css', 'style_test.css')
    
    doc = HTML(string=html_out, base_url=".").render()
    
    overflow_spells = []
    
    page_idx = 0
    for page in doc.pages:
        def find_desc(box):
            if box.position_x == 100 and box.position_y == 616 and box.width == 634:
                return box
            if hasattr(box, 'children'):
                for child in box.children:
                    res = find_desc(child)
                    if res: return res
            return None
            
        desc_box = find_desc(page._page_box)
        if desc_box:
            if desc_box.height > 380:
                overflow_spells.append(spells[page_idx]['slug'])
        page_idx += 1
        
    print(json.dumps(overflow_spells))
        
if __name__ == '__main__':
    main()
