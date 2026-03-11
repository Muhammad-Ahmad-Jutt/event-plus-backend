from app import create_app, socketio
from dotenv import load_dotenv
app = create_app()
load_dotenv()   

if __name__ == "__main__":
    # app.run(
    #     host="0.0.0.0",
    #     port=5000,
    #     debug=True
    # )
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)