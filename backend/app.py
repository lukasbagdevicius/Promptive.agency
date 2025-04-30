import os
import threading
import gradio as gr
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from .chat import chat_response

# Initialize FastAPI app
app = FastAPI(
    title="Promptive API",
    description="API for Promptive Agency Chatbot",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ChatRequest(BaseModel):
    message: str
    history: list = []

# Routes
@app.get("/")
async def root():
    return {
        "message": "Welcome to Promptive API",
        "endpoints": {
            "chat": "/chat",
            "docs": "/docs"
        },
        "status": "online"
    }

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        print("🔔 Incoming message:", request.message)
        print("📝 Message history length:", len(request.history))
        reply = chat_response(request.message, request.history)
        print("✅ Response generated successfully")
        return {"response": reply}
    except Exception as e:
        print("🔥 FULL ENDPOINT ERROR:", str(e))
        return {"response": f"⚠️ Internal error: {str(e)}"}

# Gradio interface for local development
demo = gr.ChatInterface(
    fn=chat_response,
    title="Promptive.Agency consultant",
    description="Ask me about Promptive.Agency!",
    examples=[
        "What your company does?",
        "How you can help me with my business?",
        "How much does it cost",
        "Can I contact you?",
    ],
    theme=gr.themes.Soft(primary_hue="purple", secondary_hue="pink")
)

def run_fastapi():
    # Get port from environment variable with fallback to 8000
    port = int(os.environ.get("PORT", 8000))
    print(f"✅ Starting FastAPI server on port {port}")
    print(f"✅ Environment: {'Production (Render)' if os.environ.get('RENDER') else 'Local Development'}")
    print(f"✅ Module path: backend.app:app")
    uvicorn.run(
        "backend.app:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        reload=False  # Disable reload in production
    )

# Run FastAPI on Render, Gradio locally
if __name__ == "__main__":
    if os.environ.get("RENDER"):
        # Running on Render - only start FastAPI
        run_fastapi()
    else:
        # Running locally - start both FastAPI and Gradio
        threading.Thread(target=run_fastapi).start()
        demo.launch(share=True) 