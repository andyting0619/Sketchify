import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import base64

st.set_page_config(
    page_title="Sketchify - Pencil Sketch Generator",
    page_icon="✏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Title styling */
    .main-title {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(45deg, #00d4ff, #0099cc, #0066ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
    }
    
    .subtitle {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.2rem !important;
        color: #8892b0;
        text-align: center;
        margin-bottom: 1.1rem;
        font-weight: 500;
    }
            
    .developer-credit {
        font-family: 'Orbitron', 'Rajdhani', sans-serif;
        font-size: 1.0rem !important;
        color: #64ffda;
        text-align: center;
        letter-spacing: 1px;
    }
        
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #0a0e1a 0%, #1a1f2e 100%);
        border-right: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    /* Parameter sections */
    .param-section {
        background: rgba(17, 25, 40, 0.6);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        backdrop-filter: blur(10px);
    }
    
    .param-title {
        font-family: 'Orbitron', monospace;
        font-size: 1.1rem;
        font-weight: 700;
        color: #00d4ff;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .param-description {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.9rem;
        color: #8892b0;
        margin-bottom: 15px;
        line-height: 1.4;
    }
    
    /* Rail & track */
    .stSlider .rc-slider-rail {
    background: linear-gradient(90deg, #0066ff, #00d4ff) !important;
    height: 8px !important;
    border-radius: 10px !important;
    }
            
    .stSlider .rc-slider-track {
    background: linear-gradient(90deg, #0066ff, #00d4ff) !important;
    height: 8px !important;
    border-radius: 10px !important;
    }

    /* Handle */
    .stSlider .rc-slider-handle {
    background: transparent !important;
    border: none           !important;
    box-shadow: none       !important;
    width: 12px            !important;
    height: 12px           !important;
    margin-top: -2px       !important;
    }

    /* Tooltip (number bubble) */
    .stSlider .rc-slider-handle .rc-slider-tooltip,
    .stSlider .rc-slider-tooltip-inner,
    .stSlider .rc-slider-tooltip-arrow {
    display: none !important;
    visibility: hidden   !important;
    opacity: 0           !important;
    pointer-events: none !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #0066ff, #00d4ff);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 2rem;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 102, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.4);
        background: linear-gradient(45deg, #0080ff, #00e6ff);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Upload button special styling */
    .stFileUploader > div > div > div > button {
        background: linear-gradient(45deg, #ff6b35, #ff8e53);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.8rem 2rem;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
    }
    
    .stFileUploader > div > div > div > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 142, 83, 0.4);
        background: linear-gradient(45deg, #ff8e53, #ffab76);
    }
    
    /* Download button styling */
    .download-button {
        background: linear-gradient(45deg, #00ff88, #00cc6a);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.8rem 2rem;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 255, 136, 0.3);
        cursor: pointer;
        text-decoration: none !important;
        display: inline-block;
        text-align: center;
        margin: 10px 0;
    }
    
    .download-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 204, 106, 0.4);
        background: linear-gradient(45deg, #00cc6a, #00ff88);
        text-decoration: none;
        color: white;
    }
    
    /* Image containers */
    .image-container {
        border: 2px solid rgba(0, 212, 255, 0.3);
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        background: rgba(17, 25, 40, 0.3);
        height: 400px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .image-container img {
        max-height: 100%;
        max-width: 100%;
        object-fit: contain;
    }
    
    /* Upload section centering */
    .upload-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin: 2rem 0;
    }
    
    /* Progress bar styling */
    .stProgress .st-bo {
        background: linear-gradient(90deg, #0066ff, #00d4ff);
        border-radius: 10px;
    }
    
    /* Info box styling */
    .info-box {
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        font-family: 'Rajdhani', sans-serif;
        color: #64ffda;
    }
    
    /* Hiding streamlit elements */
    .css-1rs6os, .css-17ziqus {
        visibility: hidden;
    }
    
    .css-1v0mbdj > img {
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)


def pencil_sketch_enhanced(img_array, blur_kernel, edge_threshold, texture_strength, shading_intensity, paper_texture, line_density):
    if len(img_array.shape) == 2:
        gray_img = img_array
    elif len(img_array.shape) == 3 and img_array.shape[2] == 3:
        gray_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    elif len(img_array.shape) == 3 and img_array.shape[2] == 4:
        # Handle RGBA by dropping alpha channel
        rgb_img = img_array[:, :, :3]
        gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2GRAY)

    # Apply bilateral filter to reduce noise while keeping edges sharp
    smooth_img = cv2.bilateralFilter(gray_img, 9, 75, 75)

    # Create base sketch using improved dodge blend technique
    inv_gray = 255 - smooth_img
    blur_inv = cv2.GaussianBlur(inv_gray, (blur_kernel, blur_kernel), 0)

    # Improved dodge blend with better brightness control
    dodge_blend = cv2.divide(smooth_img, 255 - blur_inv, scale=256.0)

    # Enhance the sketch with gamma correction for better visibility
    gamma = 1.2
    dodge_blend = np.power(dodge_blend / 255.0, gamma) * 255
    dodge_blend = dodge_blend.astype(np.uint8)

    # Edge detection using adaptive threshold
    edges = cv2.adaptiveThreshold(
        smooth_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, edge_threshold)

    # Blend edges with base sketch more subtly
    edges_weight = 0.7  # Reduce edge intensity
    sketch_base = cv2.addWeighted(
        dodge_blend, 1.0, 255 - edges, edges_weight * 0.3, 0)

    # Add controlled texture
    if texture_strength > 0:
        # Create subtle texture noise
        np.random.seed(42)  # For consistent results
        noise = np.random.normal(
            0, texture_strength * 2, gray_img.shape).astype(np.int16)
        sketch_base = np.clip(sketch_base.astype(
            np.int16) + noise, 0, 255).astype(np.uint8)

    # Enhance shading with gradient-based approach (reduced intensity)
    if shading_intensity > 0:
        # Calculate gradients
        grad_x = cv2.Sobel(smooth_img, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(smooth_img, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        gradient_magnitude = cv2.normalize(
            gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        # Apply gradient shading more subtly
        shading_factor = shading_intensity / 200.0  # Reduced from 100
        shading_mask = (gradient_magnitude * shading_factor).astype(np.uint8)
        sketch_base = cv2.subtract(sketch_base, shading_mask)

    # Add paper texture effect
    if paper_texture:
        h, w = sketch_base.shape
        np.random.seed(123)  # For consistent results
        paper = np.random.uniform(0.98, 1.02, (h, w))  # Subtle texture
        sketch_base = np.clip(sketch_base * paper, 0, 255).astype(np.uint8)

    # Adjust line density
    if line_density != 1.0:
        # Apply line density adjustment more carefully
        adjusted_density = np.clip(line_density, 0.5, 1.0)
        sketch_base = cv2.convertScaleAbs(
            sketch_base, alpha=adjusted_density, beta=0)

    # Final enhancement with controlled histogram equalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    sketch_final = clahe.apply(sketch_base)

    # Ensure the result is not too dark
    sketch_final = cv2.convertScaleAbs(sketch_final, alpha=1.1, beta=10)

    # Final smooth
    sketch_final = cv2.GaussianBlur(sketch_final, (3, 3), 0)

    return sketch_final


def create_download_link(img_array, filename="sketchify_output.png"):
    img_pil = Image.fromarray(img_array)

    # Convert to bytes
    buf = io.BytesIO()
    img_pil.save(buf, format='PNG')
    byte_data = buf.getvalue()

    # Create base64 string
    b64 = base64.b64encode(byte_data).decode()

    # Create download link
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}" class="download-button">📥 Download Sketch</a>'
    return href


def main():
    st.markdown('<h1 class="main-title">SKETCHIFY</h1>',
                unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Enhanced Pencil Sketch Generator without Artificial Intelligence (AI)</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="developer-credit">Developed by Andy Ting Zhi Wei</p>',
                unsafe_allow_html=True)

    # Sidebar for parameters
    st.sidebar.markdown("## ⚙️ Sketch Parameters")

    # Basic Controls Section
    st.sidebar.markdown("""
    <div class="param-section">
        <div class="param-title">🎨 Basic Controls</div>
        <div class="param-description">
            Fundamental parameters that control the overall sketch appearance
        </div>
    </div>
    """, unsafe_allow_html=True)

    blur_kernel = st.sidebar.slider(
        "Blur Kernel Size",
        min_value=51, max_value=251, value=121, step=10,
        help="Controls the softness of the sketch. Higher values create softer, more artistic strokes."
    )

    line_density = st.sidebar.slider(
        "Line Density",
        min_value=0.5, max_value=1.0, value=0.8, step=0.1,
        help="Adjusts the darkness and intensity of pencil lines. Lower values create darker, more prominent lines."
    )

    st.sidebar.markdown("""
    <div class="param-section">
        <div class="param-title">🔍 Edge Enhancement</div>
        <div class="param-description">
            Controls how prominent edges and outlines appear in your sketch
        </div>
    </div>
    """, unsafe_allow_html=True)

    edge_threshold = st.sidebar.slider(
        "Edge Threshold",
        min_value=1, max_value=20, value=10, step=1,
        help="Determines edge sensitivity. Lower values detect more edges, higher values focus on stronger edges only."
    )

    st.sidebar.markdown("""
    <div class="param-section">
        <div class="param-title">🎭 Artistic Effects</div>
        <div class="param-description">
            Add realistic pencil drawing effects and textures
        </div>
    </div>
    """, unsafe_allow_html=True)

    texture_strength = st.sidebar.slider(
        "Texture Strength",
        min_value=0, max_value=20, value=10, step=1,
        help="Adds paper grain texture to simulate real pencil on paper. 0 = smooth, 20 = very textured."
    )

    shading_intensity = st.sidebar.slider(
        "Shading Intensity",
        min_value=0, max_value=50, value=25, step=1,
        help="Controls depth and shadow effects. Higher values create more dramatic shading and dimensionality."
    )

    paper_texture = st.sidebar.checkbox(
        "Paper Texture Effect",
        value=True,
        help="Simulates drawing on textured paper surface for more realistic appearance."
    )

    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### 📤 Upload Your Image")
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=['png', 'jpg', 'jpeg'],
        help="Upload any image to transform it into a pencil sketch"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📷 Original Image")
            image = Image.open(uploaded_file)
            st.image(image, caption="Original Image", use_container_width=True)

        with col2:
            st.markdown("### ✏️ Pencil Sketch Result")

            img_array = np.array(image)

            with st.spinner('🎨 Creating your pencil sketch...'):
                sketch = pencil_sketch_enhanced(
                    img_array,
                    blur_kernel,
                    edge_threshold,
                    texture_strength,
                    shading_intensity,
                    paper_texture,
                    line_density
                )

            st.image(sketch, caption="Generated Pencil Sketch",
                     use_container_width=True)

        st.markdown(create_download_link(sketch), unsafe_allow_html=True)
        st.success(
            "✅ Pencil sketch generated successfully! Click the Download Sketch buttom to download the pencil sketch!")
    else:
        st.markdown("""
        <div class="info-box">
            <h3>🚀 How to Use Sketchify</h3>
            <p>1. Upload an image using the file uploader above.</p>
            <p>2. Adjust the parameters in the sidebar to customize your sketch.</p>
            <p>3. Watch as your sketch updates in real-time.</p>
            <p>4. Download your finished artwork when satisfied.</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
