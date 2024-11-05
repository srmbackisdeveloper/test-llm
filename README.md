## Simple Run (Dockerfile is for future use)

```bash
uvicorn app.base:app --reload
```

## Environment Variables

- **`OPENAI_API_KEY`** - Your OpenAI API Key
- **`ASSISTANT_ID`** - Your Assistant ID
- **`DSN`** - DSN for PostgreSQL database

`.env` file:

```plaintext
OPENAI_API_KEY=your_openai_api_key
ASSISTANT_ID=your_assistant_id
DSN=postgresql://username:password@hostname:port/database
```

## Documentation

`GET /docs`
`GET /redoc`

## Other ref:

https://platform.openai.com/docs/api-reference/assistants/createAssistant
https://medium.com/@amirm.lavasani/how-to-structure-your-fastapi-projects-0219a6600a8f
