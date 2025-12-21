"""
DIP-IMAGE-STUDIO - Digital Image Processing Suite
==================================================
Production-Ready | Cloud-Optimized | Desktop Compatible

Contributors:
    - Ahmed Elshenawy
    - Ahmed Osama
    - Ahmed Seliem
    - Abdullrahman Elshhawy
    - Abdullrahman Shaheen

All filters implemented from scratch using NumPy.
"""

import streamlit as st

# =============================================================================
# PAGE CONFIG - MUST BE FIRST STREAMLIT COMMAND
# =============================================================================
st.set_page_config(
    page_title="DIP-IMAGE-STUDIO",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# IMPORTS
# =============================================================================
import numpy as np
from PIL import Image
import io

# =============================================================================
# CSS - HIDE STREAMLIT UI BUT KEEP SIDEBAR TOGGLE VISIBLE
# =============================================================================
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none !important;}
    [data-testid="stToolbar"] > div:first-child {display: none !important;}
    .stActionButton {display: none !important;}
    [data-testid="stSidebarNav"] {display: none;}
    .stStatusWidget, [data-testid="manage-app-button"] {display: none !important;}
    .viewerBadge_container__r5tak {display: none !important;}
    
    /* KEEP SIDEBAR TOGGLE ARROW VISIBLE */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] button,
    [data-testid="collapsedControl"] button,
    button[kind="header"] {
        background: rgba(0, 212, 255, 0.15) !important;
        border: 1px solid rgba(0, 212, 255, 0.4) !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="collapsedControl"] svg {
        color: #00d4ff !important;
        stroke: #00d4ff !important;
    }
    
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    /* Dark Theme */
    :root {
        --bg-dark: #0E1117;
        --neon-cyan: #00d4ff;
        --neon-pink: #ff007f;
        --text-primary: #FAFAFA;
        --text-secondary: #94a3b8;
    }
    
    html, body, .stApp {
        background: var(--bg-dark) !important;
    }
    
    .stApp {
        background-image: 
            radial-gradient(ellipse 80% 50% at 20% -20%, rgba(0, 212, 255, 0.12) 0%, transparent 50%),
            radial-gradient(ellipse 60% 40% at 80% 100%, rgba(255, 0, 127, 0.08) 0%, transparent 50%);
    }
    
    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(14, 17, 23, 0.95) 0%, rgba(22, 27, 34, 0.98) 100%) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    /* Neon Header */
    .neon-header {
        text-align: center;
        padding: 2rem;
        margin-bottom: 2rem;
        background: linear-gradient(180deg, rgba(0, 212, 255, 0.08) 0%, transparent 100%);
        border-radius: 20px;
        border: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    .neon-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00d4ff 0%, #ff007f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .neon-subtitle {
        color: var(--text-secondary);
        font-size: 1rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }
    
    /* Image Cards */
    .image-card {
        background: rgba(22, 27, 34, 0.8);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(0, 212, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .image-card:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 212, 255, 0.5);
        box-shadow: 0 8px 30px rgba(0, 212, 255, 0.15);
    }
    
    .card-label {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 1rem;
        padding: 0.5rem;
        border-radius: 8px;
    }
    
    .label-original {
        color: #00d4ff;
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
    }
    
    .label-processed {
        color: #ff007f;
        background: rgba(255, 0, 127, 0.1);
        border: 1px solid rgba(255, 0, 127, 0.3);
    }
    
    [data-testid="stImage"] img {
        border-radius: 12px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #ff007f 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.4) !important;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%) !important;
        color: #0a0d12 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
    }
    
    /* Footer */
    .pro-footer {
        text-align: center;
        padding: 2.5rem 1rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(0, 212, 255, 0.2);
        background: linear-gradient(180deg, transparent 0%, rgba(0, 212, 255, 0.03) 100%);
    }
    
    .footer-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: #00d4ff;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 1.25rem;
    }
    
    .contributors-list {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.75rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .contributor-name {
        font-size: 0.95rem;
        color: var(--text-secondary);
        padding: 0.4rem 1rem;
        background: rgba(0, 212, 255, 0.08);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 20px;
        transition: all 0.3s ease;
    }
    
    .contributor-name:hover {
        background: rgba(0, 212, 255, 0.15);
        color: var(--text-primary);
        transform: translateY(-2px);
    }
    
    .footer-brand {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.8rem;
        background: linear-gradient(135deg, #00d4ff 0%, #ff007f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 1.5rem;
    }
    
    /* Welcome Card */
    .welcome-card {
        background: rgba(22, 27, 34, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        max-width: 600px;
        margin: 2rem auto;
    }
    
    .welcome-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .welcome-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.8rem;
        background: linear-gradient(135deg, #00d4ff 0%, #ff007f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .welcome-text {
        color: var(--text-secondary);
        font-size: 1.05rem;
        line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# NUMPY-BASED IMAGE PROCESSING FILTERS (From Scratch)
# =============================================================================

def numpy_convolve2d(image, kernel):
    """Manual 2D convolution using pure NumPy."""
    if len(image.shape) == 3:
        # Process each channel separately for color images
        result = np.zeros_like(image, dtype=np.float64)
        for c in range(image.shape[2]):
            result[:, :, c] = numpy_convolve2d(image[:, :, c], kernel)
        return np.clip(result, 0, 255).astype(np.uint8)
    
    image = image.astype(np.float64)
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    
    # Pad image
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='reflect')
    
    # Output array
    output = np.zeros_like(image, dtype=np.float64)
    
    # Perform convolution
    for i in range(kh):
        for j in range(kw):
            output += kernel[i, j] * padded[i:i+image.shape[0], j:j+image.shape[1]]
    
    return np.clip(output, 0, 255).astype(np.uint8)


def numpy_grayscale(image):
    """Convert to grayscale using luminosity formula."""
    if len(image.shape) == 2:
        return image
    # Y = 0.299*R + 0.587*G + 0.114*B
    return np.dot(image[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)


def numpy_gaussian_blur(image, kernel_size=5, sigma=1.0):
    """Gaussian blur using manually created kernel."""
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    # Create Gaussian kernel
    ax = np.linspace(-(kernel_size // 2), kernel_size // 2, kernel_size)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    kernel = kernel / kernel.sum()
    
    return numpy_convolve2d(image, kernel)


def numpy_box_blur(image, kernel_size=5):
    """Box blur (average filter) using NumPy."""
    if kernel_size % 2 == 0:
        kernel_size += 1
    kernel = np.ones((kernel_size, kernel_size), dtype=np.float64) / (kernel_size * kernel_size)
    return numpy_convolve2d(image, kernel)


def numpy_sharpen(image, strength=1.0):
    """Sharpening filter using NumPy."""
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ], dtype=np.float64)
    
    if strength != 1.0:
        identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.float64)
        kernel = identity + strength * (kernel - identity)
    
    return numpy_convolve2d(image, kernel)


def numpy_sobel_edge(image):
    """Sobel edge detection using NumPy."""
    gray = numpy_grayscale(image)
    
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float64)
    
    gray = gray.astype(np.float64)
    pad_gray = np.pad(gray, ((1, 1), (1, 1)), mode='reflect')
    
    gx = np.zeros_like(gray)
    gy = np.zeros_like(gray)
    
    for i in range(3):
        for j in range(3):
            gx += sobel_x[i, j] * pad_gray[i:i+gray.shape[0], j:j+gray.shape[1]]
            gy += sobel_y[i, j] * pad_gray[i:i+gray.shape[0], j:j+gray.shape[1]]
    
    magnitude = np.sqrt(gx**2 + gy**2)
    magnitude = (magnitude / magnitude.max() * 255).astype(np.uint8) if magnitude.max() > 0 else magnitude.astype(np.uint8)
    return magnitude


def numpy_laplacian(image):
    """Laplacian edge detection using NumPy."""
    gray = numpy_grayscale(image)
    kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float64)
    
    gray = gray.astype(np.float64)
    pad_gray = np.pad(gray, ((1, 1), (1, 1)), mode='reflect')
    
    output = np.zeros_like(gray)
    for i in range(3):
        for j in range(3):
            output += kernel[i, j] * pad_gray[i:i+gray.shape[0], j:j+gray.shape[1]]
    
    output = np.abs(output)
    output = (output / output.max() * 255).astype(np.uint8) if output.max() > 0 else output.astype(np.uint8)
    return output


def numpy_threshold(image, threshold_value=128):
    """Binary thresholding using NumPy."""
    gray = numpy_grayscale(image)
    return ((gray > threshold_value) * 255).astype(np.uint8)


def numpy_invert(image):
    """Invert colors using NumPy."""
    return (255 - image).astype(np.uint8)


def numpy_brightness(image, value=0):
    """Adjust brightness using NumPy."""
    return np.clip(image.astype(np.int16) + value, 0, 255).astype(np.uint8)


def numpy_contrast(image, factor=1.0):
    """Adjust contrast using NumPy."""
    mean = 128
    return np.clip((image.astype(np.float64) - mean) * factor + mean, 0, 255).astype(np.uint8)


def numpy_median_filter(image, kernel_size=3):
    """Median filter for noise removal using NumPy."""
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    pad = kernel_size // 2
    
    if len(image.shape) == 3:
        result = np.zeros_like(image)
        for c in range(image.shape[2]):
            result[:, :, c] = numpy_median_filter(image[:, :, c], kernel_size)
        return result
    
    padded = np.pad(image, pad, mode='reflect')
    output = np.zeros_like(image)
    
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            window = padded[i:i+kernel_size, j:j+kernel_size]
            output[i, j] = np.median(window)
    
    return output.astype(np.uint8)


def numpy_emboss(image):
    """Emboss effect using NumPy."""
    kernel = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]], dtype=np.float64)
    result = numpy_convolve2d(image, kernel)
    return np.clip(result + 128, 0, 255).astype(np.uint8)


def numpy_sepia(image):
    """Sepia tone filter using NumPy."""
    if len(image.shape) == 2:
        image = np.stack([image] * 3, axis=-1)
    
    sepia_matrix = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    
    result = image.dot(sepia_matrix.T)
    return np.clip(result, 0, 255).astype(np.uint8)


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    # Header
    st.markdown("""
    <div class="neon-header">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎨</div>
        <div class="neon-title">DIP-IMAGE-STUDIO</div>
        <div class="neon-subtitle">Digital Image Processing Suite</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; border-bottom: 1px solid rgba(0,212,255,0.2); margin-bottom: 1rem;">
            <div style="font-size: 2rem;">🎨</div>
            <div style="font-family: 'Orbitron', sans-serif; font-size: 1.2rem; background: linear-gradient(135deg, #00d4ff, #ff007f); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">DIP STUDIO</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📤 Step 1: Upload Image")
        uploaded_file = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")
        
        st.markdown("---")
        st.markdown("### 🎛️ Step 2: Select Filter")
        
        filter_category = st.selectbox(
            "Category",
            ["🚫 None", "🎨 Basic", "✨ Enhancement", "🔍 Edge Detection", "🎭 Effects"],
            label_visibility="collapsed"
        )
        
        # Filter selection based on category
        selected_filter = "None"
        filter_params = {}
        
        if filter_category == "🎨 Basic":
            selected_filter = st.selectbox("Filter", ["Grayscale", "Invert", "Threshold"])
            if selected_filter == "Threshold":
                filter_params["threshold"] = st.slider("Threshold Value", 0, 255, 128)
        
        elif filter_category == "✨ Enhancement":
            selected_filter = st.selectbox("Filter", ["Brightness", "Contrast", "Sharpen", "Gaussian Blur", "Box Blur", "Median Filter"])
            if selected_filter == "Brightness":
                filter_params["value"] = st.slider("Brightness", -100, 100, 0)
            elif selected_filter == "Contrast":
                filter_params["factor"] = st.slider("Contrast", 0.5, 2.0, 1.0)
            elif selected_filter == "Sharpen":
                filter_params["strength"] = st.slider("Strength", 0.5, 3.0, 1.0)
            elif selected_filter in ["Gaussian Blur", "Box Blur", "Median Filter"]:
                filter_params["kernel_size"] = st.slider("Kernel Size", 3, 15, 5, step=2)
                if selected_filter == "Gaussian Blur":
                    filter_params["sigma"] = st.slider("Sigma", 0.5, 5.0, 1.0)
        
        elif filter_category == "🔍 Edge Detection":
            selected_filter = st.selectbox("Filter", ["Sobel", "Laplacian"])
        
        elif filter_category == "🎭 Effects":
            selected_filter = st.selectbox("Filter", ["Sepia", "Emboss"])
        
        st.markdown("---")
        st.markdown("### 💾 Step 3: Download")
        st.info("Process an image to enable download")
    
    # Main content area
    if uploaded_file is None:
        st.markdown("""
        <div class="welcome-card">
            <div class="welcome-icon">📷</div>
            <div class="welcome-title">Welcome to DIP Studio</div>
            <div class="welcome-text">
                Upload an image from the sidebar to begin processing.<br>
                Choose from various filters including edge detection,<br>
                blur effects, enhancements, and artistic styles.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Load and process image
        try:
            pil_image = Image.open(uploaded_file)
            image = np.array(pil_image)
            
            # Ensure RGB format
            if len(image.shape) == 2:
                image = np.stack([image] * 3, axis=-1)
            elif image.shape[2] == 4:
                image = image[:, :, :3]
            
            # Apply filter
            processed_image = image.copy()
            
            with st.spinner(f"Applying {selected_filter}..."):
                if selected_filter == "Grayscale":
                    processed_image = numpy_grayscale(image)
                elif selected_filter == "Invert":
                    processed_image = numpy_invert(image)
                elif selected_filter == "Threshold":
                    processed_image = numpy_threshold(image, filter_params.get("threshold", 128))
                elif selected_filter == "Brightness":
                    processed_image = numpy_brightness(image, filter_params.get("value", 0))
                elif selected_filter == "Contrast":
                    processed_image = numpy_contrast(image, filter_params.get("factor", 1.0))
                elif selected_filter == "Sharpen":
                    processed_image = numpy_sharpen(image, filter_params.get("strength", 1.0))
                elif selected_filter == "Gaussian Blur":
                    processed_image = numpy_gaussian_blur(image, filter_params.get("kernel_size", 5), filter_params.get("sigma", 1.0))
                elif selected_filter == "Box Blur":
                    processed_image = numpy_box_blur(image, filter_params.get("kernel_size", 5))
                elif selected_filter == "Median Filter":
                    processed_image = numpy_median_filter(image, filter_params.get("kernel_size", 3))
                elif selected_filter == "Sobel":
                    processed_image = numpy_sobel_edge(image)
                elif selected_filter == "Laplacian":
                    processed_image = numpy_laplacian(image)
                elif selected_filter == "Sepia":
                    processed_image = numpy_sepia(image)
                elif selected_filter == "Emboss":
                    processed_image = numpy_emboss(image)
            
            if selected_filter != "None":
                st.toast(f"✅ {selected_filter} filter applied!", icon="🎨")
            
            # Display images side by side
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="image-card">
                    <div class="card-label label-original">📷 Original</div>
                </div>
                """, unsafe_allow_html=True)
                st.image(image, use_container_width=True)
            
            with col2:
                label = f"🎨 {selected_filter}" if selected_filter != "None" else "🎨 Processed"
                st.markdown(f"""
                <div class="image-card">
                    <div class="card-label label-processed">{label}</div>
                </div>
                """, unsafe_allow_html=True)
                st.image(processed_image, use_container_width=True)
            
            # Download section
            if selected_filter != "None":
                st.markdown("---")
                st.markdown("### 💾 Download Processed Image")
                
                pil_processed = Image.fromarray(processed_image)
                filter_name = selected_filter.lower().replace(" ", "_")
                
                col_d1, col_d2, col_d3 = st.columns(3)
                
                with col_d1:
                    buf = io.BytesIO()
                    pil_processed.save(buf, format='PNG')
                    st.download_button("⬇️ PNG", buf.getvalue(), f"processed_{filter_name}.png", "image/png", use_container_width=True)
                
                with col_d2:
                    buf = io.BytesIO()
                    if pil_processed.mode != 'RGB':
                        pil_processed = pil_processed.convert('RGB')
                    pil_processed.save(buf, format='JPEG', quality=95)
                    st.download_button("⬇️ JPEG", buf.getvalue(), f"processed_{filter_name}.jpg", "image/jpeg", use_container_width=True)
                
                with col_d3:
                    buf = io.BytesIO()
                    pil_processed.save(buf, format='WebP', quality=95)
                    st.download_button("⬇️ WebP", buf.getvalue(), f"processed_{filter_name}.webp", "image/webp", use_container_width=True)
        
        except Exception as e:
            st.error(f"❌ Error processing image: {str(e)}")
    
    # Footer with contributors
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
        <div class="footer-brand">DIP-IMAGE-STUDIO © 2024</div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
