import uvicorn

def main():
    # host를 "0.0.0.0" 으로 하면 완전 개방
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()

