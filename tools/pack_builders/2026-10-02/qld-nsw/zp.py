# zp.py CODE ground which [margin_px=260] [dpi=300] : zoom on a detected panel with margin
import sys, subprocess, os; sys.path.insert(0,'tools')
import trace_symbol as T
from PIL import Image
code, ground, which = sys.argv[1], sys.argv[2], int(sys.argv[3]); m = int(sys.argv[4]) if len(sys.argv) > 4 else 260; dpi = sys.argv[5] if len(sys.argv) > 5 else '300'
img = Image.open(f'Processing/Australia/NSW/Original PNGs/{code}.png').convert('RGB')
b = T.find_white_panel(img, which, True) if ground == 'white' else T.find_panel(img, ground, which, True)
print('box', b)
subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'zoom.py'), code, str(max(0, b[0] - m)), str(max(0, b[1] - m)), str(min(img.width, b[2] + m)), str(min(img.height, b[3] + m)), dpi])
