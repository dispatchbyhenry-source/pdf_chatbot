# Deploying to Vercel

This guide will help you deploy your PDF Reader & Chatbot application to Vercel.

## Prerequisites

1. A Vercel account (sign up at [vercel.com](https://vercel.com))
2. Vercel CLI installed (optional, for CLI deployment)
3. Your GitHub repository connected to Vercel

## Important Notes

⚠️ **Vercel Serverless Limitations:**
- Vercel serverless functions have a **read-only filesystem** (except `/tmp`)
- Files stored in `/tmp` are **temporary** and may be cleared between function invocations
- For production use, consider using:
  - **Vercel Blob Storage** for file uploads
  - **External database** (MongoDB, PostgreSQL) for storing embeddings
  - **Vector databases** (Pinecone, Weaviate) for embeddings

## Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard**
   - Visit [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "Add New Project"

2. **Import Your Repository**
   - Select your GitHub repository: `dispatchbyhenry-source/pdf_chatbot`
   - Click "Import"

3. **Configure Project Settings**
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: Leave empty (or `echo "No build needed"`)
   - **Output Directory**: Leave empty

4. **Add Environment Variables**
   - Click "Environment Variables"
   - Add: `OPENAI_API_KEY` = `your_openai_api_key_here`
   - Click "Save"

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI** (if not already installed)
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Add Environment Variables**
   ```bash
   vercel env add OPENAI_API_KEY
   ```
   Enter your OpenAI API key when prompted.

5. **Deploy to Production**
   ```bash
   vercel --prod
   ```

## Configuration Files

The project includes:
- `vercel.json` - Vercel configuration
- `api/index.py` - Serverless function handler
- `.vercelignore` - Files to exclude from deployment

## Environment Variables

Required environment variable:
- `OPENAI_API_KEY` - Your OpenAI API key

## File Storage Considerations

### Current Implementation
The app uses `/tmp` directory for file storage in Vercel, which means:
- ✅ Files can be uploaded and processed
- ⚠️ Files are **temporary** and may be lost
- ⚠️ Files are **not shared** between function invocations

### Recommended for Production

1. **Use Vercel Blob Storage** for PDF files:
   ```python
   from vercel import blob
   
   # Upload file
   blob.put(file_name, file_data)
   
   # Download file
   file_data = blob.get(file_name)
   ```

2. **Use External Vector Database** for embeddings:
   - Pinecone
   - Weaviate
   - Qdrant
   - Chroma

3. **Use Database** for metadata:
   - MongoDB
   - PostgreSQL
   - Supabase

## Testing the Deployment

After deployment:

1. Visit your Vercel URL (e.g., `https://your-project.vercel.app`)
2. Test PDF upload functionality
3. Test chat functionality

## Troubleshooting

### Issue: "Module not found"
- **Solution**: Ensure all dependencies are in `requirements.txt`
- Check that `vercel.json` is correctly configured

### Issue: "File not found" errors
- **Solution**: Files in `/tmp` are temporary. Consider using external storage.

### Issue: "OpenAI API key not found"
- **Solution**: Add `OPENAI_API_KEY` in Vercel environment variables

### Issue: "Function timeout"
- **Solution**: PDF processing can be slow. Consider:
  - Increasing function timeout in `vercel.json`
  - Using background jobs for processing
  - Optimizing PDF processing

### Issue: "FAISS index not found"
- **Solution**: Embeddings in `/tmp` are temporary. Use external vector database.

## Updating Deployment

After making changes:

1. **Via GitHub**: Push to your repository, Vercel will auto-deploy
2. **Via CLI**: Run `vercel --prod`

## Support

For Vercel-specific issues, check:
- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Python Runtime](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)

---

**Note**: For production use with persistent file storage, consider migrating to external storage solutions as mentioned above.

