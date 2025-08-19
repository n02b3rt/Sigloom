import uvicorn
from .settings import settings

def main():
    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=False,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )

if __name__ == "__main__":
    main()
