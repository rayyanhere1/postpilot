import streamlit as st
import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

load_dotenv()

class LinkedInPostAgent:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    def generate_post(self, topic, tone, post_type, length):
        lengths = {"Short": "50-100 words", "Medium": "100-200 words", "Long": "200-300 words"}
        prompt = f"""Create a viral LinkedIn post about "{topic}" with {tone} tone, {post_type} type, {lengths[length]}. 
        Include 3-5 emojis, 5-7 hashtags, proper formatting, call-to-action, and make it engaging."""
        
        try:
            response = self.model.generate_content(prompt)
            return re.sub(r'\*+([^*]+)\*+', r'\1', response.text)
        except Exception as e:
            return f"Error: {str(e)}"

st.set_page_config(page_title="LinkedIn Post Generator", page_icon="🚀", layout="centered")

st.markdown("""<style>
.main-header {text-align: center; color: #0077B5; font-size: 3rem; font-weight: bold;}
.sub-header {text-align: center; color: #666; font-size: 1.2rem; margin-bottom: 2rem;}
.post-container {background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #0077B5;}
</style>""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🚀 LinkedIn Post Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Turn Ideas into Viral LinkedIn Posts ✍️</p>', unsafe_allow_html=True)

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    st.error("❌ GEMINI_API_KEY not found in .env file!")
    st.stop()

if 'agent' not in st.session_state:
    st.session_state.agent = LinkedInPostAgent(api_key)
    
st.markdown("### 🎯 Post Configuration")

col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("Topic", placeholder="e.g., AI in marketing")
    tone = st.selectbox("Tone", ["Professional", "Witty", "Story-driven"])
with col2:
    post_type = st.selectbox("Type", ["Story", "Tips", "Question", "Achievement"])
    length = st.selectbox("Post Length", ["Short", "Medium", "Long"])

if st.button("🔗 Generate Your LinkedIn Post", type="primary", use_container_width=True, key="generate_post"):
    if not topic.strip():
        st.warning("⚠️ Please enter a topic!")
    else:
        with st.spinner("⚡ Generating your viral LinkedIn post..."):
            try:
                post = st.session_state.agent.generate_post(topic, tone, post_type, length)
                if "Error:" in post:
                    st.error(f"❌ {post}")
                    st.info("💡 **Solutions:**\n- Wait 24 hours for quota reset\n- Create new Google account & API key\n- Upgrade to paid plan")
                else:
                    st.session_state.generated_post = post
                    st.session_state.post_config = {'topic': topic, 'tone': tone, 'type': post_type, 'length': length}
            except Exception as e:
                st.error(f"❌ API Error: {str(e)}")
                st.info("💡 Try refreshing the page or check your API key")
if 'generated_post' in st.session_state:
    st.success("🎉 Your LinkedIn Post is Ready!")
    
    st.markdown('<div class="post-container">', unsafe_allow_html=True)
    st.text_area("Your LinkedIn Post", value=st.session_state.generated_post, height=300, key="post_display")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 Copy to Clipboard", type="secondary", use_container_width=True, key="copy_clipboard"):
            st.code(st.session_state.generated_post, language=None)
    with col2:
        if st.button("🔄 Generate Another Version", type="secondary", use_container_width=True, key="regenerate_post"):
            with st.spinner("⚡ Creating another version..."):
                config = st.session_state.post_config
                new_post = st.session_state.agent.generate_post(config['topic'], config['tone'], config['type'], config['length'])
                st.session_state.generated_post = new_post
                st.rerun()
    
    st.divider()
    st.info("💡 **Tips:** Be specific with topics, use trending keywords, ask questions for engagement, post during peak hours (8-10 AM, 12-2 PM)")