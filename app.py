from promptivebackend import app

# This file is just a wrapper to make the app available as 'app:app' for gunicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000) 