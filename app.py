"""
🎨 DIP-IMAGE-STUDIO - Digital Image Processing Suite
=====================================================
Production-Ready | Cloud-Optimized | Premium Edition

Contributors:
    - Ahmed Elshenawy
    - Ahmed Osama
    - Ahmed Seliem
    - Abdullrahman Elshhawy
    - Abdullrahman Shaheen

Final Polish Version with:
- Ultra-clean standalone look
- Gradient border frames on images
- Spinner + Toast notifications
- Step-by-step sidebar guide
- High-resolution downloads
"""

import streamlit as st

# =============================================================================
# PAGE CONFIG - MUST BE FIRST STREAMLIT COMMAND!
# =============================================================================
st.set_page_config(
    page_title="DIP-IMAGE-STUDIO",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# IMPORTS (after page config)
# =============================================================================
try:
    import cv2
    import numpy as np
    from PIL import Image
    import io
    import time
except ImportError as e:
    st.error(f"❌ Failed to import required module: {e}")
    st.stop()

# =============================================================================
# CONFIGURATION
# =============================================================================
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
SUPPORTED_FORMATS = ['jpg', 'png', 'jpeg']

# =============================================================================
# ZERO-UI FOOTPRINT CSS - 100% INDEPENDENT WEB APP LOOK
# Hides: Manage App button, GitHub/Share icons, Header, Footer, Sidebar Nav
# =============================================================================
st.markdown("""
<style>
    /* ===== ZERO-UI FOOTPRINT: HIDE ALL STREAMLIT DEFAULT ELEMENTS ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stSidebarNav"] {display: none;}
    
    /* Hide the toolbar/action buttons at top */
    [data-testid="stToolbar"] {display: none !important;}
    .stActionButton {display: none !important;}
    
    /* ===== IMPORT PREMIUM FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* ===== CSS CUSTOM PROPERTIES (DESIGN TOKENS) ===== */
    :root {
        --bg-void: #0E1117;
        --bg-dark: #161B22;
        --bg-card: rgba(22, 27, 34, 0.75);
        --glass-border: rgba(0, 212, 255, 0.2);
        --glass-border-hover: rgba(0, 212, 255, 0.4);
        --neon-cyan: #00d4ff;
        --neon-pink: #ff007f;
        --neon-purple: #a855f7;
        --neon-green: #00ff88;
        --gradient-cyber: linear-gradient(135deg, #00d4ff 0%, #ff007f 100%);
        --gradient-aurora: linear-gradient(135deg, #00d4ff 0%, #a855f7 50%, #ff007f 100%);
        --text-primary: #FAFAFA;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
        --radius-2xl: 24px;
        --shadow-neon: 0 0 20px rgba(0, 212, 255, 0.3), 0 0 40px rgba(0, 212, 255, 0.1);
        --shadow-pink: 0 0 20px rgba(255, 0, 127, 0.3), 0 0 40px rgba(255, 0, 127, 0.1);
    }
    
    /* ===== GLOBAL STYLES ===== */
    * {
        font-family: 'Inter', 'Rajdhani', sans-serif;
    }
    
    html, body, .stApp {
        background: var(--bg-void) !important;
    }
    
    .stApp {
        background-image: 
            radial-gradient(ellipse 80% 50% at 20% -20%, rgba(0, 212, 255, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse 60% 40% at 80% 100%, rgba(255, 0, 127, 0.12) 0%, transparent 50%),
            radial-gradient(ellipse 40% 30% at 50% 50%, rgba(168, 85, 247, 0.05) 0%, transparent 50%);
    }
    
    /* ===== GLASSMORPHISM SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(14, 17, 23, 0.92) 0%, rgba(22, 27, 34, 0.95) 100%) !important;
        backdrop-filter: blur(30px) saturate(200%);
        -webkit-backdrop-filter: blur(30px) saturate(200%);
        border-right: 1px solid var(--glass-border);
        box-shadow: 
            4px 0 30px rgba(0, 0, 0, 0.6),
            inset -1px 0 0 rgba(255, 255, 255, 0.05);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdown"] {
        color: var(--text-primary);
    }
    
    /* ===== GLOWING NEON HEADER ===== */
    .neon-header-container {
        text-align: center;
        padding: 2.5rem 1.5rem;
        margin-bottom: 2rem;
        background: linear-gradient(180deg, rgba(0, 212, 255, 0.08) 0%, rgba(255, 0, 127, 0.04) 50%, transparent 100%);
        border-radius: var(--radius-2xl);
        border: 1px solid var(--glass-border);
        position: relative;
        overflow: hidden;
    }
    
    .neon-header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        height: 2px;
        background: var(--gradient-aurora);
        filter: blur(1px);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.8);
    }
    
    .header-icon {
        font-size: 3.5rem;
        margin-bottom: 0.75rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    .neon-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        background: var(--gradient-aurora);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
        position: relative;
        animation: glow-pulse 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow-pulse {
        from {
            filter: drop-shadow(0 0 10px rgba(0, 212, 255, 0.5)) drop-shadow(0 0 20px rgba(0, 212, 255, 0.3));
        }
        to {
            filter: drop-shadow(0 0 15px rgba(255, 0, 127, 0.5)) drop-shadow(0 0 30px rgba(255, 0, 127, 0.3));
        }
    }
    
    .header-subtitle {
        font-family: 'Rajdhani', sans-serif;
        color: var(--text-secondary);
        font-size: 1rem;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }
    
    /* ===== PREMIUM IMAGE CARDS WITH GRADIENT BORDER ===== */
    .image-card {
        position: relative;
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            0 0 20px rgba(0, 212, 255, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Gradient Border Effect */
    .image-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: var(--gradient-aurora);
        border-radius: 22px;
        z-index: -1;
        opacity: 0.6;
        transition: opacity 0.3s ease;
    }
    
    .image-card:hover::before {
        opacity: 1;
    }
    
    .image-card:hover {
        transform: translateY(-6px);
        box-shadow: 
            0 16px 48px rgba(0, 0, 0, 0.5),
            0 0 40px rgba(0, 212, 255, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.08);
    }
    
    /* Processed image specific gradient (pink dominant) */
    .image-card-processed::before {
        background: linear-gradient(135deg, #ff007f 0%, #a855f7 50%, #00d4ff 100%);
    }
    
    .image-badge {
        text-align: center;
        padding: 0.6rem 1rem;
        margin-bottom: 1rem;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        border-radius: var(--radius-md);
    }
    
    .badge-original {
        color: var(--neon-cyan);
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
    }
    
    .badge-processed {
        color: var(--neon-pink);
        background: rgba(255, 0, 127, 0.1);
        border: 1px solid rgba(255, 0, 127, 0.3);
    }
    
    /* ===== FADE-IN ANIMATION FOR PROCESSED IMAGE ===== */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px) scale(0.98);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    .processed-container {
        animation: fadeInUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }
    
    /* ===== IMAGE STYLING WITH GRADIENT FRAME ===== */
    .image-frame {
        position: relative;
        padding: 3px;
        background: var(--gradient-aurora);
        border-radius: 18px;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
    }
    
    .image-frame img {
        border-radius: 15px !important;
        display: block;
        width: 100%;
    }
    
    [data-testid="stImage"] img {
        border-radius: 16px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: transform 0.3s ease;
    }
    
    [data-testid="stImage"] img:hover {
        transform: scale(1.02);
    }
    
    /* ===== SIDEBAR STYLING ===== */
    .sidebar-brand {
        text-align: center;
        padding: 1.5rem 1rem;
        border-bottom: 1px solid var(--glass-border);
        margin-bottom: 1rem;
    }
    
    .sidebar-brand-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .sidebar-brand-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        background: var(--gradient-cyber);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.05em;
    }
    
    /* Step Guide Styling */
    .step-guide {
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        background: rgba(0, 212, 255, 0.05);
        border-left: 3px solid var(--neon-cyan);
        border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    }
    
    .step-number {
        display: inline-block;
        width: 24px;
        height: 24px;
        line-height: 24px;
        text-align: center;
        background: var(--gradient-cyber);
        color: white;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    
    .step-text {
        color: var(--text-secondary);
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .step-active {
        background: rgba(0, 255, 136, 0.08);
        border-left-color: var(--neon-green);
    }
    
    .step-active .step-number {
        background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
    }
    
    /* Elegant thin divider */
    .thin-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(0, 212, 255, 0.3) 50%, transparent 100%);
        margin: 1rem 0;
    }
    
    .sidebar-section {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--neon-cyan);
        margin: 1.5rem 0 0.75rem 0;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(0, 212, 255, 0.15);
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: var(--gradient-cyber) !important;
        border: none !important;
        color: white !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        border-radius: var(--radius-md) !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }
    
    /* ===== RESET BUTTON (RED HOVER) ===== */
    .reset-btn > div > button {
        background: linear-gradient(135deg, #374151 0%, #1f2937 100%) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    }
    
    .reset-btn > div > button:hover {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%) !important;
        box-shadow: 0 8px 25px rgba(220, 38, 38, 0.4) !important;
    }
    
    /* ===== DOWNLOAD BUTTONS ===== */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%) !important;
        border: none !important;
        color: #0a0d12 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700 !important;
        border-radius: var(--radius-md) !important;
        box-shadow: 0 4px 15px rgba(0, 255, 136, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(0, 255, 136, 0.5) !important;
    }
    
    /* ===== WELCOME CARD ===== */
    .welcome-card {
        background: var(--bg-card);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-2xl);
        padding: 4rem 3rem;
        text-align: center;
        max-width: 700px;
        margin: 3rem auto;
        box-shadow: 
            0 16px 48px rgba(0, 0, 0, 0.4),
            0 0 40px rgba(0, 212, 255, 0.05);
        position: relative;
        overflow: hidden;
    }
    
    .welcome-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-aurora);
    }
    
    .welcome-icon {
        font-size: 5rem;
        margin-bottom: 1.5rem;
        animation: float 3s ease-in-out infinite;
    }
    
    .welcome-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        background: var(--gradient-cyber);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
    }
    
    .welcome-text {
        color: var(--text-secondary);
        font-size: 1.1rem;
        line-height: 1.9;
    }
    
    .feature-list {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.75rem;
        margin-top: 2rem;
    }
    
    .feature-tag {
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.2);
        color: var(--neon-cyan);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* ===== PROFESSIONAL CONTRIBUTORS FOOTER ===== */
    .pro-footer {
        text-align: center;
        padding: 3rem 1rem 2.5rem;
        margin-top: 4rem;
        border-top: 1px solid var(--glass-border);
        background: linear-gradient(180deg, transparent 0%, rgba(0, 212, 255, 0.03) 100%);
    }
    
    .footer-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--neon-cyan);
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }
    
    .contributors-list {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        gap: 1rem 2rem;
        max-width: 900px;
        margin: 0 auto;
    }
    
    .contributor-name {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        font-weight: 500;
        color: var(--text-secondary);
        padding: 0.5rem 1.25rem;
        background: rgba(0, 212, 255, 0.08);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 25px;
        transition: all 0.3s ease;
        white-space: nowrap;
    }
    
    .contributor-name:hover {
        background: rgba(0, 212, 255, 0.15);
        border-color: var(--neon-cyan);
        color: var(--text-primary);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.2);
    }
    
    .footer-app-name {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.85rem;
        font-weight: 500;
        background: var(--gradient-cyber);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 2rem;
        letter-spacing: 0.05em;
    }
    
    /* ===== SPINNER STYLING ===== */
    .stSpinner > div {
        border-color: var(--neon-cyan) !important;
    }
    
    /* ===== SLIDERS & SELECT BOXES ===== */
    .stSlider > div > div > div > div {
        background: var(--gradient-cyber) !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(22, 27, 34, 0.8) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-md) !important;
    }
    
    /* ===== FILE UPLOADER ===== */
    [data-testid="stFileUploader"] {
        background: rgba(22, 27, 34, 0.5);
        border: 2px dashed var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 1rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--neon-cyan);
        background: rgba(0, 212, 255, 0.05);
    }
    
    /* ===== SECTION DIVIDERS ===== */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, var(--glass-border) 50%, transparent 100%);
        margin: 2rem 0;
    }
    
    /* ===== TOAST NOTIFICATION STYLING ===== */
    [data-testid="stToast"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--neon-green) !important;
        border-radius: var(--radius-md) !important;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-void);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--glass-border);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--neon-cyan);
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# IMAGE PROCESSING FUNCTIONS (Cloud-Ready with Error Handling)
# =============================================================================

def convert_to_grayscale(image):
    """Convert image to grayscale using OpenCV."""
    try:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except Exception as e:
        raise RuntimeError(f"Grayscale conversion failed: {e}")


def apply_gaussian_blur(image, kernel_size, sigma):
    """Apply Gaussian blur filter."""
    try:
        if kernel_size % 2 == 0:
            kernel_size += 1
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    except Exception as e:
        raise RuntimeError(f"Gaussian blur failed: {e}")


def apply_box_blur(image, kernel_size):
    """Apply box blur (average) filter."""
    try:
        if kernel_size % 2 == 0:
            kernel_size += 1
        return cv2.blur(image, (kernel_size, kernel_size))
    except Exception as e:
        raise RuntimeError(f"Box blur failed: {e}")


def apply_median_filter(image, kernel_size):
    """Apply median filter for noise removal."""
    try:
        if kernel_size % 2 == 0:
            kernel_size += 1
        return cv2.medianBlur(image, kernel_size)
    except Exception as e:
        raise RuntimeError(f"Median filter failed: {e}")


def apply_sharpening(image, strength=1.0):
    """Apply sharpening filter."""
    try:
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], dtype=np.float32)
        if strength != 1.0:
            identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.float32)
            kernel = identity + strength * (kernel - identity)
        return cv2.filter2D(image, -1, kernel)
    except Exception as e:
        raise RuntimeError(f"Sharpening failed: {e}")


def apply_canny_edge(image, low, high):
    """Apply Canny edge detection."""
    try:
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)
        return cv2.Canny(blurred, low, high)
    except Exception as e:
        raise RuntimeError(f"Canny edge detection failed: {e}")


def apply_sobel_edge(image, ksize=3):
    """Apply Sobel edge detection."""
    try:
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
        magnitude = np.sqrt(sobelx**2 + sobely**2)
        if np.max(magnitude) > 0:
            return np.uint8(255 * magnitude / np.max(magnitude))
        return np.uint8(magnitude)
    except Exception as e:
        raise RuntimeError(f"Sobel edge detection failed: {e}")


def apply_laplacian(image):
    """Apply Laplacian edge detection."""
    try:
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        laplacian_abs = np.absolute(laplacian)
        if np.max(laplacian_abs) > 0:
            return np.uint8(255 * laplacian_abs / np.max(laplacian_abs))
        return np.uint8(laplacian_abs)
    except Exception as e:
        raise RuntimeError(f"Laplacian edge detection failed: {e}")


def apply_threshold(image, threshold_value):
    """Apply global thresholding."""
    try:
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        _, thresholded = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
        return thresholded
    except Exception as e:
        raise RuntimeError(f"Thresholding failed: {e}")


def apply_adaptive_threshold(image, block_size, c):
    """Apply adaptive thresholding."""
    try:
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        if block_size % 2 == 0:
            block_size += 1
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY, block_size, c)
    except Exception as e:
        raise RuntimeError(f"Adaptive thresholding failed: {e}")


def adjust_brightness_contrast(image, brightness, contrast):
    """Adjust image brightness and contrast."""
    try:
        return cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
    except Exception as e:
        raise RuntimeError(f"Brightness/contrast adjustment failed: {e}")


def apply_inversion(image):
    """Invert image colors."""
    try:
        return cv2.bitwise_not(image)
    except Exception as e:
        raise RuntimeError(f"Inversion failed: {e}")


def apply_histogram_equalization(image):
    """Apply histogram equalization for contrast enhancement."""
    try:
        if len(image.shape) == 3:
            ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
            ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
            return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
        return cv2.equalizeHist(image)
    except Exception as e:
        raise RuntimeError(f"Histogram equalization failed: {e}")


def apply_morphological(image, operation, kernel_size):
    """Apply morphological operations."""
    try:
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        ops = {
            "Erosion": lambda: cv2.erode(gray, kernel, iterations=1),
            "Dilation": lambda: cv2.dilate(gray, kernel, iterations=1),
            "Opening": lambda: cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel),
            "Closing": lambda: cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        }
        return ops.get(operation, lambda: gray)()
    except Exception as e:
        raise RuntimeError(f"Morphological operation failed: {e}")


def process_image_with_filter(image, selected_filter, filter_params):
    """Process image with selected filter. Returns processed image."""
    if selected_filter == "Grayscale":
        return convert_to_grayscale(image)
    elif selected_filter == "Gaussian Blur":
        return apply_gaussian_blur(image, filter_params['kernel_size'], filter_params['sigma'])
    elif selected_filter == "Box Blur":
        return apply_box_blur(image, filter_params['kernel_size'])
    elif selected_filter == "Median Filter":
        return apply_median_filter(image, filter_params['kernel_size'])
    elif selected_filter == "Brightness & Contrast":
        return adjust_brightness_contrast(image, filter_params['brightness'], filter_params['contrast'])
    elif selected_filter == "Invert Colors":
        return apply_inversion(image)
    elif selected_filter == "Canny Edge":
        return apply_canny_edge(image, filter_params['low'], filter_params['high'])
    elif selected_filter == "Sobel Edge":
        return apply_sobel_edge(image, filter_params['ksize'])
    elif selected_filter == "Laplacian Edge":
        return apply_laplacian(image)
    elif selected_filter == "Sharpening":
        return apply_sharpening(image, filter_params['strength'])
    elif selected_filter == "Global Threshold":
        return apply_threshold(image, filter_params['threshold'])
    elif selected_filter == "Adaptive Threshold":
        return apply_adaptive_threshold(image, filter_params['block'], filter_params['c'])
    elif selected_filter == "Histogram Equalization":
        return apply_histogram_equalization(image)
    elif selected_filter == "Morphological Ops":
        return apply_morphological(image, filter_params['op'], filter_params['ksize'])
    return image


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point."""
    
    # Initialize session state for processing status
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    
    # =========================================================================
    # GLOWING NEON HEADER
    # =========================================================================
    st.markdown("""
    <div class="neon-header-container">
        <div class="header-icon">🎨</div>
        <div class="neon-title">DIP-IMAGE-STUDIO</div>
        <div class="header-subtitle">Digital Image Processing Suite</div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================================================
    # MODULAR SIDEBAR WITH STEP GUIDE
    # =========================================================================
    with st.sidebar:
        # Sidebar Brand
        st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">🎨</div>
            <div class="sidebar-brand-title">DIP-IMAGE-STUDIO</div>
        </div>
        """, unsafe_allow_html=True)
        
        # =====================================================================
        # STEP 1: UPLOAD IMAGE
        # =====================================================================
        st.markdown("""
        <div class="step-guide">
            <span class="step-number">1</span>
            <span class="step-text">Upload Your Image</span>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose an image",
            type=['jpg', 'png', 'jpeg'],
            help=f"Supported: JPG, PNG, JPEG (Max: {MAX_FILE_SIZE_MB}MB)",
            label_visibility="collapsed"
        )
        
        # Validate file size
        if uploaded_file and uploaded_file.size > MAX_FILE_SIZE_BYTES:
            st.error(f"⚠️ File too large! Maximum size: {MAX_FILE_SIZE_MB}MB")
            uploaded_file = None
        elif uploaded_file:
            st.success(f"✅ {uploaded_file.name}")
        
        st.markdown('<div class="thin-divider"></div>', unsafe_allow_html=True)
        
        # =====================================================================
        # STEP 2: CHOOSE FILTER CATEGORY
        # =====================================================================
        step2_class = "step-guide step-active" if uploaded_file else "step-guide"
        st.markdown(f"""
        <div class="{step2_class}">
            <span class="step-number">2</span>
            <span class="step-text">Choose Filter Category</span>
        </div>
        """, unsafe_allow_html=True)
        
        filter_category = st.selectbox(
            "Category",
            ["🚫 None", "✨ Basic", "🔍 Edge Detection", "⚡ Advanced"],
            label_visibility="collapsed",
            disabled=not uploaded_file
        )
        
        selected_filter = "None"
        filter_params = {}
        
        # -----------------------------------------------------------------
        # BASIC FILTERS
        # -----------------------------------------------------------------
        if filter_category == "✨ Basic":
            st.markdown('<div class="thin-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-section">🎚️ Basic Filters</div>', unsafe_allow_html=True)
            selected_filter = st.selectbox(
                "Filter",
                ["Grayscale", "Gaussian Blur", "Box Blur", "Median Filter", 
                 "Brightness & Contrast", "Invert Colors"],
                label_visibility="collapsed"
            )
            if selected_filter == "Gaussian Blur":
                filter_params['kernel_size'] = st.slider("Intensity", 3, 31, 5, step=2)
                filter_params['sigma'] = st.slider("Sigma", 0.1, 10.0, 1.5)
            elif selected_filter == "Box Blur":
                filter_params['kernel_size'] = st.slider("Intensity", 3, 31, 5, step=2)
            elif selected_filter == "Median Filter":
                filter_params['kernel_size'] = st.slider("Kernel Size", 3, 31, 5, step=2)
            elif selected_filter == "Brightness & Contrast":
                filter_params['brightness'] = st.slider("Brightness", -100, 100, 0)
                filter_params['contrast'] = st.slider("Contrast", 0.5, 3.0, 1.0)
        
        # -----------------------------------------------------------------
        # EDGE DETECTION FILTERS
        # -----------------------------------------------------------------
        elif filter_category == "🔍 Edge Detection":
            st.markdown('<div class="thin-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-section">🔬 Edge Filters</div>', unsafe_allow_html=True)
            selected_filter = st.selectbox(
                "Filter",
                ["Canny Edge", "Sobel Edge", "Laplacian Edge"],
                label_visibility="collapsed"
            )
            if selected_filter == "Canny Edge":
                filter_params['low'] = st.slider("Low Threshold", 0, 200, 50)
                filter_params['high'] = st.slider("High Threshold", 50, 400, 150)
            elif selected_filter == "Sobel Edge":
                filter_params['ksize'] = st.slider("Kernel Size", 1, 7, 3, step=2)
        
        # -----------------------------------------------------------------
        # ADVANCED FILTERS
        # -----------------------------------------------------------------
        elif filter_category == "⚡ Advanced":
            st.markdown('<div class="thin-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-section">🔧 Advanced Filters</div>', unsafe_allow_html=True)
            selected_filter = st.selectbox(
                "Filter",
                ["Sharpening", "Global Threshold", "Adaptive Threshold",
                 "Histogram Equalization", "Morphological Ops"],
                label_visibility="collapsed"
            )
            if selected_filter == "Sharpening":
                filter_params['strength'] = st.slider("Strength", 0.5, 5.0, 1.0)
            elif selected_filter == "Global Threshold":
                filter_params['threshold'] = st.slider("Threshold", 0, 255, 127)
            elif selected_filter == "Adaptive Threshold":
                filter_params['block'] = st.slider("Block Size", 3, 99, 11, step=2)
                filter_params['c'] = st.slider("Constant", -20, 20, 2)
            elif selected_filter == "Morphological Ops":
                filter_params['op'] = st.selectbox("Operation", 
                                                    ["Erosion", "Dilation", "Opening", "Closing"])
                filter_params['ksize'] = st.slider("Kernel Size", 3, 21, 5, step=2)
        
        st.markdown('<div class="thin-divider"></div>', unsafe_allow_html=True)
        
        # =====================================================================
        # STEP 3: DOWNLOAD (shown as inactive hint)
        # =====================================================================
        st.markdown("""
        <div class="step-guide">
            <span class="step-number">3</span>
            <span class="step-text">Download Result</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="thin-divider"></div>', unsafe_allow_html=True)
        
        # =====================================================================
        # RESET BUTTON (RED HOVER EFFECT)
        # =====================================================================
        st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
        if st.button("🔄 Reset Application", use_container_width=True):
            st.session_state.processed = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    # MAIN CONTENT AREA
    # =========================================================================
    if uploaded_file is None:
        # Welcome Card when no image is uploaded
        st.markdown("""
        <div class="welcome-card">
            <div class="welcome-icon">🖼️</div>
            <div class="welcome-title">Ready to Transform Your Images</div>
            <div class="welcome-text">
                Upload an image using the sidebar to get started.<br><br>
                Experience professional-grade image processing with our suite of powerful filters.
            </div>
            <div class="feature-list">
                <span class="feature-tag">✨ Grayscale</span>
                <span class="feature-tag">🌀 Blur Effects</span>
                <span class="feature-tag">🔍 Edge Detection</span>
                <span class="feature-tag">⚡ Sharpening</span>
                <span class="feature-tag">📊 Thresholding</span>
                <span class="feature-tag">🎨 Color Inversion</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # =====================================================================
        # IMAGE PROCESSING WITH SPINNER & TOAST NOTIFICATIONS
        # =====================================================================
        try:
            # Read and decode image
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            original_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            
            if original_image is None:
                st.error("❌ Could not read the image. Please try a different file.")
            else:
                processed_image = original_image.copy()
                filter_applied = False
                
                # Apply selected filter with spinner
                if filter_category != "🚫 None" and selected_filter != "None":
                    with st.spinner("✨ Applying DIP Magic..."):
                        try:
                            processed_image = process_image_with_filter(
                                processed_image, 
                                selected_filter, 
                                filter_params
                            )
                            filter_applied = True
                            # Small delay for visual feedback
                            time.sleep(0.3)
                        except RuntimeError as e:
                            st.error(f"❌ Filter error: {str(e)}")
                    
                    # Show toast notification on success
                    if filter_applied:
                        st.toast("Image Processed Successfully! 🎉", icon="✅")
                
                # Convert for display (BGR to RGB)
                original_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
                if len(processed_image.shape) == 2:
                    display_processed = processed_image  # Grayscale
                else:
                    display_processed = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
                
                # =============================================================
                # IMAGE WORKSPACE - Side by Side Cards with Gradient Borders
                # =============================================================
                col1, col2 = st.columns([1, 1])
                
                # Original Image Card
                with col1:
                    st.markdown('''
                    <div class="image-card">
                        <div class="image-badge badge-original">📷 Original Image</div>
                    ''', unsafe_allow_html=True)
                    st.image(original_rgb, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Processed Image Card with Fade-in Animation & Pink Gradient
                with col2:
                    filter_label = f"🎨 Processed • {selected_filter}" if selected_filter != "None" else "🎨 Processed Image"
                    st.markdown(f'''
                    <div class="image-card image-card-processed processed-container">
                        <div class="image-badge badge-processed">{filter_label}</div>
                    ''', unsafe_allow_html=True)
                    st.image(display_processed, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # =============================================================
                # HIGH-RESOLUTION DOWNLOAD SECTION
                # =============================================================
                if filter_category != "🚫 None" and selected_filter != "None":
                    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                    st.markdown("### 💾 Download High-Resolution Result")
                    
                    # Create sanitized filter name for filename
                    filter_name_clean = selected_filter.lower().replace(' ', '_').replace('&', 'and')
                    
                    # Convert to PIL for high-quality saving
                    if len(processed_image.shape) == 2:
                        pil_image = Image.fromarray(processed_image)
                    else:
                        pil_image = Image.fromarray(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB))
                    
                    col_d1, col_d2, col_d3 = st.columns(3)
                    
                    with col_d1:
                        buf = io.BytesIO()
                        # PNG is lossless - highest quality
                        pil_image.save(buf, format='PNG', optimize=False)
                        st.download_button(
                            "⬇️ PNG (Lossless)",
                            buf.getvalue(),
                            f"processed_{filter_name_clean}.png",
                            "image/png",
                            use_container_width=True
                        )
                    
                    with col_d2:
                        buf = io.BytesIO()
                        img_rgb = pil_image.convert('RGB') if pil_image.mode != 'RGB' else pil_image
                        # JPEG at maximum quality (100)
                        img_rgb.save(buf, format='JPEG', quality=100, subsampling=0)
                        st.download_button(
                            "⬇️ JPEG (Max Quality)",
                            buf.getvalue(),
                            f"processed_{filter_name_clean}.jpg",
                            "image/jpeg",
                            use_container_width=True
                        )
                    
                    with col_d3:
                        buf = io.BytesIO()
                        # WebP at maximum quality
                        pil_image.save(buf, format='WebP', quality=100, method=6)
                        st.download_button(
                            "⬇️ WebP (Best Compression)",
                            buf.getvalue(),
                            f"processed_{filter_name_clean}.webp",
                            "image/webp",
                            use_container_width=True
                        )
        
        except Exception as e:
            st.error(f"❌ Error processing image: {str(e)}")

    # =========================================================================
    # PROFESSIONAL CONTRIBUTORS FOOTER
    # =========================================================================
    st.markdown("""
    <div class="pro-footer">
        <div class="footer-title">✨ Contributors</div>
        <div class="contributors-list">
            <span class="contributor-name">Ahmed Elshenawy</span>
            <span class="contributor-name">Ahmed Osama</span>
            <span class="contributor-name">Ahmed Seliem</span>
            <span class="contributor-name">Abdullrahman Elshhawy</span>
            <span class="contributor-name">Abdullrahman Shaheen</span>
        </div>
        <div class="footer-app-name">DIP-IMAGE-STUDIO © 2024</div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# RUN APPLICATION
# =============================================================================
if __name__ == "__main__":
    main()
