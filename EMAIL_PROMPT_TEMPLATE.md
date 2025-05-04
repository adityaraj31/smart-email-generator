# Email Generator LangChain Prompt Template

## LangChain Implementation

```python
from langchain.prompts import PromptTemplate

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

# Create LangChain prompt template
prompt = PromptTemplate(
    input_variables=["subject"],
    template=email_template
)
```

## How This Prompt Works

1. **Role Definition**: Establishes the AI as an email marketing expert, guiding it to generate content with professional expertise
   
2. **Task Specification**: Clearly defines that a complete email should be generated based on the provided subject

3. **Component Requirements**: Lists the specific elements that must be included in the generated email
   
4. **Tone Guidance**: Instructs the AI to adapt the writing style based on the subject's context

5. **Structural Template**: Provides a clear format for the email with placeholders for each section

6. **Final Guidelines**: Emphasizes the importance of conciseness, engagement, and action-oriented language

## Benefits of Using LangChain

1. **Modular Design**: The prompt template can be easily modified or extended
   
2. **Multiple Model Support**: Works with various LLM providers (OpenAI, Anthropic, Llama, etc.)
   
3. **Chain Integration**: Can be combined with other LangChain components for more complex workflows
   
4. **Parameter Control**: Easily adjust temperature, max tokens, and other generation parameters
   
5. **Memory Integration**: Can be extended to include conversation history for context-aware emails

## Usage Examples

### Business Meeting Request
**Input Subject**: "Quarterly Strategy Meeting - June 15th"

### Product Launch Announcement
**Input Subject**: "Introducing Our Revolutionary New Product Line"

### Event Invitation
**Input Subject**: "Exclusive Invitation to Our Premium Webinar"

### Follow-up After Sales Call
**Input Subject**: "Thank You for Our Conversation Yesterday"

### Customer Feedback Request
**Input Subject**: "We Value Your Opinion on Your Recent Purchase"

## Extending the Template

The template can be extended with additional parameters:

```python
email_template_extended = """
You are an AI Email Marketing Expert with years of experience crafting engaging, professional emails. Your task is to generate a complete email based on the subject line provided.

SUBJECT: {subject}
TONE: {tone}
EMAIL LENGTH: {length} paragraphs
INCLUDE PS: {include_ps}

...rest of template...
"""

prompt_extended = PromptTemplate(
    input_variables=["subject", "tone", "length", "include_ps"],
    template=email_template_extended
)
```