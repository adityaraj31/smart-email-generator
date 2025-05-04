import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Smart Email Generator",
    page_icon="📧",
    layout="wide"
)

# Application title and description
st.title("Smart Email Generator")
st.markdown("""
This application generates professional emails based on your provided subject.
Simply enter a subject, and the AI will craft a complete email for you.
""")

# Check for API keys in environment variables
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.warning("""
    No API key found. Please set your Groq API key in the .env file or in the field below.
    """)
    api_key = st.text_input("Enter your Groq API key:", type="password")
    if not api_key:
        st.stop()

# Initialize LangChain LLM (cached for efficiency)
@st.cache_resource
def load_llm(_api_key):
    return ChatGroq(
        temperature=0.7,
        max_tokens=1024,
        model_name="llama3-8b-8192",  # or any other Groq model you prefer
        groq_api_key=_api_key
    )

# Email generation prompt template using LangChain
email_template = """
You are an AI Email Marketing Expert with years of experience crafting engaging, professional emails. Your task is to generate a complete email based on the subject line provided.

SUBJECT: {subject}

Please create a comprehensive email that includes:
1. An attention-grabbing subject line that builds on the provided subject
2. A personalized greeting with [Name] placeholder
3. A concise but compelling body (2-3 paragraphs)
4. A clear call-to-action
5. A professional sign-off

Adjust the tone and style to match the context of the subject (formal, urgent, friendly, promotional, etc.).

The email should follow this structure:
---
Subject: [Enhanced Subject Line]

Dear [Name],

[First paragraph: Introduction and hook related to the subject]

[Second paragraph: Key details and value proposition]

[Third paragraph (optional): Additional information or urgency element]

[Clear call-to-action with specific instructions]

[Professional sign-off],
[Company Name]
---

Keep the email concise, engaging, and focused on driving action. Use persuasive language throughout.
"""

# Function to generate email using LangChain
def generate_email(subject, api_key, model_type="openai"):
    if model_type == "openai":
        llm = load_llm(api_key)
    else:
        # Support for additional models can be added here
        llm = load_llm(api_key)
    
    # Create LangChain prompt template
    prompt = PromptTemplate(
        input_variables=["subject"],
        template=email_template
    )
    
    # Create LangChain
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Generate email
    result = chain.run(subject=subject)
    
    return result.strip()

# Sidebar for customization options
with st.sidebar:
    st.header("About")
    st.markdown("""
    This application uses LangChain with cloud-based LLMs to generate professional emails based on your provided subject line.
    
    **How it works:**
    1. Enter your email subject
    2. Click "Generate Email"
    3. Copy the generated email and customize as needed
    
    The AI acts as an email marketing expert to create engaging, effective emails.
    """)
    
    # Model selection
    st.header("Options")
    model_choice = st.selectbox(
        "Select LLM Provider",
        ["llama3-8b-8192", "llama2-70b-4096"],  # Updated to have different options
        index=0
    )
    
    # Map selection to model parameters
    model_mapping = {
        "llama3-8b-8192": {"type": "groq", "model": "llama3-8b-8192"},
        "llama2-70b-4096": {"type": "groq", "model": "llama2-70b-4096"}
    }
    selected_model = model_mapping[model_choice]
    
    # Additional customization options
    with st.expander("Advanced Settings"):
        email_tone = st.selectbox("Tone", ["Professional", "Friendly", "Urgent", "Formal"], index=0)
        email_length = st.slider("Email Length", min_value=1, max_value=5, value=3, 
                              help="Controls the approximate length of the email in paragraphs")
        add_ps = st.checkbox("Add PS line", value=False)

# Main app interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Email Input")
    subject = st.text_input("Enter your email subject:", placeholder="e.g., Exclusive Invitation to Our Premium Webinar")
    
    # Sample subjects for inspiration
    if st.checkbox("Show sample subjects"):
        st.caption("Sample subjects (click to use):")
        sample_subjects = [
            "Quarterly Strategy Meeting - June 15th",
            "Introducing Our Revolutionary New Product Line",
            "Exclusive Invitation to Our Premium Webinar",
            "Thank You for Our Conversation Yesterday",
            "We Value Your Opinion on Your Recent Purchase"
        ]
        
        for sample in sample_subjects:
            if st.button(sample, key=sample):
                st.session_state['subject'] = sample
                subject = sample
    
    if st.button("Generate Email", type="primary"):
        if subject:
            with st.spinner("Generating your email..."):
                try:
                    email_content = generate_email(
                        subject, 
                        api_key, 
                        model_type=selected_model["type"]
                    )
                    st.session_state['generated_email'] = email_content
                    st.session_state['subject'] = subject
                except Exception as e:
                    st.error(f"Error generating email: {str(e)}")
        else:
            st.warning("Please enter a subject for your email.")

with col2:
    st.subheader("Generated Email")
    if 'generated_email' in st.session_state:
        email_content = st.session_state['generated_email']
        st.text_area("Email Content", email_content, height=400)
        
        # Action buttons
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.download_button(
                label="Download Email",
                data=email_content,
                file_name="generated_email.txt",
                mime="text/plain"
            )
        with col_b:
            if st.button("Copy to Clipboard", help="Copy the email content to your clipboard"):
                js_code = f"""
                <script>
                    try {{
                        const text = {repr(email_content)};
                        navigator.clipboard.writeText(text)
                            .then(() => {{
                                window.streamlitMessageListener.handleMessage({{
                                    type: 'streamlit:message',
                                    data: {{ type: 'success', message: 'Email copied to clipboard!' }}
                                }});
                            }})
                            .catch(err => {{
                                console.error('Failed to copy: ', err);
                                window.streamlitMessageListener.handleMessage({{
                                    type: 'streamlit:message',
                                    data: {{ type: 'error', message: 'Failed to copy to clipboard. Please try selecting and copying manually.' }}
                                }});
                            }});
                    }} catch (err) {{
                        console.error('Error: ', err);
                    }}
                </script>
                """
                st.components.v1.html(js_code, height=0)
        with col_c:
            if st.button("Regenerate"):
                if 'subject' in st.session_state:
                    with st.spinner("Regenerating email..."):
                        try:
                            email_content = generate_email(
                                st.session_state['subject'], 
                                api_key,
                                model_type=selected_model["type"]
                            )
                            st.session_state['generated_email'] = email_content
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error regenerating email: {str(e)}")
    else:
        st.info("Your generated email will appear here.")
        
        # Show example email
        with st.expander("See example email"):
            st.markdown("""
            **Subject:** Your Exclusive VIP Access: Premium Industry Insights Webinar
            
            Dear [Name],
            
            I'm reaching out with a special invitation reserved for our most valued clients. We're hosting an exclusive Premium Webinar featuring industry leaders who will be sharing cutting-edge strategies and insider knowledge that won't be available anywhere else.
            
            During this 60-minute session, you'll discover actionable techniques to improve your business outcomes, learn about emerging trends before your competitors, and have the opportunity to participate in a live Q&A with our expert panel. This invitation-only event is designed specifically for professionals at your level of expertise.
            
            Secure your spot now by clicking the button below. With limited virtual seats available, we recommend registering today to avoid disappointment.
            
            **REGISTER NOW: SECURE MY SPOT**
            
            Looking forward to seeing you there,  
            [Company Name]
            """)

# Footer
st.markdown("---")
# Add session management and user preferences
st.sidebar.markdown("---")
if "user_preferences" not in st.session_state:
    st.session_state["user_preferences"] = {
        "company_name": "",
        "default_signature": "",
        "brand_colors": {},
        "templates": []
    }

with st.sidebar.expander("Enterprise Settings"):
    st.session_state["user_preferences"]["company_name"] = st.text_input(
        "Company Name",
        value=st.session_state["user_preferences"]["company_name"]
    )
    st.session_state["user_preferences"]["default_signature"] = st.text_area(
        "Default Signature",
        value=st.session_state["user_preferences"]["default_signature"]
    )