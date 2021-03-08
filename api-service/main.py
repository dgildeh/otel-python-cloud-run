from api_service import api, config

app = api

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=config.LISTEN_HOST, port=config.LISTEN_PORT, reload=True)