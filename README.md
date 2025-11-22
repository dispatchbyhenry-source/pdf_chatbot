# PDF Reader & Chatbot

A modern, AI-powered PDF reader and chatbot application built with Flask and LangChain. Upload PDF documents and chat with them using OpenAI's GPT models and embeddings.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3-orange.svg)

## Features

- 📄 **PDF Upload**: Upload and process PDF documents with automatic text extraction
- 🤖 **AI Chat Interface**: ChatGPT-like interface for interacting with your PDFs
- 🔍 **Semantic Search**: Advanced semantic search using FAISS vector database
- 💬 **Real-time Chat**: Smooth, responsive chat interface with typing indicators
- 🎨 **Modern UI**: Beautiful, eye-catching design with gradient themes
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices

## Screenshots

### Upload Screen
- Modern gradient design
- Drag-and-drop file upload
- View all uploaded PDFs in a grid layout

### Chat Screen
- ChatGPT-inspired dark theme interface
- Real-time message streaming
- Smooth animations and transitions

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dispatchbyhenry-source/pdf_chatbot.git
   cd pdf_chatbot
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

1. **Start the Flask application**
   ```bash
   python pdfreader.py
   ```

2. **Open your browser**
   
   Navigate to `http://localhost:5000` or `http://127.0.0.1:5000`

3. **Upload a PDF**
   - Click on the upload area or drag and drop a PDF file
   - Wait for the file to be processed (embeddings will be created automatically)
   - The file will appear in the uploaded files section

4. **Chat with your PDF**
   - Navigate to the Chat page
   - Select the PDF you want to chat with
   - Start asking questions about the document content

## Project Structure

```
pdf_chatbot/
│
├── pdfreader.py          # Main Flask application
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
├── README.md            # Project documentation
│
├── templates/
│   ├── index.html       # Upload page template
│   └── chat.html        # Chat interface template
│
├── uploads/             # Uploaded PDF files (created automatically)
├── embeddings/          # FAISS vector stores (created automatically)
│
└── .env                 # Environment variables (create this file)
```

## Technologies Used

- **Backend**:
  - Flask - Web framework
  - LangChain 0.3 - LLM framework
  - LangChain OpenAI - OpenAI integrations
  - FAISS - Vector similarity search
  - PyPDFium2 - PDF processing

- **Frontend**:
  - HTML5
  - CSS3 (Modern gradients and animations)
  - Vanilla JavaScript (No framework dependencies)

- **AI/ML**:
  - OpenAI GPT-4o-mini - Chat model
  - OpenAI text-embedding-3-large - Embeddings model

## API Endpoints

### `GET /`
Renders the upload page with list of uploaded PDFs.

### `POST /upload`
Uploads and processes a PDF file.
- **Request**: Multipart form data with `pdf` file
- **Response**: JSON with success status and filename

### `GET /chat`
Renders the chat interface with available PDFs.

### `POST /chat`
Sends a question to the chatbot.
- **Request**: JSON with `question` and `pdf_file`
- **Response**: JSON with answer, question, and chunks used

## Configuration

### OpenAI Models
The application uses:
- **Chat Model**: `gpt-4o-mini` (configurable in `pdfreader.py`)
- **Embedding Model**: `text-embedding-3-large` (configurable in `pdfreader.py`)

### Text Chunking
- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 200 characters
- **Separator**: Newline (`\n`)

### Similarity Search
- **Top K Results**: 3 chunks per query

## Development

### Running in Debug Mode
The Flask app runs in debug mode by default. To disable:
```python
app.run(debug=False)
```

### Adding New Features
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Troubleshooting

### Common Issues

**Issue**: "No module named 'langchain'"
- **Solution**: Make sure you've installed all requirements: `pip install -r requirements.txt`

**Issue**: "OpenAI API key not found"
- **Solution**: Create a `.env` file with your `OPENAI_API_KEY`

**Issue**: "FAISS index not found"
- **Solution**: Make sure you've uploaded and processed a PDF first

**Issue**: Upload fails silently
- **Solution**: Check the console for error messages and ensure the `uploads/` folder exists

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Author

**dispatchbyhenry-source**
- GitHub: [@dispatchbyhenry-source](https://github.com/dispatchbyhenry-source)

## Acknowledgments

- OpenAI for providing the GPT and embedding models
- LangChain team for the excellent framework
- Flask community for the web framework

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

---

**Note**: Make sure to keep your `.env` file secure and never commit it to version control. The `.gitignore` file is already configured to exclude it.

