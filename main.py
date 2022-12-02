from flask import Flask, request, render_template, redirect, send_file, session
import pytube
from pytube import YouTube
from pytube.cli import on_progress
from os.path import expanduser


app = Flask(__name__)
app.config['SECRET_KEY'] = "super super secret key"

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/download", methods=["GET", "POST"])
def download():
    if request.method == "POST":
        session["link"] = request.form.get("link")
        url = YouTube(session['link'], on_progress_callback=on_progress)
        return render_template("see_video.html", url=url)
    return render_template("index.html")

@app.route("/see_video", methods=["GET", "POST"])
def see_video():
    if request.method == "POST":
        url = YouTube(session['link'])
        itag = request.form.get('itag')
        video = url.streams.get_by_itag(itag)
        filename = video.download()
        return send_file(filename, as_attachment=True)
    return redirect("/download")

if __name__ == "__main__":
    app.run(debug=True)
