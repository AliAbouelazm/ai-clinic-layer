# OpenAI API Setup (Optional)

## Is OpenAI API Free?

**No, but they offer free credits:**
- New accounts get **$5 in free credits** (expires after 3 months)
- After that, you pay per use:
  - GPT-4o-mini: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
  - For this app, each symptom parse costs ~$0.0001-0.0005 (very cheap)

## Setup Instructions

1. **Get an API key:**
   - Go to https://platform.openai.com/api-keys
   - Sign up/login
   - Create a new API key

2. **Add to Streamlit Cloud:**
   - Go to your Streamlit app settings
   - Click "Secrets" (or "Environment variables")
   - Add:
     ```
     LLM_PROVIDER=openai
     OPENAI_API_KEY=sk-your-key-here
     ```

3. **Or use locally:**
   - Create a `.env` file in the project root:
     ```
     LLM_PROVIDER=openai
     OPENAI_API_KEY=sk-your-key-here
     ```

## Current Default

The system **defaults to "mock" parser** which works well and is free. The mock parser:
- ✅ Detects injuries, bleeding, chest pain, etc.
- ✅ Calculates severity on a spectrum
- ✅ Provides consistent results
- ✅ No API costs

You only need OpenAI API if you want:
- More nuanced symptom parsing
- Better handling of complex descriptions
- More natural language understanding

## Testing

The mock parser should give **~52% risk** for "significant bleeding from a cut that won't stop".

If you're getting different results, check:
1. Is `LLM_PROVIDER` set to "mock" in your environment?
2. Has Streamlit Cloud reloaded the latest code?
3. Check the version number - should show "Version 4.1"

