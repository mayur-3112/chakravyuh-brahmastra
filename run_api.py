"""
Brahmastra API Server Runner
Save as: ~/chakravyuh/brahmastra/run_api.py
"""

import uvicorn

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║          BRAHMASTRA REST API SERVER                   ║
║        Automated Threat Response Engine              ║
║              Project Chakravyuh                      ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝

Starting server on http://localhost:8000
API Documentation: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
    """)
    
    uvicorn.run(
        "brahmastra.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
