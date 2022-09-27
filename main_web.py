import stua, time
import dotenv, os
from flask import Flask, render_template, Response

dotenv.load_dotenv()
stua.keyMTA(os.getenv("NYCT"))#os.getenv("NYCT"))
stua.keyBUSTIME(os.getenv("BusTime"))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/broadway')
def broadway():
    def generate():
        value = True
        while (value == True):
            yield "data:" + f'<img src="static/svg/2.svg">' + "\n\n"
            time.sleep(5)
            #print('Restart B')
    return Response(generate(), mimetype= 'text/event-stream')

if __name__ in "__main__":
    app.run()
