from flask import Flask, render_template, request , jsonify
from langchain_community.document_loaders import PyPDFium2Loader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import pickle
from langchain.vectorstores import FAISS
from langchain_openai import ChatOpenAI
#from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

import os
import numpy as np
import faiss  # ADD THIS IMPORT


from dotenv import load_dotenv

load_dotenv()

UPLOAD_FOLDER = "uploads"
EMBEDDINGS_FOLDER = "embeddings"

# Create folders if they don't exist

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EMBEDDINGS_FOLDER, exist_ok=True)

# Initialize OpenAI embeddings
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large")
# Load embeddings from pickle

llm = ChatOpenAI(
    model="gpt-4o-mini",   # or gpt-4.1, gpt-4o, etc.
    temperature=0
)

# Prompt Template for LLM generation
prompt = PromptTemplate(
    input_variables=["question", "context"],
    template="""
You are a helpful AI assistant. Use ONLY the following document context to answer the question.
If the answer is not present in the provided context, respond with:
"The document does not contain this information."

Context:
{context}

Question:
{question}

Answer:
"""
)

def load_embeddings(file_path):
    with open(file_path, "rb") as f:
        data = pickle.load(f)
    texts = [item["text"] for item in data]
    vectors = np.array([item["embedding"] for item in data]).astype("float32")
    return texts, vectors

# Search FAISS index
def semantic_search(query, texts, vectors, top_k=3):
    query_vector = np.array(embeddings_model.embed_query(query)).astype("float32")
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    distances, indices = index.search(np.array([query_vector]), top_k)
    results = [texts[i] for i in indices[0]]
    return results

# Initialize Google Gemini embeddings

# embeddings_model = GoogleGenerativeAIEmbeddings()


app = Flask(__name__)

@app.route('/')
def index():
    # Get list of uploaded PDF files
    pdf_files = []
    if os.path.exists(UPLOAD_FOLDER):
        pdf_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.pdf')]
    return render_template('index.html', uploaded_files=pdf_files)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    try:
        if 'pdf' not in request.files:
            return jsonify({"success": False, "error": "No file uploaded"}), 400

        file = request.files['pdf']
        if file.filename == '':
            return jsonify({"success": False, "error": "No file selected"}), 400

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Use PyPDFium2Loader with the file path
        loader = PyPDFium2Loader(filepath)
        docs = loader.load()
        
        # Combine all text into a single string
        full_text = "\n".join([d.page_content for d in docs])

        # Split text into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n", 
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_text(full_text)

        vectorstore = FAISS.from_texts(chunks, embeddings_model)
        vectorstore_file = os.path.join(EMBEDDINGS_FOLDER, f"{file.filename}_faiss")
        vectorstore.save_local(vectorstore_file)


    # # Generate embeddings in batch
    # embeddings_vectors = embeddings_model.embed_documents(chunks)

    # # Create embeddings for each chunk
    
    # embeddings_list = [
    #     {"text": chunk, "embedding": vector}
    #     for chunk, vector in zip(chunks, embeddings_vectors)
    # ]

    # # for chunk in chunks:
    # #     embedding = embeddings_model.embed_query(chunk)
    # #     embeddings_list.append({
    # #         "text": chunk,
    # #         "embedding": embedding
    # #     })

    # # Save embeddings as a pickle file
    # embeddings_file = os.path.join(EMBEDDINGS_FOLDER, f"{file.filename}.pkl")
    # with open(embeddings_file, "wb") as f:
    #     pickle.dump(embeddings_list, f)

    # # formatted_chunks = "\n\n---\n\n".join(chunks)
    # # return f"<pre>{formatted_chunks}</pre>"

        return jsonify({
            "success": True,
            "message": "PDF uploaded and embeddings created successfully!",
            "filename": file.filename
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


    #xreturn f"<pre>{content}</pre>"

@app.route('/chat')
def chat_page():
    # Show chat interface
    # Dynamically list uploaded PDFs
    # pdf_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.pdf')]
    # return render_template('chat.html', pdf_files=pdf_files)
    pdf_files = [f for f in os.listdir(EMBEDDINGS_FOLDER) 
                 if os.path.isdir(os.path.join(EMBEDDINGS_FOLDER, f)) and f.endswith('_faiss')]
    return render_template('chat.html', pdf_files=pdf_files)

# @app.route('/chat', methods=['POST'])

# def chat():
#     data = request.json
#     user_question = data.get("question")
#     pdf_file = data.get("pdf_file")

#     if not pdf_file:
#         return jsonify({"error": "No PDF selected"}), 400

#     vectorstore_file = os.path.join(EMBEDDINGS_FOLDER, pdf_file)
#     if not os.path.exists(vectorstore_file):
#         return jsonify({"error": "Vectorstore not found"}), 404

#     # Load vectorstore
#     # with open(vectorstore_file, "rb") as f:
#     #     vectorstore = pickle.load(f)
#     vectorstore = FAISS.load_local(vectorstore_file, embeddings_model)


#     # Perform semantic search using LangChain
#     relevant_chunks = vectorstore.similarity_search(user_question, k=3)

#     # Extract text from Document objects
#     results = [doc.page_content for doc in relevant_chunks]

#     return jsonify({"relevant_chunks": results})
@app.route('/chat', methods=['POST'])
def chat():
    # Accept both JSON and form data
    if request.is_json:
        data = request.json
    else:
        data = request.form

    user_question = data.get("question")
    pdf_file = data.get("pdf_file")

    if not user_question or not pdf_file:
        return jsonify({"error": "Missing question or PDF"}), 400

    vectorstore_file = os.path.join(EMBEDDINGS_FOLDER, pdf_file)
    if not os.path.exists(vectorstore_file):
        return jsonify({"error": "Vectorstore not found"}), 404

    # Load FAISS vectorstore
    # vectorstore = FAISS.load_local(vectorstore_file, embeddings_model)
    vectorstore = FAISS.load_local(
        vectorstore_file,
        embeddings_model,
        allow_dangerous_deserialization=True
    )


    # EXPLICITLY create embedding for the user's question
    question_embedding = embeddings_model.embed_query(user_question)
    print(f"User Question: {user_question}")
    print(f"Question Embedding Created - Vector Dimension: {len(question_embedding)}")

    # Perform semantic search
    relevant_chunks = vectorstore.similarity_search_by_vector(question_embedding, k=3)

    results = [doc.page_content for doc in relevant_chunks]
    # Prepare LLM context
    context = "\n\n".join(results)

    # Generate final answer using OpenAI
    # chain = LLMChain(llm=llm, prompt=prompt)
    # final_answer = chain.run({
    #     "question": user_question,
    #     "context": context
    # })
    final_answer = llm.invoke(prompt.format( question=user_question, context=context )).content


    return jsonify({
        "question": user_question,
        "answer": final_answer,
        "chunks_used": results,
        "embedding_info": {
            "vector_dimension": len(question_embedding),
            "embedding_model": "text-embedding-3-large"
        }
    })
# def format_answer(chunks):
#     """Format the chunks into a readable answer"""
#     if not chunks:
#         return "No relevant information found."
    
#     formatted = "Based on the document, here's what I found:\n\n"
#     for i, chunk in enumerate(chunks, 1):
#         formatted += f"{i}. {chunk}\n\n"
#     return formatted

if __name__ == '__main__':
    app.run(debug=True)
