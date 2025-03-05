# AI-Powered Text Generation API

This is a Flask-based API that allows users to generate AI-powered text using Multiple AI providers. It includes user authentication, text generation, and CRUD operations for generated texts.

## Features
- User registration and login with JWT authentication.
- Generate AI-powered text using multiple AI providers.
- Save, retrieve, update, and delete generated texts.
- PostgreSQL database for persistent storage.

## Prerequisites
- Docker and Docker Compose installed.
- OpenAI/Gemini/etc API key.

## Setup and Deployment

1. **Clone the repository:**
   ```bash
   git clone project
   cd gen-text-ai

2. **Create a .env file:**
   ```bash
   cp .env.example .env
   ```

3. **Remember to Set the OpenAI API key in the .env file:**
   ```bash
   OPENAI_API_KEY=sk-xxxx
   GOOGLE_API_KEY=xxxx
   ```

4. **How to run the application:**

  **Option 1:Using Docker Compose**
  Use Docker Compose to build the images and start the services:
   ```bash
   docker-compose up --build

   ```

  **Option 2:without Docker**
   * create a virtual environment
   python3 -m venv venv
   * activate the virtual environment
   source venv/bin/activate

   * install dependencies
   pip install -r requirements.txt

  * run migrations to create the database tables
   flask db migrate
   flask db upgrade

   * run the application
   flask run

   ```

 **Access the application:**
    * The Flask application will be accessible at localhost:5000.

## API Endpoints

### Register User
```bash
POST /api/auth/register
```

**Parameters:**
- `email` (required): The user's email address.
- `password` (required): The user's password.

**Response:**
```json
{
  "message": "User registered successfully"
}
```

### Login User
```bash
POST /api/auth/login
```

**Parameters:**
- `email` (required): The user's email address.
- `password` (required): The user's password.

**Response:**
```json
{
  "access_token": "**********************"
}

```

### Generate AI-Powered Text
```bash
POST /api/text/generate-text
```

**Parameters:**
- `prompt` (required): The prompt for the AI-powered text generation.

**Response:**
```json
{
  "id": 1,
  "prompt": "Tell me a joke",
  "response": "Why did the tomato turn red? Because it saw the salad dressing!",
  "timestamp": "2023-03-01 12:00:00"
}
```

### Retrieve AI-Powered Text
```bash
GET /api/text/generated-text/{text_id}
```

**Parameters:**
- `text_id` (required): The ID of the text to retrieve.

**Response:**
```json
{
  "id": 1,
  "prompt": "Tell me a joke",
  "response": "Why did the tomato turn red? Because it saw the salad dressing!",
  "timestamp": "2023-03-01 12:00:00"
}
```

### Update AI-Powered Text
```bash
PUT /api/text/generated-text/{text_id}
```

**Parameters:**
- `text_id` (required): The ID of the text to update.
- `response` (required): The new response for the text.

**Response:**
```json
{
  "message": "Text updated successfully"
}
```

### Delete AI-Powered Text
```bash
DELETE /api/text/generated-text/{text_id}
```

**Parameters:**
- `text_id` (required): The ID of the text to delete.

**Response:**
```json
{
  "message": "Text deleted successfully"
}
```

## Author
[Tuti](https://github.com/TUTI254)