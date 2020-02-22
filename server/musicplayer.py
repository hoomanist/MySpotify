from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/musicplayer"
mongo = PyMongo(app)
@app.route('/')
def main():
   return """
   <div class='main'>
   <h1>
      hooman musicplayer
   </h1>
   <h2>this is a simple funny project that written as a flask training it is a clone of spotify</h2>
   </div>

   <a href="/musics">show musics</a>
   <a href="/upload">upload musics</a>
   """


@app.route('/upload')
def upload():
    return """
      <h4> in your music name shouldn't be ' please before upload replace it with - or \</h4>
       <form method="post" action="save" enctype="multipart/form-data">
          <input name="music" type="file">
          <input type="submit">
       </form>
    """

@app.route('/save', methods=['POST'])
def save():
    file = request.files["music"]
    mongo.save_file(file.filename,file)
    return f"done! {file.filename} is uploaded <br><a href='/'>return to mine window</a>"


@app.route('/musics')
def ShowMusics():
   files = list(mongo.db.fs.files.find())
   ret = ""
   for i in files:
      filename = i["filename"]
      ret += f"<a href='/media/{filename}'>{filename}</a> <br>"
   return ret


@app.route('/media/<file>')
def MusicFile(file):
   return mongo.send_file(file)

