"""
🎨 DIP-IMAGE-STUDIO - Digital Image Processing Suite
=====================================================
Cloud-Optimized Version - Production Ready
Premium Professional Edition
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
except ImportError as e:
    st.error(f"❌ Failed to import required module: {e}")
    st.stop()

# =============================================================================
# CONFIGURATION
# =============================================================================
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
SUPPORTED_FORMATS = ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp']

# =============================================================================
# CSS STYLES - DARK MODE WITH GLASSMORPHISM & PREMIUM ANIMATIONS
# =============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&display=swap');
    
    /* ===== HIDE STREAMLIT BRANDING FOR STANDALONE LOOK ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    :root {
        --bg-void: #0E1117;
        --bg-card: rgba(22, 27, 34, 0.65);
        --glass-border: rgba(0, 212, 255, 0.15);
        --neon-cyan: #00d4ff;
        --neon-pink: #ff007f;
        --gradient-cyber: linear-gradient(135deg, #00d4ff 0%, #ff007f 100%);
        --text-primary: #FAFAFA;
        --text-secondary: #94a3b8;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
    }
    
    * { font-family: 'Rajdhani', sans-serif; }
    
    .stApp {
        background: var(--bg-void);
        background-image: 
            radial-gradient(ellipse at top left, rgba(0, 212, 255, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at bottom right, rgba(255, 0, 127, 0.08) 0%, transparent 50%);
    }
    
    /* ===== GLASSMORPHISM SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(14, 17, 23, 0.85) 0%, rgba(22, 27, 34, 0.9) 100%) !important;
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        border-right: 1px solid rgba(0, 212, 255, 0.2);
        box-shadow: 4px 0 30px rgba(0, 0, 0, 0.5);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdown"] {
        color: var(--text-primary);
    }
    
    .cyber-header {
        text-align: center;
        padding: 2rem 1rem;
        margin-bottom: 2rem;
        background: linear-gradient(180deg, rgba(0, 212, 255, 0.08) 0%, transparent 100%);
        border-radius: var(--radius-xl);
        border: 1px solid var(--glass-border);
    }
    
    .header-icon { font-size: 3rem; margin-bottom: 0.5rem; }
    
    .header-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        background: var(--gradient-cyber);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .header-subtitle {
        color: var(--text-secondary);
        font-size: 1rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }
    
    /* ===== PREMIUM IMAGE CARDS WITH 20PX ROUNDED BORDERS ===== */
    .image-card {
        background: var(--bg-card);
        backdrop-filter: blur(15px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            0 0 20px rgba(0, 212, 255, 0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .image-card:hover {
        transform: translateY(-4px);
        box-shadow: 
            0 12px 40px rgba(0, 0, 0, 0.5),
            0 0 30px rgba(0, 212, 255, 0.1);
    }
    
    .image-badge {
        text-align: center;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    
    .badge-before { color: var(--neon-cyan); }
    .badge-after { color: var(--neon-pink); }
    
    /* ===== FADE-IN ANIMATION FOR PROCESSED IMAGE ===== */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .processed-image-container {
        animation: fadeInUp 0.6s ease-out forwards;
    }
    
    .stButton > button {
        background: var(--gradient-cyber) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: var(--radius-md) !important;
        padding: 0.75rem 1.5rem !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 20px rgba(0, 212, 255, 0.4) !important;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #00ff88, #00cc6a) !important;
        border: none !important;
        color: #0a0d12 !important;
        font-weight: 700 !important;
        border-radius: var(--radius-md) !important;
    }
    
    .welcome-card {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-xl);
        padding: 3rem 2rem;
        text-align: center;
        max-width: 600px;
        margin: 2rem auto;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .welcome-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        background: var(--gradient-cyber);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .welcome-text { color: var(--text-secondary); line-height: 1.8; }
    
    .cyber-footer {
        text-align: center;
        padding: 2rem 1rem;
        margin-top: 3rem;
        border-top: 1px solid var(--glass-border);
        color: var(--text-secondary);
    }
    
    .footer-brand {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.85rem;
        background: var(--gradient-cyber);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* ===== IMAGE STYLING WITH 20PX ROUNDED CORNERS & SHADOWS ===== */
    [data-testid="stImage"] img {
        border-radius: 20px !important;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.4);
    }
    
    /* ===== SIDEBAR SECTION HEADERS ===== */
    .sidebar-section {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--neon-cyan);
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid rgba(0, 212, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# IMAGE PROCESSING FUNCTIONS
# =============================================================================

def convert_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def apply_gaussian_blur(image, kernel_size, sigma):
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)

def apply_box_blur(image, kernel_size):
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.blur(image, (kernel_size, kernel_size))

def apply_median_filter(image, kernel_size):
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.medianBlur(image, kernel_size)

def apply_sharpening(image, strength=1.0):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], dtype=np.float32)
    if strength != 1.0:
        identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.float32)
        kernel = identity + strength * (kernel - identity)
    return cv2.filter2D(image, -1, kernel)

def apply_canny_edge(image, low, high):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)
    return cv2.Canny(blurred, low, high)

def apply_sobel_edge(image, ksize=3):
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

def apply_laplacian(image):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian_abs = np.absolute(laplacian)
    if np.max(laplacian_abs) > 0:
        return np.uint8(255 * laplacian_abs / np.max(laplacian_abs))
    return np.uint8(laplacian_abs)

def apply_threshold(image, threshold_value):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    _, thresholded = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    return thresholded

def apply_adaptive_threshold(image, block_size, c):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    if block_size % 2 == 0:
        block_size += 1
    return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, c)

def adjust_brightness_contrast(image, brightness, contrast):
    return cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)

def apply_inversion(image):
    return cv2.bitwise_not(image)

def apply_histogram_equalization(image):
    if len(image.shape) == 3:
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
    return cv2.equalizeHist(image)

def apply_morphological(image, operation, kernel_size):
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


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    # Header
    st.markdown("""
    <div class="cyber-header">
        <div class="header-icon">🎨</div>
        <div class="header-title">DIP-IMAGE-STUDIO</div>
        <div class="header-subtitle">Digital Image Processing Suite</div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar with Icons
    with st.sidebar:
        st.markdown("## 🎨 DIP-IMAGE-STUDIO")
        st.markdown("---")
        
        # File Upload Section with Icon
        st.markdown('<div class="sidebar-section">📸 Upload Image</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Choose an image",
            type=SUPPORTED_FORMATS,
            help=f"Max size: {MAX_FILE_SIZE_MB}MB",
            label_visibility="collapsed"
        )
        
        # Validate file size
        if uploaded_file and uploaded_file.size > MAX_FILE_SIZE_BYTES:
            st.error(f"⚠️ File too large! Max: {MAX_FILE_SIZE_MB}MB")
            uploaded_file = None
        elif uploaded_file:
            st.success(f"✅ {uploaded_file.name}")
        
        st.markdown("---")
        
        # Filter Selection with Icons
        st.markdown('<div class="sidebar-section">✨ Filter Category</div>', unsafe_allow_html=True)
        filter_category = st.selectbox(
            "Category",
            ["None", "✨ Basic", "🛠️ Edge Detection", "⚡ Advanced"],
            label_visibility="collapsed"
        )
        
        selected_filter = "None"
        filter_params = {}
        
        if filter_category == "✨ Basic":
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
                
        elif filter_category == "🛠️ Edge Detection":
            st.markdown('<div class="sidebar-section">🔍 Edge Filters</div>', unsafe_allow_html=True)
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
                
        elif filter_category == "⚡ Advanced":
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
                filter_params['op'] = st.selectbox("Operation", ["Erosion", "Dilation", "Opening", "Closing"])
                filter_params['ksize'] = st.slider("Kernel Size", 3, 21, 5, step=2)
        
        st.markdown("---")
        if st.button("🔄 Reset All", use_container_width=True):
            st.rerun()

    # Main Content
    if uploaded_file is None:
        st.markdown("""
        <div class="welcome-card">
            <div style="font-size: 4rem;">🖼️</div>
            <div class="welcome-title">READY TO TRANSFORM</div>
            <div class="welcome-text">
                Upload an image using the sidebar to get started.<br><br>
                <strong>Features:</strong> Grayscale, Blur, Edge Detection, Sharpening, Thresholding, and more!
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Process Image with try-except for stability
        try:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            original_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            
            if original_image is None:
                st.error("❌ Could not read the image. Please try a different file.")
            else:
                processed_image = original_image.copy()
                
                # Apply selected filter
                if filter_category != "None" and selected_filter != "None":
                    if selected_filter == "Grayscale":
                        processed_image = convert_to_grayscale(processed_image)
                    elif selected_filter == "Gaussian Blur":
                        processed_image = apply_gaussian_blur(processed_image, filter_params['kernel_size'], filter_params['sigma'])
                    elif selected_filter == "Box Blur":
                        processed_image = apply_box_blur(processed_image, filter_params['kernel_size'])
                    elif selected_filter == "Median Filter":
                        processed_image = apply_median_filter(processed_image, filter_params['kernel_size'])
                    elif selected_filter == "Brightness & Contrast":
                        processed_image = adjust_brightness_contrast(processed_image, filter_params['brightness'], filter_params['contrast'])
                    elif selected_filter == "Invert Colors":
                        processed_image = apply_inversion(processed_image)
                    elif selected_filter == "Canny Edge":
                        processed_image = apply_canny_edge(processed_image, filter_params['low'], filter_params['high'])
                    elif selected_filter == "Sobel Edge":
                        processed_image = apply_sobel_edge(processed_image, filter_params['ksize'])
                    elif selected_filter == "Laplacian Edge":
                        processed_image = apply_laplacian(processed_image)
                    elif selected_filter == "Sharpening":
                        processed_image = apply_sharpening(processed_image, filter_params['strength'])
                    elif selected_filter == "Global Threshold":
                        processed_image = apply_threshold(processed_image, filter_params['threshold'])
                    elif selected_filter == "Adaptive Threshold":
                        processed_image = apply_adaptive_threshold(processed_image, filter_params['block'], filter_params['c'])
                    elif selected_filter == "Histogram Equalization":
                        processed_image = apply_histogram_equalization(processed_image)
                    elif selected_filter == "Morphological Ops":
                        processed_image = apply_morphological(processed_image, filter_params['op'], filter_params['ksize'])
                
                # Convert for display
                original_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
                if len(processed_image.shape) == 2:
                    display_processed = processed_image
                else:
                    display_processed = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
                
                # Display Images Side-by-Side
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="image-card"><div class="image-badge badge-before">📷 Original Image</div>', unsafe_allow_html=True)
                    st.image(original_rgb, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    label = f"🎨 Processed • {selected_filter}" if selected_filter != "None" else "🎨 Processed Image"
                    st.markdown(f'<div class="image-card processed-image-container"><div class="image-badge badge-after">{label}</div>', unsafe_allow_html=True)
                    st.image(display_processed, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Download Section
                if filter_category != "None" and selected_filter != "None":
                    st.markdown("### 💾 Download Processed Image")
                    
                    if len(processed_image.shape) == 2:
                        pil_image = Image.fromarray(processed_image)
                    else:
                        pil_image = Image.fromarray(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB))
                    
                    col_d1, col_d2, col_d3 = st.columns(3)
                    
                    with col_d1:
                        buf = io.BytesIO()
                        pil_image.save(buf, format='PNG')
                        st.download_button("⬇️ PNG", buf.getvalue(), "processed.png", "image/png", use_container_width=True)
                    
                    with col_d2:
                        buf = io.BytesIO()
                        img_rgb = pil_image.convert('RGB') if pil_image.mode != 'RGB' else pil_image
                        img_rgb.save(buf, format='JPEG', quality=95)
                        st.download_button("⬇️ JPEG", buf.getvalue(), "processed.jpg", "image/jpeg", use_container_width=True)
                    
                    with col_d3:
                        buf = io.BytesIO()
                        pil_image.save(buf, format='WebP', quality=95)
                        st.download_button("⬇️ WebP", buf.getvalue(), "processed.webp", "image/webp", use_container_width=True)
        
        except Exception as e:
            st.error(f"❌ Error processing image: {str(e)}")

    # Footer
    st.markdown("""
    <div class="cyber-footer">
        <div class="footer-brand">Developed by Ahmed Elshenawii | DIP-IMAGE-STUDIO © 2024</div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# RUN APP
# =============================================================================
if __name__ == "__main__":
    main()
