"""
🔮 NEXUS STUDIO PRO - Digital Image Processing Suite
=====================================================
A professional-grade image processing application featuring
cyberpunk aesthetics, glassmorphism, and premium UX.

Built with Streamlit & OpenCV
Author: Ahmed El-Shenawi
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import time


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="NEXUS Studio Pro",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =============================================================================
# ULTRA-PREMIUM CYBERPUNK CSS - The "Jamid" Look
# =============================================================================
st.markdown("""
<style>
    /* ===== Import Premium Fonts ===== */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ===== CSS Variables - Cyberpunk Neon Palette ===== */
    :root {
        /* Core Dark Theme */
        --bg-void: #0E1117;
        --bg-deep: #0a0d12;
        --bg-primary: #0E1117;
        --bg-secondary: #161B22;
        --bg-tertiary: #1a1f26;
        --bg-card: rgba(22, 27, 34, 0.65);
        
        /* Glass Effects */
        --glass-bg: rgba(14, 17, 23, 0.7);
        --glass-border: rgba(0, 212, 255, 0.15);
        --glass-hover: rgba(0, 212, 255, 0.25);
        
        /* Neon Accent Colors */
        --neon-cyan: #00d4ff;
        --neon-pink: #ff007f;
        --neon-purple: #a855f7;
        --neon-green: #00ff88;
        --neon-orange: #ff6b35;
        
        /* Gradients */
        --gradient-cyber: linear-gradient(135deg, #00d4ff 0%, #ff007f 100%);
        --gradient-aurora: linear-gradient(135deg, #00d4ff 0%, #a855f7 50%, #ff007f 100%);
        --gradient-pink: linear-gradient(135deg, #ff007f 0%, #ff4d6d 50%, #ff758f 100%);
        --gradient-cyan: linear-gradient(135deg, #00d4ff 0%, #00b4d8 50%, #0096c7 100%);
        --gradient-dark: linear-gradient(180deg, rgba(0,212,255,0.03) 0%, transparent 100%);
        
        /* Text Colors */
        --text-glow: #00d4ff;
        --text-primary: #FAFAFA;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        
        /* Shadows & Glows */
        --shadow-neon-cyan: 0 0 30px rgba(0, 212, 255, 0.4);
        --shadow-neon-pink: 0 0 30px rgba(255, 0, 127, 0.4);
        --shadow-card: 0 8px 32px rgba(0, 0, 0, 0.5);
        --shadow-float: 0 20px 50px rgba(0, 0, 0, 0.6);
        
        /* Border Radius */
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
        --radius-2xl: 24px;
        
        /* Transitions */
        --transition-fast: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-smooth: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-bounce: 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }

    /* ===== Global Styles ===== */
    * {
        font-family: 'Rajdhani', 'Inter', sans-serif;
    }

    .stApp {
        background: var(--bg-void);
        background-image: 
            radial-gradient(ellipse at top left, rgba(0, 212, 255, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at bottom right, rgba(255, 0, 127, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at center, rgba(168, 85, 247, 0.03) 0%, transparent 70%);
        background-attachment: fixed;
    }

    /* Animated Background Grid */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px);
        background-size: 60px 60px;
        pointer-events: none;
        z-index: 0;
    }

    /* ===== SIDEBAR - Advanced Glassmorphism ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(14, 17, 23, 0.85) 0%, rgba(22, 27, 34, 0.9) 100%) !important;
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        border-right: 1px solid var(--glass-border);
        box-shadow: 4px 0 30px rgba(0, 0, 0, 0.5);
    }

    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--gradient-cyber);
        box-shadow: var(--shadow-neon-cyan);
    }

    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
        padding: 1.5rem 1rem;
    }

    /* ===== GLOWING ANIMATED HEADER ===== */
    .cyber-header {
        text-align: center;
        padding: 2.5rem 1.5rem;
        margin-bottom: 2rem;
        background: linear-gradient(180deg, rgba(0, 212, 255, 0.08) 0%, rgba(255, 0, 127, 0.05) 50%, transparent 100%);
        border-radius: var(--radius-2xl);
        border: 1px solid var(--glass-border);
        position: relative;
        overflow: hidden;
    }

    .cyber-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-cyber);
        box-shadow: var(--shadow-neon-cyan);
        animation: glowPulse 2s ease-in-out infinite;
    }

    .cyber-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--neon-cyan), var(--neon-pink), transparent);
    }

    @keyframes glowPulse {
        0%, 100% { opacity: 0.8; box-shadow: 0 0 20px rgba(0, 212, 255, 0.5); }
        50% { opacity: 1; box-shadow: 0 0 40px rgba(0, 212, 255, 0.8), 0 0 60px rgba(255, 0, 127, 0.4); }
    }

    .header-icon {
        font-size: 4rem;
        margin-bottom: 0.5rem;
        animation: float 3s ease-in-out infinite, iconGlow 2s ease-in-out infinite;
        filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.6));
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-12px); }
    }

    @keyframes iconGlow {
        0%, 100% { filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.6)); }
        50% { filter: drop-shadow(0 0 35px rgba(255, 0, 127, 0.8)); }
    }

    .header-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        background: var(--gradient-aurora);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
        animation: textGlow 3s ease-in-out infinite;
        text-shadow: 0 0 40px rgba(0, 212, 255, 0.5);
    }

    @keyframes textGlow {
        0%, 100% { filter: brightness(1) drop-shadow(0 0 10px rgba(0, 212, 255, 0.3)); }
        50% { filter: brightness(1.2) drop-shadow(0 0 20px rgba(255, 0, 127, 0.5)); }
    }

    .header-subtitle {
        font-family: 'Rajdhani', sans-serif;
        color: var(--text-secondary);
        font-size: 1.1rem;
        font-weight: 400;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }

    .header-badge {
        display: inline-block;
        margin-top: 1.5rem;
        padding: 0.5rem 1.5rem;
        background: var(--gradient-cyber);
        border-radius: 50px;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: white;
        box-shadow: var(--shadow-neon-cyan), inset 0 1px 0 rgba(255,255,255,0.2);
        animation: badgePulse 2s ease-in-out infinite;
    }

    @keyframes badgePulse {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.4); }
        50% { box-shadow: 0 0 35px rgba(0, 212, 255, 0.7), 0 0 50px rgba(255, 0, 127, 0.3); }
    }

    /* ===== IMAGE CARDS - Premium Glass Design ===== */
    .image-card {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-xl);
        padding: 1rem;
        box-shadow: var(--shadow-card);
        transition: var(--transition-smooth);
        position: relative;
        overflow: hidden;
    }

    .image-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-cyber);
        opacity: 0;
        transition: var(--transition-smooth);
    }

    .image-card:hover {
        border-color: var(--neon-cyan);
        box-shadow: var(--shadow-card), 0 0 40px rgba(0, 212, 255, 0.15);
        transform: translateY(-5px);
    }

    .image-card:hover::before {
        opacity: 1;
    }

    /* Image Badge */
    .image-badge {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        padding: 0.75rem 1rem;
        margin-bottom: 0.75rem;
        background: linear-gradient(180deg, rgba(0, 212, 255, 0.1) 0%, transparent 100%);
        border-radius: var(--radius-md) var(--radius-md) 0 0;
        border-bottom: 1px solid var(--glass-border);
    }

    .badge-icon {
        font-size: 1.25rem;
    }

    .badge-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--text-primary);
    }

    .badge-before { color: var(--neon-cyan); }
    .badge-after { color: var(--neon-pink); }

    /* ===== Streamlit Image Styling ===== */
    [data-testid="stImage"] {
        border-radius: var(--radius-lg);
        overflow: hidden;
    }

    [data-testid="stImage"] img {
        border-radius: var(--radius-md);
        transition: var(--transition-smooth);
    }

    [data-testid="stImage"]:hover img {
        transform: scale(1.02);
    }

    /* ===== BUTTONS - Neon Glow Effects ===== */
    .stButton > button {
        background: var(--gradient-cyber) !important;
        border: none !important;
        color: white !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 0.05em;
        padding: 0.875rem 1.75rem !important;
        border-radius: var(--radius-md) !important;
        transition: var(--transition-smooth) !important;
        box-shadow: 0 4px 20px rgba(0, 212, 255, 0.4) !important;
        position: relative;
        overflow: hidden;
        width: 100%;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: 0.6s;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-4px) scale(1.03) !important;
        box-shadow: 0 8px 35px rgba(0, 212, 255, 0.6), 0 0 50px rgba(255, 0, 127, 0.3) !important;
    }

    .stButton > button:active {
        transform: translateY(-2px) scale(0.98) !important;
    }

    /* ===== DOWNLOAD BUTTON - Floating Glow ===== */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%) !important;
        border: none !important;
        color: #0a0d12 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.05em;
        border-radius: var(--radius-md) !important;
        box-shadow: 0 4px 20px rgba(0, 255, 136, 0.4) !important;
        transition: var(--transition-smooth) !important;
        width: 100%;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 8px 35px rgba(0, 255, 136, 0.6), 0 0 50px rgba(0, 255, 136, 0.3) !important;
    }

    /* ===== TABS - Cyberpunk Style ===== */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-card);
        backdrop-filter: blur(15px);
        border-radius: var(--radius-lg);
        border: 1px solid var(--glass-border);
        padding: 0.5rem;
        gap: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-secondary) !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.03em;
        padding: 0.75rem 1.25rem !important;
        transition: var(--transition-smooth) !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 212, 255, 0.1) !important;
        color: var(--neon-cyan) !important;
    }

    .stTabs [aria-selected="true"] {
        background: var(--gradient-cyber) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3) !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }

    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* ===== EXPANDER - Glass Style ===== */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        backdrop-filter: blur(15px);
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
        transition: var(--transition-smooth);
    }

    .streamlit-expanderHeader:hover {
        background: rgba(0, 212, 255, 0.1) !important;
        border-color: var(--neon-cyan) !important;
        box-shadow: 0 0 25px rgba(0, 212, 255, 0.15);
    }

    .streamlit-expanderContent {
        background: rgba(14, 17, 23, 0.6) !important;
        border: 1px solid var(--glass-border) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
    }

    /* ===== SELECTBOX & SLIDERS ===== */
    [data-testid="stSelectbox"] > div > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-sm) !important;
        transition: var(--transition-fast);
    }

    [data-testid="stSelectbox"] > div > div:hover {
        border-color: var(--neon-cyan) !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.15);
    }

    [data-testid="stSlider"] label {
        color: var(--text-secondary) !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 500;
    }

    /* Slider Track & Thumb */
    .stSlider > div > div > div > div {
        background: var(--gradient-cyber) !important;
    }

    /* ===== FILE UPLOADER ===== */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.05) 0%, rgba(255, 0, 127, 0.03) 100%);
        border: 2px dashed var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        transition: var(--transition-smooth);
    }

    [data-testid="stFileUploader"]:hover {
        border-color: var(--neon-cyan);
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(255, 0, 127, 0.05) 100%);
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.15);
    }

    /* ===== FLOATING DOWNLOAD CARD ===== */
    .download-card {
        background: linear-gradient(180deg, rgba(0, 255, 136, 0.1) 0%, rgba(0, 212, 255, 0.05) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: var(--radius-xl);
        padding: 1.75rem;
        margin-top: 2rem;
        box-shadow: var(--shadow-card), 0 0 40px rgba(0, 255, 136, 0.1);
        position: relative;
        overflow: hidden;
    }

    .download-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00ff88, #00d4ff);
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
    }

    .download-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(0, 255, 136, 0.2);
    }

    .download-icon {
        font-size: 1.5rem;
        animation: downloadPulse 2s ease-in-out infinite;
    }

    @keyframes downloadPulse {
        0%, 100% { transform: scale(1); filter: drop-shadow(0 0 5px rgba(0, 255, 136, 0.5)); }
        50% { transform: scale(1.1); filter: drop-shadow(0 0 15px rgba(0, 255, 136, 0.8)); }
    }

    .download-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        color: var(--neon-green);
        text-transform: uppercase;
    }

    /* ===== RESULT STATS CARD ===== */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }

    .stat-item {
        text-align: center;
        padding: 1rem 0.75rem;
        background: rgba(0, 212, 255, 0.05);
        border-radius: var(--radius-md);
        border: 1px solid var(--glass-border);
        transition: var(--transition-fast);
    }

    .stat-item:hover {
        border-color: var(--neon-cyan);
        background: rgba(0, 212, 255, 0.1);
    }

    .stat-label {
        color: var(--text-muted);
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.35rem;
    }

    .stat-value {
        color: var(--text-primary);
        font-family: 'Orbitron', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
    }

    /* ===== CUSTOM SPINNER ===== */
    .cyber-spinner {
        text-align: center;
        padding: 3rem;
        background: var(--bg-card);
        backdrop-filter: blur(15px);
        border-radius: var(--radius-xl);
        border: 1px solid var(--glass-border);
    }

    .spinner-ring {
        width: 60px;
        height: 60px;
        margin: 0 auto 1.5rem;
        border: 3px solid transparent;
        border-top-color: var(--neon-cyan);
        border-right-color: var(--neon-pink);
        border-radius: 50%;
        animation: spinnerRotate 1s linear infinite;
    }

    @keyframes spinnerRotate {
        100% { transform: rotate(360deg); }
    }

    .spinner-text {
        font-family: 'Orbitron', sans-serif;
        color: var(--text-secondary);
        font-size: 0.9rem;
        letter-spacing: 0.1em;
        animation: spinnerPulse 1.5s ease-in-out infinite;
    }

    @keyframes spinnerPulse {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }

    /* ===== WELCOME SCREEN ===== */
    .welcome-card {
        background: var(--bg-card);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-2xl);
        padding: 3.5rem 2.5rem;
        text-align: center;
        max-width: 700px;
        margin: 2rem auto;
        box-shadow: var(--shadow-float);
        position: relative;
        overflow: hidden;
    }

    .welcome-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-aurora);
        box-shadow: var(--shadow-neon-cyan);
    }

    .welcome-icon {
        font-size: 5rem;
        margin-bottom: 1.5rem;
        animation: float 3s ease-in-out infinite, iconGlow 2s ease-in-out infinite;
    }

    .welcome-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        background: var(--gradient-cyber);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }

    .welcome-text {
        color: var(--text-secondary);
        font-size: 1.05rem;
        line-height: 1.8;
        margin-bottom: 2rem;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        text-align: left;
    }

    .feature-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem;
        background: rgba(0, 212, 255, 0.05);
        border-radius: var(--radius-md);
        border: 1px solid var(--glass-border);
        transition: var(--transition-fast);
    }

    .feature-item:hover {
        border-color: var(--neon-cyan);
        transform: translateX(5px);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.1);
    }

    .feature-icon {
        font-size: 1.5rem;
        filter: drop-shadow(0 0 8px rgba(0, 212, 255, 0.4));
    }

    .feature-text {
        color: var(--text-secondary);
        font-weight: 500;
        font-size: 0.9rem;
    }

    /* ===== SIDEBAR BRAND ===== */
    .sidebar-brand {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
        border-bottom: 1px solid var(--glass-border);
    }

    .brand-icon {
        font-size: 2.5rem;
        filter: drop-shadow(0 0 15px rgba(0, 212, 255, 0.5));
        animation: iconGlow 2s ease-in-out infinite;
    }

    .brand-name {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        color: var(--text-primary);
        margin-top: 0.5rem;
    }

    .brand-version {
        font-size: 0.7rem;
        color: var(--neon-cyan);
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    /* ===== FOOTER ===== */
    .cyber-footer {
        text-align: center;
        padding: 2.5rem 1rem;
        margin-top: 3rem;
        border-top: 1px solid var(--glass-border);
    }

    .footer-brand {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        background: var(--gradient-cyber);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .footer-tech {
        color: var(--text-muted);
        font-size: 0.75rem;
        margin-top: 0.5rem;
    }

    /* ===== DIVIDER ===== */
    hr {
        border: none !important;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--glass-border), var(--neon-cyan), var(--glass-border), transparent) !important;
        margin: 2rem 0 !important;
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
        background: var(--gradient-cyber);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--neon-cyan);
    }

    /* ===== COLUMN SPACING ===== */
    [data-testid="column"] {
        padding: 0.75rem;
    }

    /* ===== ALERTS ===== */
    .stAlert {
        background: var(--bg-card) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-md) !important;
        backdrop-filter: blur(10px);
    }

    /* ===== SIDEBAR SECTION TITLES ===== */
    [data-testid="stSidebar"] .stMarkdown h2 {
        font-family: 'Orbitron', sans-serif;
        color: var(--text-primary);
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        padding: 0.75rem 0;
        margin: 0.5rem 0;
        border-bottom: 1px solid var(--glass-border);
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# IMAGE PROCESSING FUNCTIONS (OpenCV)
# =============================================================================

def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert image to grayscale using luminosity formula."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def apply_gaussian_blur(image: np.ndarray, kernel_size: int, sigma: float) -> np.ndarray:
    """Apply Gaussian blur filter."""
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)

def apply_box_blur(image: np.ndarray, kernel_size: int) -> np.ndarray:
    """Apply box/average blur filter."""
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.blur(image, (kernel_size, kernel_size))

def apply_median_filter(image: np.ndarray, kernel_size: int) -> np.ndarray:
    """Apply median filter for noise reduction."""
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.medianBlur(image, kernel_size)

def apply_sharpening(image: np.ndarray, strength: float = 1.0) -> np.ndarray:
    """Apply sharpening filter with adjustable strength."""
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], dtype=np.float32)
    if strength != 1.0:
        identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.float32)
        kernel = identity + strength * (kernel - identity)
    return cv2.filter2D(image, -1, kernel)

def apply_canny_edge(image: np.ndarray, low_threshold: int, high_threshold: int) -> np.ndarray:
    """Apply Canny edge detection."""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)
    return cv2.Canny(blurred, low_threshold, high_threshold)

def apply_sobel_edge(image: np.ndarray, ksize: int = 3) -> np.ndarray:
    """Apply Sobel edge detection."""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
    magnitude = np.sqrt(sobelx**2 + sobely**2)
    return np.uint8(255 * magnitude / np.max(magnitude)) if np.max(magnitude) > 0 else np.uint8(magnitude)

def apply_laplacian(image: np.ndarray) -> np.ndarray:
    """Apply Laplacian edge detection."""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian_abs = np.absolute(laplacian)
    return np.uint8(255 * laplacian_abs / np.max(laplacian_abs)) if np.max(laplacian_abs) > 0 else np.uint8(laplacian_abs)

def apply_threshold(image: np.ndarray, threshold_value: int) -> np.ndarray:
    """Apply global thresholding."""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    _, thresholded = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    return thresholded

def apply_adaptive_threshold(image: np.ndarray, block_size: int, c: int) -> np.ndarray:
    """Apply adaptive thresholding."""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    if block_size % 2 == 0:
        block_size += 1
    return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, c)

def adjust_brightness_contrast(image: np.ndarray, brightness: int, contrast: float) -> np.ndarray:
    """Adjust image brightness and contrast."""
    return cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)

def apply_inversion(image: np.ndarray) -> np.ndarray:
    """Invert image colors."""
    return cv2.bitwise_not(image)

def apply_histogram_equalization(image: np.ndarray) -> np.ndarray:
    """Apply histogram equalization for contrast enhancement."""
    if len(image.shape) == 3:
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
    return cv2.equalizeHist(image)

def apply_morphological(image: np.ndarray, operation: str, kernel_size: int) -> np.ndarray:
    """Apply morphological operations (erosion, dilation, opening, closing)."""
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
    # =========================================================================
    # ANIMATED CYBER HEADER
    # =========================================================================
    st.markdown("""
    <div class="cyber-header">
        <div class="header-icon">🔮</div>
        <div class="header-title">NEXUS STUDIO</div>
        <div class="header-subtitle">Ultra-Premium Image Processing Suite</div>
        <div class="header-badge">⚡ PRO EDITION v3.0</div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================================================
    # SESSION STATE
    # =========================================================================
    if 'processing' not in st.session_state:
        st.session_state.processing = False

    # =========================================================================
    # SIDEBAR - GLASSMORPHISM CONTROL CENTER
    # =========================================================================
    with st.sidebar:
        # Brand Logo
        st.markdown("""
        <div class="sidebar-brand">
            <div class="brand-icon">🔮</div>
            <div class="brand-name">NEXUS</div>
            <div class="brand-version">PRO v3.0</div>
        </div>
        """, unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # 📸 INPUT SECTION
        # ---------------------------------------------------------------------
        with st.expander("📸 IMAGE INPUT", expanded=True):
            uploaded_file = st.file_uploader(
                "Drop your image",
                type=['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp'],
                help="Supported: PNG, JPG, JPEG, BMP, TIFF, WebP",
                key="uploader"
            )
            
            if uploaded_file:
                st.success(f"✅ {uploaded_file.name}")

        # Process uploaded image
        original_image = None
        file_size = 0
        file_format = "N/A"

        if uploaded_file is not None:
            file_size = uploaded_file.size
            file_format = uploaded_file.name.split('.')[-1].upper()
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            original_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # ---------------------------------------------------------------------
        # ✨ FILTERS - ORGANIZED WITH TABS
        # ---------------------------------------------------------------------
        st.markdown("## ✨ FILTERS")
        
        filter_tabs = st.tabs(["🎨 Basic", "🔍 Edges", "⚡ Advanced"])
        
        selected_filter = None
        filter_params = {}
        filter_category = "None"

        # TAB 1: Basic Filters
        with filter_tabs[0]:
            basic_filter = st.selectbox(
                "Select Filter",
                ["None", "Grayscale", "Gaussian Blur", "Box Blur", 
                 "Median Filter", "Brightness & Contrast", "Invert Colors"],
                key="basic_filter"
            )
            
            if basic_filter != "None":
                filter_category = "Basic"
                selected_filter = basic_filter
                
                if basic_filter == "Gaussian Blur":
                    filter_params['kernel_size'] = st.slider("🔘 Intensity", 3, 31, 5, step=2, key="g_k")
                    filter_params['sigma'] = st.slider("🌀 Sigma", 0.1, 10.0, 1.5, step=0.1, key="g_s")
                elif basic_filter == "Box Blur":
                    filter_params['kernel_size'] = st.slider("🔘 Intensity", 3, 31, 5, step=2, key="b_k")
                elif basic_filter == "Median Filter":
                    filter_params['kernel_size'] = st.slider("🔘 Kernel Size", 3, 31, 5, step=2, key="m_k")
                elif basic_filter == "Brightness & Contrast":
                    filter_params['brightness'] = st.slider("☀️ Brightness", -100, 100, 0, key="br")
                    filter_params['contrast'] = st.slider("🌓 Contrast", 0.5, 3.0, 1.0, step=0.1, key="ct")

        # TAB 2: Edge Detection
        with filter_tabs[1]:
            edge_filter = st.selectbox(
                "Select Edge Detector",
                ["None", "Canny Edge", "Sobel Edge", "Laplacian Edge"],
                key="edge_filter"
            )
            
            if edge_filter != "None":
                filter_category = "Edge Detection"
                selected_filter = edge_filter
                
                if edge_filter == "Canny Edge":
                    filter_params['low'] = st.slider("📉 Low Threshold", 0, 200, 50, key="c_l")
                    filter_params['high'] = st.slider("📈 High Threshold", 50, 400, 150, key="c_h")
                elif edge_filter == "Sobel Edge":
                    filter_params['ksize'] = st.slider("🔘 Kernel Size", 1, 7, 3, step=2, key="s_k")

        # TAB 3: Advanced Filters
        with filter_tabs[2]:
            adv_filter = st.selectbox(
                "Select Advanced Filter",
                ["None", "Sharpening", "Global Threshold", "Adaptive Threshold",
                 "Histogram Equalization", "Morphological Ops"],
                key="adv_filter"
            )
            
            if adv_filter != "None":
                filter_category = "Advanced"
                selected_filter = adv_filter
                
                if adv_filter == "Sharpening":
                    filter_params['strength'] = st.slider("⚡ Strength", 0.5, 5.0, 1.0, step=0.1, key="sh")
                elif adv_filter == "Global Threshold":
                    filter_params['threshold'] = st.slider("🎚️ Threshold Value", 0, 255, 127, key="th")
                elif adv_filter == "Adaptive Threshold":
                    filter_params['block'] = st.slider("📦 Block Size", 3, 99, 11, step=2, key="ab")
                    filter_params['c'] = st.slider("📐 Constant (C)", -20, 20, 2, key="ac")
                elif adv_filter == "Morphological Ops":
                    filter_params['op'] = st.selectbox(
                        "Operation Type", 
                        ["Erosion", "Dilation", "Opening", "Closing"], 
                        key="mo"
                    )
                    filter_params['ksize'] = st.slider("🔘 Kernel Size", 3, 21, 5, step=2, key="mk")

        # ---------------------------------------------------------------------
        # ⚙️ SETTINGS
        # ---------------------------------------------------------------------
        st.markdown("---")
        
        with st.expander("⚙️ SETTINGS", expanded=False):
            if st.button("🔄 Reset All Filters", key="reset", use_container_width=True):
                st.session_state.basic_filter = "None"
                st.session_state.edge_filter = "None"
                st.session_state.adv_filter = "None"
                st.rerun()

    # =========================================================================
    # MAIN CONTENT AREA
    # =========================================================================
    
    if uploaded_file is None or original_image is None:
        # Welcome Screen
        st.markdown("""
        <div class="welcome-card">
            <div class="welcome-icon">🖼️</div>
            <div class="welcome-title">READY TO TRANSFORM</div>
            <div class="welcome-text">
                Upload an image to unlock the full power of NEXUS Studio Pro.
                Experience professional-grade image processing with stunning filters and real-time preview.
            </div>
            <div class="feature-grid">
                <div class="feature-item">
                    <span class="feature-icon">🎨</span>
                    <span class="feature-text">Basic Filters & Effects</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">🔍</span>
                    <span class="feature-text">Edge Detection</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">⚡</span>
                    <span class="feature-text">Advanced Processing</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">💾</span>
                    <span class="feature-text">Multi-Format Export</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # =========================================================================
    # APPLY FILTER WITH STYLISH PROCESSING ANIMATION
    # =========================================================================
    processed_image = original_image.copy()
    filter_applied = "None"

    if filter_category != "None" and selected_filter and selected_filter != "None":
        filter_applied = selected_filter
        
        # Show processing animation
        with st.spinner(""):
            # Create stylish processing indicator
            processing_placeholder = st.empty()
            processing_placeholder.markdown("""
            <div class="cyber-spinner">
                <div class="spinner-ring"></div>
                <div class="spinner-text">⚡ PROCESSING IMAGE ⚡</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Simulate processing time for effect
            time.sleep(0.4)
            
            # Apply filters
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
            
            # Clear processing indicator
            processing_placeholder.empty()

    # =========================================================================
    # DISPLAY IMAGES - SIDE BY SIDE WITH BADGES
    # =========================================================================
    
    # Convert for display
    original_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    if len(processed_image.shape) == 2:
        display_processed = processed_image
    else:
        display_processed = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)

    # Side-by-side comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="image-card">
            <div class="image-badge">
                <span class="badge-icon">📷</span>
                <span class="badge-text badge-before">BEFORE</span>
            </div>
        """, unsafe_allow_html=True)
        st.image(original_rgb, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        badge_label = f"AFTER • {filter_applied}" if filter_applied != "None" else "AFTER"
        st.markdown(f"""
        <div class="image-card">
            <div class="image-badge">
                <span class="badge-icon">🎨</span>
                <span class="badge-text badge-after">{badge_label}</span>
            </div>
        """, unsafe_allow_html=True)
        st.image(display_processed, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # FLOATING DOWNLOAD SECTION
    # =========================================================================
    if filter_category != "None" and selected_filter and selected_filter != "None":
        height, width = original_image.shape[:2]
        proc_h, proc_w = processed_image.shape[:2]
        channels = 1 if len(processed_image.shape) == 2 else processed_image.shape[2]
        
        st.markdown(f"""
        <div class="download-card">
            <div class="download-header">
                <span class="download-icon">✅</span>
                <span class="download-title">Processing Complete - Ready to Export</span>
            </div>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-label">Dimensions</div>
                    <div class="stat-value">{proc_w} × {proc_h}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Filter</div>
                    <div class="stat-value">{filter_applied}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Color Mode</div>
                    <div class="stat-value">{'Grayscale' if channels == 1 else 'RGB'}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Original Size</div>
                    <div class="stat-value">{file_size / 1024:.1f} KB</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Convert for export
        if len(processed_image.shape) == 2:
            pil_image = Image.fromarray(processed_image)
        else:
            pil_image = Image.fromarray(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB))
        
        # Download buttons
        st.markdown("### 💾 EXPORT OPTIONS")
        
        col_d1, col_d2, col_d3 = st.columns(3)
        
        with col_d1:
            buf_png = io.BytesIO()
            pil_image.save(buf_png, format='PNG', optimize=True)
            st.download_button(
                "⬇️ DOWNLOAD PNG", 
                buf_png.getvalue(), 
                "nexus_processed.png", 
                "image/png", 
                key="dl_png",
                use_container_width=True
            )
        
        with col_d2:
            buf_jpg = io.BytesIO()
            img_jpg = pil_image.convert('RGB') if pil_image.mode != 'RGB' else pil_image
            img_jpg.save(buf_jpg, format='JPEG', quality=95)
            st.download_button(
                "⬇️ DOWNLOAD JPEG", 
                buf_jpg.getvalue(), 
                "nexus_processed.jpg", 
                "image/jpeg", 
                key="dl_jpg",
                use_container_width=True
            )
        
        with col_d3:
            buf_webp = io.BytesIO()
            pil_image.save(buf_webp, format='WebP', quality=95)
            st.download_button(
                "⬇️ DOWNLOAD WEBP", 
                buf_webp.getvalue(), 
                "nexus_processed.webp", 
                "image/webp", 
                key="dl_webp",
                use_container_width=True
            )

    # =========================================================================
    # FOOTER
    # =========================================================================
    st.markdown("""
    <div class="cyber-footer">
        <div class="footer-brand">🔮 NEXUS STUDIO PRO</div>
        <div class="footer-tech">Powered by Streamlit • OpenCV • NumPy</div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
