import numpy as np
import matplotlib.colors as mcolors
from PIL import Image

# --- 功能 1: 色盲模拟算法 (Machado et al.) ---
def simulate_colorblindness(hex_color, type="Deuteranopia"):
    # 1. Hex to Linear RGB
    rgb = mcolors.hex2color(hex_color)
    r, g, b = rgb
    
    # Gamma correction removal
    r = r ** 2.2
    g = g ** 2.2
    b = b ** 2.2

    # 2. Simulation Matrices
    deut_matrix = np.array([[0.625, 0.375, 0], [0.7, 0.3, 0], [0, 0.3, 1]])
    prot_matrix = np.array([[0.567, 0.433, 0], [0.558, 0.442, 0], [0, 0.242, 0.758]])
    trit_matrix = np.array([[0.95, 0.05, 0], [0, 0.433, 0.567], [0, 0.475, 0.525]])

    if type == "Deuteranopia":
        matrix = deut_matrix
    elif type == "Protanopia":
        matrix = prot_matrix
    elif type == "Tritanopia":
        matrix = trit_matrix
    else:
        return hex_color

    # 3. Apply Matrix
    transform = np.dot(np.array([r, g, b]), matrix.T)
    
    # 4. Clip and Re-apply Gamma
    transform = np.clip(transform, 0, 1)
    transform = transform ** (1/2.2)
    
    return mcolors.to_hex(transform)

# --- 功能 2: DPI 转换器 ---
def convert_dpi(image_file, target_dpi=300):
    img = Image.open(image_file)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    return img
