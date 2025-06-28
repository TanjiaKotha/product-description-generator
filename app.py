import streamlit as st
from description_generator import DescriptionGenerator
from seo_tools import extract_keywords, generate_meta_description, calculate_readability
import time

# Configure page
st.set_page_config(
    page_title="🌟 AI Product Description Generator",
    page_icon=":shopping_bags:",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom Dark Mode CSS (unchanged)
st.markdown("""
<style>
    /* Base dark theme */
    [data-testid="stAppViewContainer"] {
        background: rgba(15, 15, 35, 0.9);
        color: #ffffff;
    }
    
    /* Headers */
    h1 {
        color: #ff4d4d !important;
        text-shadow: 0 0 8px rgba(255, 77, 77, 0.5);
        font-weight: 800 !important;
    }
    h2, h3, h4, h5, h6 {
        color: #ff6666 !important;
    }
    
    /* Text elements */
    p, div, span, label {
        color: #ffffff !important;
    }
    
    /* Input fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(30, 30, 46, 0.8) !important;
        color: white !important;
        border: 1px solid #4f46e5;
        border-radius: 10px;
        padding: 12px;
        box-shadow: 0 0 10px rgba(79, 70, 229, 0.3);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(to right, #ff4d4d, #ff1a1a);
        color: white !important;
        font-weight: bold;
        border: none;
        padding: 12px 24px;
        border-radius: 10px;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(255, 77, 77, 0.4);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255, 77, 77, 0.6);
        background: linear-gradient(to right, #ff3333, #ff0000);
    }
    
    /* Cards */
    .result-card {
        background: rgba(23, 23, 37, 0.8);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border-left: 4px solid #ff4d4d;
        backdrop-filter: blur(4px);
        -webkit-backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    .metric-card {
        background: rgba(23, 23, 37, 0.8);
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 30, 46, 0.7) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #ff4d4d, #7c3aed) !important;
        color: white !important;
        font-weight: bold;
        box-shadow: 0 0 15px rgba(255, 77, 77, 0.5);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 15, 35, 0.9) !important;
        border-right: 1px solid #4f46e5;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem;
        margin-top: 2rem;
        color: #a0a0c0;
        font-size: 0.9rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(15, 15, 35, 0.8);
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(#ff4d4d, #7c3aed);
        border-radius: 4px;
    }
    
    # /* Glowing effect for headers */
    # .glow {
    #     text-shadow: 0 0 10px #ff4d4d, 0 0 20px #ff4d4d, 0 0 30px #ff4d4d;
    #     animation: glow 1.5s ease-in-out infinite alternate;
    # }
    
    # @keyframes glow {
    #     from {
    #         text-shadow: 0 0 5px #ff4d4d, 0 0 10px #ff4d4d;
    #     }
    #     to {
    #         text-shadow: 0 0 15px #ff4d4d, 0 0 20px #ff4d4d, 0 0 25px #ff4d4d;
    #     }
    # }
</style>
""", unsafe_allow_html=True)

# App header with glowing effect
st.markdown('<h1 class="glow">🌟 AI PRODUCT DESCRIPTION GENERATOR</h1>', unsafe_allow_html=True)
st.markdown("Create professional, SEO-optimized descriptions for any product in seconds")

# Initialize generator
@st.cache_resource
def load_generator():
    return DescriptionGenerator()

generator = load_generator()

# Sidebar for advanced options
with st.sidebar:
    st.header("⚙️ Product Details")
    product_type = st.selectbox("Product Category", 
                       ["Electronics", "Clothing", "Home & Kitchen", 
                        "Beauty", "Sports", "Books", "Toys", "Other"],
                       index=0)
    
    st.divider()
    st.header("🎚️ Content Settings")
    tone = st.selectbox("Description Tone", 
                       ["Professional", "Friendly", "Technical", "Persuasive"],
                       index=0)
    
    target_audience = st.selectbox("Target Audience",
                                  ["General Consumers", "Enthusiasts", "Business Buyers"],
                                  index=0)
    
    st.divider()
    st.header("🔍 SEO Focus")
    seo_focus = st.multiselect("Priority Keywords",
                              ["Performance", "Quality", "Value", "Innovation", "Durability"],
                              ["Performance", "Quality"])
    
    st.divider()
    
    # Proxy status indicator
    st.caption("SYSTEM STATUS")
    proxy_status = st.empty()
    
    # Replace the existing clear session button code with:

    st.divider()
    if st.button("Clear Session", type="secondary", key="clear_session_btn"):
        st.session_state.clear_session_confirm = True

    if st.session_state.get('clear_session_confirm'):
        st.warning("Are you sure? This will erase all generated content")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, Clear Everything", key="confirm_clear"):
                st.session_state.clear()
                st.session_state.clear_session_confirm = False
                st.rerun()
        with col2:
            if st.button("Cancel", key="cancel_clear"):
                st.session_state.clear_session_confirm = False

# Main content
tab1, tab2 = st.tabs(["✨ GENERATOR", "📊 SEO ANALYSIS"])

with tab1:
    with st.form("product_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(
                "**PRODUCT NAME**", 
                placeholder="e.g., Premium Wireless Headphones",
                help="Enter the product name"
            )
        with col2:
            brand = st.text_input(
                "**BRAND**", 
                placeholder="e.g., Sony",
                help="Manufacturer or brand name"
            )
        
        features = st.text_area(
            "**KEY FEATURES**", 
            placeholder="e.g., Noise cancellation, 30hr battery life, Bluetooth 5.0",
            height=130,
            help="Separate features with commas"
        )
        
        submitted = st.form_submit_button("🚀 GENERATE DESCRIPTION", use_container_width=True)
    
    # Processing and output
    if submitted:
        if not name or not features:
            st.warning("Please fill in both Product Name and Key Features fields")
        else:
            with st.spinner("Generating professional description..."):
                start_time = time.time()
                
                # Combine inputs
                full_name = f"{brand} {name}" if brand else name
                
                # Show proxy status
                proxy_status.info(f"Using AI provider: {generator.current_proxy.split('//')[1].split('/')[0]}")
                
                # Generate description
                # app.py (line ~240)
                description = generator.generate_description(
                    product_name=full_name, 
                    features=features,
                    product_type=product_type.lower()
                )
                
                # SEO processing
                keywords = extract_keywords(description)
                meta_desc = generate_meta_description(description)
                readability = calculate_readability(description)
                
                elapsed = time.time() - start_time
                
                # Display results
                st.success(f"✅ Description generated in {elapsed:.1f} seconds")
                
                st.divider()
                st.subheader("PROFESSIONAL DESCRIPTION")
                st.markdown(f'<div class="result-card">{description}</div>', unsafe_allow_html=True)
                
                # Export options
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="💾 DOWNLOAD TEXT",
                        data=description,
                        file_name=f"{full_name.replace(' ', '_')}_description.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with col2:
                    if st.button("📋 COPY TO CLIPBOARD", use_container_width=True):
                        st.session_state.copied = True
                        st.toast("Copied to clipboard!")
                
                # Store in session for SEO tab
                st.session_state.description = description
                st.session_state.keywords = keywords
                st.session_state.meta_desc = meta_desc
                st.session_state.readability = readability

with tab2:
    if 'description' in st.session_state:
        st.subheader("📊 SEO ANALYSIS")
        
        # SEO metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="metric-card"><h3>🔑 KEYWORDS</h3><p style="font-size:24px;margin:0;color:#ff6666">{len(st.session_state.keywords)}</p></div>', 
                       unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><h3>📖 READABILITY</h3><p style="font-size:24px;margin:0;color:#ff6666">{st.session_state.readability:.0f}/100</p></div>', 
                       unsafe_allow_html=True)
        with col3:
            char_count = len(st.session_state.description)
            st.markdown(f'<div class="metric-card"><h3>📏 LENGTH</h3><p style="font-size:24px;margin:0;color:#ff6666">{char_count} chars</p></div>', 
                       unsafe_allow_html=True)
        
        # SEO recommendations
        st.subheader("🔝 TOP KEYWORDS")
        st.write("These are the most important phrases for SEO:")
        for i, keyword in enumerate(st.session_state.keywords[:5]):
            st.markdown(f"<div style='background: rgba(79, 70, 229, 0.2); padding: 10px; border-radius: 8px; margin: 5px 0;'>"
                        f"{i+1}. <strong style='color:#ff9999'>{keyword}</strong></div>", 
                        unsafe_allow_html=True)
        
        st.subheader("🔍 META DESCRIPTION")
        st.markdown(f'<div class="result-card">{st.session_state.meta_desc}</div>', unsafe_allow_html=True)
        
        st.subheader("💡 OPTIMIZATION TIPS")
        st.markdown("""
        - **✨ Include keywords** in product title and first paragraph
        - **📌 Use bullet points** for key features
        - **📊 Add specifications** table with technical details
        - **⭐ Include customer reviews** and ratings
        - **🖼️ Use high-quality images** from multiple angles
        - **🎥 Add videos** demonstrating product use
        """)
    else:
        st.info("Generate a description first to see SEO analysis")

# Footer
st.divider()
st.markdown('<div class="footer">🌟 AI Product Description Generator • Powered by GPT-3.5 • 100% Free • Dark Mode</div>', 
           unsafe_allow_html=True)