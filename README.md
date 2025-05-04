# Smart Email Generator

This application generates professional emails based on user-provided subject lines using LangChain and cloud-based language models.

## Features

- **Subject-Based Email Generation**: Enter a subject and receive a complete, professional email
- **Cloud-Based LLM Integration**: Uses OpenAI's GPT models (with options for other providers)
- **Role-Based Generation**: AI assumes the role of an email marketing expert
- **Structured Output**: Generated emails include subject line, greeting, body, call-to-action, and sign-off
- **Contextual Tone Adjustment**: Adapts email tone based on subject context
- **Simple Interface**: Easy-to-use Streamlit web application

## Tech Stack

- **Python**: Core programming language
- **LangChain**: Framework for LLM application development
- **OpenAI GPT**: Cloud-based language models
- **Streamlit**: Web interface for user interaction

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/smart-email-generator.git
   cd smart-email-generator
   ```

2. Install requirements:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

3. If you haven't set the API key in the `.env` file, you'll be prompted to enter it in the application

4. Enter your email subject and click "Generate Email"

5. Copy, download, or customize the generated email as needed

## LangChain Prompt Structure

The system uses a LangChain PromptTemplate that:

1. Defines the AI's role as an email marketing expert
2. Specifies the email components (subject, greeting, body, CTA, sign-off)
3. Provides structural guidance for the email format
4. Instructs on tone adaptation based on subject context
5. Emphasizes persuasive, action-oriented language

## Example

**Input Subject:** "Exclusive Invitation to Our Premium Webinar"

**Generated Email:**
```
Subject: Your Exclusive VIP Access: Premium Industry Insights Webinar

Dear [Name],

I'm reaching out with a special invitation reserved for our most valued clients. We're hosting an exclusive Premium Webinar featuring industry leaders who will be sharing cutting-edge strategies and insider knowledge that won't be available anywhere else.

During this 60-minute session, you'll discover actionable techniques to improve your business outcomes, learn about emerging trends before your competitors, and have the opportunity to participate in a live Q&A with our expert panel. This invitation-only event is designed specifically for professionals at your level of expertise.

Secure your spot now by clicking the button below. With limited virtual seats available, we recommend registering today to avoid disappointment.

REGISTER NOW: SECURE MY SPOT

Looking forward to seeing you there,
[Company Name]
```

## Advanced Features

The application includes several advanced features in the `advanced_features.py` file:

1. **Structured Output Parsing**: For more organized email components
2. **Sequential Email Chain**: Analyzes the subject before generating content
3. **Memory Integration**: For follow-up emails referencing previous communications
4. **Custom Email Templates**: Based on tone, length, and other parameters
5. **Multi-Provider Support**: Integration with various LLM providers
6. **UI-Driven Customization**: Options for tone, length, and additional elements

## Customization Options

The application includes UI elements for customization:
- Model selection (OpenAI GPT-3.5 or GPT-4)
- Email tone selection (Professional, Friendly, Urgent, Formal)
- Email length control
- Option to add a PS line

## Environment Variables

The application uses the following environment variables:
- `GROQ_API_KEY`: Your Groq API key
- `OPENAI_API_KEY`: Your OpenAI API key

## License

MIT License