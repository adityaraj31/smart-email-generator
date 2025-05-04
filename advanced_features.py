"""
Additional advanced features to extend the Smart Email Generator using LangChain.
These features can be implemented by importing and using these components in app.py.
"""

from langchain.chains import SequentialChain
from langchain.chains.base import Chain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from typing import Dict, List, Any
from langchain.chains import LLMChain

# 1. Structured Output Parser for Email Components
def create_output_parser():
    """Creates a structured output parser for email components"""
    response_schemas = [
        ResponseSchema(name="subject_line", 
                      description="The enhanced subject line for the email"),
        ResponseSchema(name="greeting", 
                      description="The greeting with [Name] placeholder"),
        ResponseSchema(name="body_paragraph_1", 
                      description="Introduction paragraph with hook"),
        ResponseSchema(name="body_paragraph_2", 
                      description="Key details and value proposition"),
        ResponseSchema(name="body_paragraph_3", 
                      description="Additional information or urgency element (optional)"),
        ResponseSchema(name="call_to_action", 
                      description="Clear call-to-action with specific instructions"),
        ResponseSchema(name="sign_off", 
                      description="Professional sign-off"),
    ]
    
    return StructuredOutputParser.from_response_schemas(response_schemas)

# 2. Advanced Email Chain with Analysis Step
def create_advanced_email_chain(llm) -> Chain:
    """Creates a two-step chain that first analyzes the subject, then generates the email"""
    
    # Step 1: Analyze the subject
    analysis_template = """
    You're an expert email marketing analyst. First, analyze the following email subject to determine:
    1. The primary purpose (promotional, informational, invitation, etc.)
    2. The appropriate tone (formal, conversational, urgent, etc.)
    3. The target audience characteristics
    4. Key points that should be emphasized

    SUBJECT: {subject}

    Provide your analysis:
    """
    
    analysis_prompt = PromptTemplate(
        input_variables=["subject"],
        template=analysis_template
    )
    
    analysis_chain = LLMChain(
        llm=llm,
        prompt=analysis_prompt,
        output_key="analysis"
    )
    
    # Step 2: Generate the email based on analysis
    email_template = """
    You are an AI Email Marketing Expert with years of experience crafting engaging, professional emails.
    
    SUBJECT: {subject}
    
    Here's an analysis of the subject that you should use to guide your email creation:
    {analysis}
    
    Based on this analysis, create a comprehensive email that includes:
    1. An attention-grabbing subject line that builds on the provided subject
    2. A personalized greeting with [Name] placeholder
    3. A concise but compelling body (2-3 paragraphs)
    4. A clear call-to-action
    5. A professional sign-off
    
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
    
    email_prompt = PromptTemplate(
        input_variables=["subject", "analysis"],
        template=email_template
    )
    
    email_chain = LLMChain(
        llm=llm,
        prompt=email_prompt,
        output_key="email"
    )
    
    # Combine the chains
    sequential_chain = SequentialChain(
        chains=[analysis_chain, email_chain],
        input_variables=["subject"],
        output_variables=["analysis", "email"],
        verbose=True
    )
    
    return sequential_chain

# 3. Email Chain with Memory for Follow-up Emails
def create_email_chain_with_memory(llm) -> Chain:
    """Creates an email chain that maintains conversation history for follow-up emails"""
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key="subject"
    )
    
    follow_up_template = """
    You are an AI Email Marketing Expert with years of experience crafting engaging, professional emails.
    
    CURRENT SUBJECT: {subject}
    
    PREVIOUS EMAIL HISTORY:
    {chat_history}
    
    Based on the current subject and the previous email history, create a follow-up email that:
    1. References the previous communication
    2. Maintains continuity in tone and messaging
    3. Advances the conversation or objective
    4. Includes all standard email components (greeting, body, CTA, sign-off)
    
    The email should follow this structure:
    ---
    Subject: [Follow-up Subject Line]
    
    Dear [Name],
    
    [First paragraph: Reference to previous communication]
    
    [Second paragraph: New information or next steps]
    
    [Third paragraph (optional): Additional details or urgency]
    
    [Clear call-to-action with specific instructions]
    
    [Professional sign-off],
    [Company Name]
    ---
    
    Keep the email concise, engaging, and focused on driving action.
    """
    
    follow_up_prompt = PromptTemplate(
        input_variables=["subject", "chat_history"],
        template=follow_up_template
    )
    
    follow_up_chain = LLMChain(
        llm=llm,
        prompt=follow_up_prompt,
        memory=memory,
        verbose=True
    )
    
    return follow_up_chain

# 4. Email Template Customization Function
def create_custom_email_template(tone: str, length: int, include_ps: bool) -> PromptTemplate:
    """Creates a customized email template based on user parameters"""
    
    # Base template
    template = """
    You are an AI Email Marketing Expert with years of experience crafting engaging, professional emails.
    
    SUBJECT: {subject}
    REQUESTED TONE: {tone}
    EMAIL LENGTH: {length} paragraphs
    
    Please create a {tone} email that includes:
    1. An attention-grabbing subject line that builds on the provided subject
    2. A personalized greeting with [Name] placeholder
    3. A body with exactly {length} paragraphs
    4. A clear call-to-action
    5. A professional sign-off
    """
    
    # Add PS instruction if requested
    if include_ps:
        template += """
    6. A brief PS line that adds value or creates urgency
    """
    
    # Add tone-specific instructions
    if tone == "formal":
        template += """
    Use formal language, avoid contractions, and maintain professional distance.
    Address the recipient with proper titles and use industry-specific terminology where appropriate.
    """
    elif tone == "friendly":
        template += """
    Use a warm, conversational tone with a personal touch.
    Include light humor where appropriate and focus on building relationship.
    """
    elif tone == "urgent":
        template += """
    Create a sense of urgency throughout the email.
    Use time-sensitive language and emphasize limited availability or deadlines.
    """
    
    # Add email structure
    template += """
    The email should follow this structure:
    ---
    Subject: [Enhanced Subject Line]
    
    Dear [Name],
    
    [Email body with exactly {length} paragraphs]
    
    [Clear call-to-action with specific instructions]
    
    [Professional sign-off],
    [Company Name]
    """
    
    # Add PS if requested
    if include_ps:
        template += """
    
    P.S. [Brief value-add or urgency statement]
    """
    
    template += """
    ---
    
    Keep the email concise, engaging, and focused on driving action. Use persuasive language throughout.
    """
    
    return PromptTemplate(
        input_variables=["subject", "tone", "length"],
        template=template
    )

# 5. Multi-Provider Support
def get_llm_by_provider(provider: str, api_key: str):
    """Returns appropriate LLM based on the provider"""
    if provider == "openai":
        from langchain_openai import OpenAI
        return OpenAI(
            temperature=0.7,
            max_tokens=1024,
            model_name="gpt-3.5-turbo-instruct",
            openai_api_key=api_key
        )
    elif provider == "openai-chat":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo",
            openai_api_key=api_key
        )
    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            temperature=0.7,
            max_tokens=1024,
            model="claude-2",
            anthropic_api_key=api_key
        )
    else:
        # Default to OpenAI
        from langchain_openai import OpenAI
        return OpenAI(
            temperature=0.7,
            max_tokens=1024,
            model_name="gpt-3.5-turbo-instruct",
            openai_api_key=api_key
        )

# 6. Function to integrate settings from the UI
def generate_email_with_settings(subject: str, api_key: str, model_type: str = "openai", 
                               tone: str = "Professional", length: int = 3, include_ps: bool = False) -> str:
    """Generates an email with custom settings"""
    
    # Get the appropriate LLM
    llm = get_llm_by_provider(model_type, api_key)
    
    # Create custom template
    prompt_template = create_custom_email_template(
        tone.lower(), 
        length, 
        include_ps
    )
    
    # Create chain
    chain = LLMChain(
        llm=llm,
        prompt=prompt_template
    )
    
    # Generate email
    result = chain.run(subject=subject, tone=tone.lower(), length=length)
    
    return result.strip()

# Import these in the main app to use them
# from advanced_features import generate_email_with_settings, create_advanced_email_chain