import uvicorn
import os

if __name__ == "__main__":
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # Important: listen on all interfaces
        port=port,
        reload=False  # Disable auto-reload in production
    )
