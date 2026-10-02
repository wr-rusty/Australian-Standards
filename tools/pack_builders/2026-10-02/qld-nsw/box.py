import sys; sys.path.insert(0,'tools')
import trace_symbol as T
from PIL import Image
code, ground = sys.argv[1], sys.argv[2]; which = int(sys.argv[3]) if len(sys.argv) > 3 else 0
img = Image.open(f'Processing/Australia/NSW/Original PNGs/{code}.png').convert('RGB')
print(T.find_white_panel(img, which, True) if ground == 'white' else T.find_panel(img, ground, which, True))
