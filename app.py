import streamlit as st
from utils.paper_analysis import predict_topics_from_papers
from utils.study_planner import stress_test_plan
from utils.clarity_bot import explain_in_levels

# --- Page Config ---
st.set_page_config(
    page_title="Exam Copilot ✨",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Enhanced CSS with Better Layout ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* CSS Custom Properties for Theme Support */
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --bg-tertiary: #ffffff;
        --text-primary: #1a1a1a;
        --text-secondary: #666666;
        --text-tertiary: #999999;
        --border-primary: #e5e5e5;
        --border-secondary: #d0d7de;
        --shadow-light: rgba(0, 0, 0, 0.08);
        --shadow-medium: rgba(0, 0, 0, 0.12);
        --accent-primary: #2563eb;
        --accent-secondary: #1d4ed8;
        --accent-light: #3b82f6;
        --success-bg: #f0f9ff;
        --success-border: #0ea5e9;
        --success-text: #0c4a6e;
        --warning-bg: #fefce8;
        --warning-border: #eab308;
        --warning-text: #713f12;
        --error-bg: #fef2f2;
        --error-border: #ef4444;
        --error-text: #991b1b;
    }
    
    /* Dark Theme */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --text-primary: #f0f6fc;
            --text-secondary: #c9d1d9;
            --text-tertiary: #8b949e;
            --border-primary: #30363d;
            --border-secondary: #21262d;
            --shadow-light: rgba(0, 0, 0, 0.3);
            --shadow-medium: rgba(0, 0, 0, 0.4);
            --accent-primary: #2563eb;
            --accent-secondary: #1d4ed8;
            --accent-light: #3b82f6;
            --success-bg: #0d1421;
            --success-border: #1f6feb;
            --success-text: #58a6ff;
            --warning-bg: #1c1810;
            --warning-border: #d29922;
            --warning-text: #f2cc60;
            --error-bg: #1c1416;
            --error-border: #f85149;
            --error-text: #ff7b72;
        }
    }
    
    /* Force dark theme class for manual toggle */
    .dark-theme {
        --bg-primary: #0d1117;
        --bg-secondary: #161b22;
        --bg-tertiary: #21262d;
        --text-primary: #f0f6fc;
        --text-secondary: #c9d1d9;
        --text-tertiary: #8b949e;
        --border-primary: #30363d;
        --border-secondary: #21262d;
        --shadow-light: rgba(0, 0, 0, 0.3);
        --shadow-medium: rgba(0, 0, 0, 0.4);
        --accent-primary: #2563eb;
        --accent-secondary: #1d4ed8;
        --accent-light: #3b82f6;
        --success-bg: #0d1421;
        --success-border: #1f6feb;
        --success-text: #58a6ff;
        --warning-bg: #1c1810;
        --warning-border: #d29922;
        --warning-text: #f2cc60;
        --error-bg: #1c1416;
        --error-border: #f85149;
        --error-text: #ff7b72;
    }
    
    /* Reset and base styles */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    .main {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Custom font */
    html, body, [class*="css"], * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    /* Hero Section - Improved */
    .hero-section {
        background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
        border: 1px solid var(--border-primary);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        margin: 0 0 2rem 0;
        box-shadow: 0 4px 20px var(--shadow-light);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--accent-light), transparent);
        opacity: 0.5;
    }
    
    .hero-title {
        font-size: 3rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        margin-bottom: 1rem !important;
        letter-spacing: -0.025em;
        background: linear-gradient(135deg, var(--text-primary), var(--accent-primary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 1.125rem !important;
        color: var(--text-secondary) !important;
        font-weight: 400 !important;
        margin-bottom: 2rem !important;
        line-height: 1.6;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 1rem;
        margin-top: 2rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .stat-card {
        background: var(--bg-primary);
        border: 1px solid var(--border-primary);
        border-radius: 12px;
        padding: 1.5rem 1rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(37, 99, 235, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px var(--shadow-medium);
        border-color: var(--accent-light);
    }
    
    .stat-card:hover::before {
        left: 100%;
    }
    
    .stat-number {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--accent-primary);
        display: block;
    }
    
    .stat-label {
        color: var(--text-secondary);
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Enhanced Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-primary) !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
        margin: 1.5rem 0 2rem 0 !important;
        gap: 0.25rem !important;
        box-shadow: 0 2px 10px var(--shadow-light) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 8px !important;
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        padding: 0.875rem 1.5rem !important;
        transition: all 0.2s ease !important;
        border: none !important;
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--accent-primary) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3) !important;
        transform: scale(1.02);
    }
    
    .stTabs [data-baseweb="tab-border"],
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    
    /* Enhanced Feature Cards */
    .feature-card {
        background: var(--bg-tertiary);
        border: 1px solid var(--border-primary);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 12px var(--shadow-light);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-primary), var(--accent-light));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px var(--shadow-medium);
        border-color: var(--accent-light);
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    .feature-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border-primary);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-right: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-light));
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-primary) !important;
        margin: 0;
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-light)) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        padding: 0.875rem 2rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        height: 52px !important;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--accent-secondary), var(--accent-primary)) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* Enhanced File Uploader */
    .stFileUploader > div {
        background: var(--bg-secondary) !important;
        border: 2px dashed var(--border-secondary) !important;
        border-radius: 12px !important;
        padding: 3rem 2rem !important;
        transition: all 0.3s ease !important;
        text-align: center !important;
        position: relative;
        overflow: hidden;
    }
    
    .stFileUploader > div::before {
        content: '📄';
        font-size: 3rem;
        display: block;
        margin-bottom: 1rem;
        opacity: 0.7;
    }
    
    .stFileUploader > div:hover {
        border-color: var(--accent-primary) !important;
        background: var(--bg-tertiary) !important;
        border-style: solid !important;
    }
    
    .stFileUploader label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* Enhanced Inputs */
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextInput > div > div > input {
        background: var(--bg-tertiary) !important;
        border: 2px solid var(--border-secondary) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        padding: 0.875rem !important;
        font-size: 0.95rem !important;
        font-weight: 400 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus,
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
        outline: none !important;
        transform: scale(1.02) !important;
    }
    
    .stTextArea > div > div > textarea::placeholder,
    .stTextInput > div > div > input::placeholder {
        color: var(--text-tertiary) !important;
        font-style: italic;
    }
    
    /* Enhanced Labels */
    .stTextArea label,
    .stNumberInput label,
    .stFileUploader label,
    .stSelectbox label,
    .stTextInput label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.75rem !important;
        display: block !important;
    }
    
    /* Enhanced Message Boxes */
    .success-box {
        background: var(--success-bg) !important;
        border: 1px solid var(--success-border) !important;
        border-left: 4px solid var(--success-border) !important;
        border-radius: 10px !important;
        padding: 1rem 1.5rem !important;
        color: var(--success-text) !important;
        font-weight: 500 !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 2px 8px rgba(14, 165, 233, 0.1) !important;
    }
    
    .warning-box {
        background: var(--warning-bg) !important;
        border: 1px solid var(--warning-border) !important;
        border-left: 4px solid var(--warning-border) !important;
        border-radius: 10px !important;
        padding: 1rem 1.5rem !important;
        color: var(--warning-text) !important;
        font-weight: 500 !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 2px 8px rgba(234, 179, 8, 0.1) !important;
    }
    
    .error-box {
        background: var(--error-bg) !important;
        border: 1px solid var(--error-border) !important;
        border-left: 4px solid var(--error-border) !important;
        border-radius: 10px !important;
        padding: 1rem 1.5rem !important;
        color: var(--error-text) !important;
        font-weight: 500 !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.1) !important;
    }
    
    /* Enhanced Result Container */
    .result-box {
        background: var(--bg-secondary);
        border: 1px solid var(--border-primary);
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        border-left: 4px solid var(--accent-primary);
        box-shadow: 0 4px 20px var(--shadow-light);
        position: relative;
    }
    
    .result-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, var(--accent-primary), transparent);
        opacity: 0.5;
    }
    
    /* Typography improvements */
    p, .stMarkdown p {
        color: var(--text-secondary) !important;
        font-size: 0.95rem !important;
        line-height: 1.7 !important;
        font-weight: 400 !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        line-height: 1.4 !important;
    }
    
    .stMarkdown h3 {
        font-size: 1.25rem !important;
        margin-bottom: 1rem !important;
        margin-top: 1.5rem !important;
    }
    
    /* Enhanced Footer */
    .footer {
        text-align: center;
        padding: 3rem 2rem;
        color: var(--text-tertiary) !important;
        font-size: 0.875rem;
        margin-top: 4rem;
        border-top: 1px solid var(--border-primary);
        background: var(--bg-secondary);
        border-radius: 16px 16px 0 0;
    }
    
    /* Spinner styling */
    .stSpinner {
        color: var(--accent-primary) !important;
    }
    
    /* Enhanced Grid layouts */
    .input-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .two-column-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    /* Enhanced Theme Toggle */
    .theme-toggle {
        position: fixed;
        top: 1.5rem;
        right: 1.5rem;
        background: var(--bg-tertiary);
        border: 1px solid var(--border-primary);
        border-radius: 50%;
        width: 56px;
        height: 56px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 1.5rem;
        transition: all 0.3s ease;
        z-index: 1000;
        box-shadow: 0 4px 20px var(--shadow-medium);
    }
    
    .theme-toggle:hover {
        transform: rotate(180deg) scale(1.1);
        box-shadow: 0 8px 30px var(--shadow-medium);
        background: var(--accent-primary);
        color: white;
    }
    
    /* Loading states */
    .loading-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        flex-direction: column;
        gap: 1rem;
    }
    
    .loading-text {
        color: var(--text-secondary) !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        .two-column-grid {
            grid-template-columns: 1fr;
        }
        
        .hero-title {
            font-size: 2rem !important;
        }
        
        .hero-subtitle {
            font-size: 1rem !important;
        }
        
        .stats-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 0.75rem;
        }
        
        .feature-card {
            padding: 1.5rem;
        }
        
        .theme-toggle {
            width: 48px;
            height: 48px;
            font-size: 1.2rem;
            top: 1rem;
            right: 1rem;
        }
        
        .feature-header {
            flex-direction: column;
            text-align: center;
            gap: 1rem;
        }
        
        .feature-icon {
            margin-right: 0;
        }
    }
    
    /* Selectbox improvements */
    .stSelectbox [data-baseweb="select"] {
        background: var(--bg-tertiary) !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background: var(--bg-tertiary) !important;
        border: 2px solid var(--border-secondary) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-up {
        animation: slideUp 0.3s ease-out;
    }
    
    @keyframes slideUp {
        from { transform: translateY(10px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
</style>

<script>
function toggleTheme() {
    const root = document.documentElement;
    const isDark = root.classList.contains('dark-theme');
    
    if (isDark) {
        root.classList.remove('dark-theme');
        localStorage.setItem('theme', 'light');
    } else {
        root.classList.add('dark-theme');
        localStorage.setItem('theme', 'dark');
    }
}

// Load saved theme or detect system preference
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
        document.documentElement.classList.add('dark-theme');
    }
    
    // Add fade-in animation to main content
    setTimeout(() => {
        document.querySelector('.main').classList.add('fade-in');
    }, 100);
});

// Add smooth scroll behavior
document.addEventListener('DOMContentLoaded', function() {
    const style = document.createElement('style');
    style.textContent = `
        html {
            scroll-behavior: smooth;
        }
    `;
    document.head.appendChild(style);
});
</script>
""", unsafe_allow_html=True)

# --- Theme Toggle Button ---
st.markdown("""
<div class="theme-toggle" onclick="toggleTheme()" title="Toggle theme">
    🌓
</div>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div class="hero-section fade-in">
    <h1 class="hero-title">🧠 Exam Copilot</h1>
    <p class="hero-subtitle">Your AI-powered study partner for smarter, more effective exam preparation</p>
    <div class="stats-grid">
        <div class="stat-card">
            <span class="stat-number">AI</span>
            <div class="stat-label">Powered</div>
        </div>
        <div class="stat-card">
            <span class="stat-number">24/7</span>
            <div class="stat-label">Available</div>
        </div>
        <div class="stat-card">
            <span class="stat-number">Smart</span>
            <div class="stat-label">Analysis</div>
        </div>
        <div class="stat-card">
            <span class="stat-number">Fast</span>
            <div class="stat-label">Results</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Enhanced Tabs ---
tab1, tab2, tab3 = st.tabs([
    "🔮 Past Paper Predictor", 
    "📊 Study Plan Optimizer", 
    "💡 Clarity Assistant"
])

# --- Past Paper Predictor ---
with tab1:
    st.markdown('<div class="feature-card slide-up">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-header">
        <div class="feature-icon">🔮</div>
        <div>
            <h2 class="feature-title">Past Paper Predictor</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Upload your past exam papers and let our advanced AI analyze patterns, question frequencies, and topic distributions 
    to predict the most likely topics for your upcoming exam with high accuracy.
    """)
    
    # File upload section
    st.markdown("### 📄 Upload Your Past Papers")
    uploaded_files = st.file_uploader(
        "Choose PDF files", 
        type="pdf", 
        accept_multiple_files=True,
        help="Upload multiple past exam papers for better prediction accuracy. Supports PDF format only.",
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        st.markdown(f'<div class="success-box">✅ {len(uploaded_files)} file(s) uploaded successfully!</div>', unsafe_allow_html=True)
        
        # Show uploaded files
        with st.expander("📋 View uploaded files"):
            for file in uploaded_files:
                st.write(f"• {file.name} ({file.size} bytes)")

    # Analysis button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_btn = st.button("🚀 Analyze Papers & Predict Topics", key="analyze_btn", use_container_width=True)

    if analyze_btn:
        if uploaded_files:
            with st.spinner("🔍 Analyzing your papers and identifying patterns..."):
                try:
                    result = predict_topics_from_papers(uploaded_files)
                    st.markdown('<div class="success-box">✅ Analysis complete! Here are your predicted topics:</div>', unsafe_allow_html=True)
                    st.markdown('<div class="result-box slide-up">', unsafe_allow_html=True)
                    st.markdown("### 📈 Predicted High-Probability Topics")
                    st.markdown(result)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="error-box">❌ Error analyzing papers: {str(e)}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box">⚠️ Please upload some past exam papers first to start the analysis.</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Study Plan Stress Test ---
with tab2:
    st.markdown('<div class="feature-card slide-up">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-header">
        <div class="feature-icon">📊</div>
        <div>
            <h2 class="feature-title">Study Plan Optimizer</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Create an intelligent, optimized study schedule that adapts to your available time, learning pace, 
    and exam priorities. Our AI considers cognitive load distribution and retention patterns.
    """)
    
    # Study topics input
    st.markdown("### 📝 Study Configuration")
    topics = st.text_area(
        "Topics to Study", 
        placeholder="Enter topics separated by commas (e.g., Calculus, Linear Algebra, Statistics, Probability)",
        height=100,
        help="List all the topics you need to cover for your exam. Be specific for better planning."
    )
    
    # Time configuration
    st.markdown("### ⏰ Time Management")
    st.markdown('<div class="two-column-grid">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        hours_per_day = st.number_input(
            "Study Hours Per Day", 
            min_value=1, 
            max_value=16, 
            value=6,
            help="Realistic daily study hours (including breaks)"
        )
        
        study_intensity = st.selectbox(
            "Study Intensity",
            ["Light", "Moderate", "Intensive", "Exam Mode"],
            index=1,
            help="Choose your preferred study intensity level"
        )
    
    with col2:
        days_until_exam = st.number_input(
            "Days Until Exam", 
            min_value=1, 
            max_value=90, 
            value=14,
            help="Number of days remaining until your exam"
        )
        
        break_frequency = st.selectbox(
            "Break Frequency",
            ["Every 25 mins (Pomodoro)", "Every 45 mins", "Every hour", "Every 90 mins"],
            index=0,
            help="How often you want to take breaks during study sessions"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional preferences
    with st.expander("🎯 Advanced Preferences (Optional)"):
        col1, col2 = st.columns(2)
        with col1:
            priority_topics = st.text_input(
                "High Priority Topics",
                placeholder="Topics that need extra focus (comma separated)",
                help="Topics you find challenging or that carry more weight"
            )
        with col2:
            learning_style = st.selectbox(
                "Learning Style",
                ["Visual", "Auditory", "Reading/Writing", "Kinesthetic", "Mixed"],
                index=4,
                help="Your preferred learning approach"
            )

    # Generate plan button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        plan_btn = st.button("🎯 Generate Optimal Study Plan", key="plan_btn", use_container_width=True)

    if plan_btn:
        if not topics.strip():
            st.markdown('<div class="warning-box">⚠️ Please enter some topics to study first.</div>', unsafe_allow_html=True)
        else:
            with st.spinner("🧠 Creating your personalized study plan..."):
                try:
                    # Create enhanced context for the planner
                    context = {
                        'intensity': study_intensity,
                        'break_frequency': break_frequency,
                        'priority_topics': priority_topics,
                        'learning_style': learning_style
                    }
                    
                    plan = stress_test_plan(topics, hours_per_day, days_until_exam, context)
                    st.markdown('<div class="success-box">✅ Your optimized study plan is ready! 📚</div>', unsafe_allow_html=True)
                    st.markdown('<div class="result-box slide-up">', unsafe_allow_html=True)
                    st.markdown("### 📋 Your Personalized Study Schedule")
                    st.markdown(plan)
                    
                    # Add download option
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.download_button(
                            "📥 Download Study Plan",
                            data=plan,
                            file_name="my_study_plan.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="error-box">❌ Error generating study plan: {str(e)}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Clarity Assistant ---
with tab3:
    st.markdown('<div class="feature-card slide-up">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-header">
        <div class="feature-icon">💡</div>
        <div>
            <h2 class="feature-title">Clarity Assistant</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Get complex concepts explained at different levels of understanding, from beginner to expert. 
    Our AI adapts explanations with examples, analogies, and visual descriptions tailored to your learning level.
    """)
    
    # Concept input
    st.markdown("### 🤔 What Would You Like to Understand?")
    concept = st.text_area(
        "Concept or Topic", 
        placeholder="Enter any topic, concept, or question you're struggling with...\n\nExample: 'Explain quantum entanglement' or 'How does machine learning work?'",
        height=120,
        help="Describe the concept you want to understand better. Be as specific as possible."
    )
    
    # Configuration options
    st.markdown("### ⚙️ Explanation Settings")
    st.markdown('<div class="two-column-grid">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        level = st.selectbox(
            "Explanation Level",
            ["Beginner (ELI5)", "Intermediate", "Advanced", "Expert"],
            index=1,
            help="Choose the complexity level for the explanation"
        )
        
        explanation_style = st.selectbox(
            "Explanation Style",
            ["Conversational", "Academic", "Step-by-step", "Analogies & Examples"],
            index=0,
            help="How you prefer to receive explanations"
        )
    
    with col2:
        context = st.text_input(
            "Subject Context",
            placeholder="e.g., Mathematics, Physics, Biology, Computer Science",
            help="Provide subject context for more accurate explanations"
        )
        
        include_examples = st.checkbox(
            "Include Practical Examples",
            value=True,
            help="Add real-world examples and applications"
        )

    # Advanced options
    with st.expander("🔧 Advanced Options"):
        col1, col2 = st.columns(2)
        with col1:
            include_visuals = st.checkbox(
                "Include Visual Descriptions",
                value=True,
                help="Add descriptions of diagrams, charts, or visual aids"
            )
            
            follow_up_questions = st.checkbox(
                "Suggest Follow-up Questions",
                value=True,
                help="Get related questions to deepen your understanding"
            )
        
        with col2:
            explanation_length = st.selectbox(
                "Explanation Length",
                ["Concise", "Detailed", "Comprehensive"],
                index=1,
                help="How detailed you want the explanation to be"
            )
            
            prerequisites = st.text_input(
                "Prerequisites (Optional)",
                placeholder="What background knowledge do you have?",
                help="Any relevant background knowledge or prerequisites"
            )

    # Generate explanation button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        explain_btn = st.button("💡 Get Clear Explanation", key="explain_btn", use_container_width=True)

    if explain_btn:
        if not concept.strip():
            st.markdown('<div class="warning-box">⚠️ Please enter a concept to explain first.</div>', unsafe_allow_html=True)
        else:
            with st.spinner("🧠 Generating your personalized explanation..."):
                try:
                    # Create enhanced context for the clarity bot
                    enhanced_context = {
                        'context': context,
                        'style': explanation_style,
                        'include_examples': include_examples,
                        'include_visuals': include_visuals,
                        'follow_up_questions': follow_up_questions,
                        'length': explanation_length,
                        'prerequisites': prerequisites
                    }
                    
                    explanation = explain_in_levels(concept, level, enhanced_context)
                    st.markdown('<div class="success-box">✅ Here\'s your personalized explanation! 🎯</div>', unsafe_allow_html=True)
                    st.markdown('<div class="result-box slide-up">', unsafe_allow_html=True)
                    st.markdown(f"### 🎯 {level} Level Explanation")
                    if context:
                        st.markdown(f"**Subject:** {context}")
                    st.markdown("---")
                    st.markdown(explanation)
                    
                    # Add rating and feedback
                    st.markdown("---")
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col1:
                        if st.button("👍 Helpful"):
                            st.success("Thanks for your feedback!")
                    with col3:
                        if st.button("👎 Needs improvement"):
                            st.info("We'll work on improving our explanations!")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="error-box">❌ Error generating explanation: {str(e)}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Additional Features Section ---
st.markdown("---")
st.markdown("## 🚀 More Features Coming Soon")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: var(--bg-secondary); border-radius: 12px; margin: 0.5rem 0;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
        <h4 style="color: var(--text-primary); margin: 0.5rem 0;">Progress Tracking</h4>
        <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">Track your study progress and performance analytics</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: var(--bg-secondary); border-radius: 12px; margin: 0.5rem 0;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
        <h4 style="color: var(--text-primary); margin: 0.5rem 0;">Smart Quizzes</h4>
        <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">AI-generated practice questions based on your topics</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: var(--bg-secondary); border-radius: 12px; margin: 0.5rem 0;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">👥</div>
        <h4 style="color: var(--text-primary); margin: 0.5rem 0;">Study Groups</h4>
        <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">Collaborate with peers and share study materials</p>
    </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div class="footer">
    <div style="margin-bottom: 1rem;">
        <strong>🧠 Exam Copilot</strong> - Your AI Study Partner
    </div>
    <div style="font-size: 0.8rem; opacity: 0.8;">
        Made with ❤️ for better learning • Powered by Advanced AI<br>
        © 2024 Exam Copilot. Helping students achieve their academic goals.
    </div>
</div>
""", unsafe_allow_html=True)