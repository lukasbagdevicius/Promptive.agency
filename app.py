from promptivebackend import app
from asgiref.wsgi import WsgiToAsgi

# Wrap the FastAPI app with WSGI middleware
wsgi_app = WsgiToAsgi(app)

# This file is just a wrapper to make the app available as 'app:wsgi_app' for gunicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000) 