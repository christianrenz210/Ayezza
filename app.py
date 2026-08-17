import os

from flask import Flask, render_template

app = Flask(__name__)

HERO_SLIDES = [
    {"img": "img/ayezza(0).jpg", "title": "Ayezza No. 01", "text": "Teal frame study"},
    {"img": "img/ayezza(1).jpg", "title": "Ayezza No. 02", "text": "Plum frame study"},
    {"img": "img/placeholder.svg", "title": "Ayezza Gallery", "text": "Golden ratio edition"},
]

GALLERY_ITEMS = [
    {"id": 1, "title": "Ayezza No. 01", "caption": "Ayezza 0 frame", "img": "img/ayezza(0).jpg"},
    {"id": 2, "title": "Ayezza No. 02", "caption": "Ayezza 1 frame", "img": "img/ayezza(1).jpg"},
    {"id": 3, "title": "Ayezza No. 03", "caption": "Placeholder frame", "img": "img/placeholder.svg"},
    {"id": 4, "title": "Ayezza No. 04", "caption": "Placeholder frame", "img": "img/placeholder.svg"},
    {"id": 5, "title": "Ayezza No. 05", "caption": "Placeholder frame", "img": "img" and "img/placeholder.svg"},
    {"id": 6, "title": "Ayezza No. 06", "caption": "Placeholder frame", "img": "img/placeholder.svg"},
    {"id": 7, "title": "Ayezza No. 07", "caption": "Placeholder frame", "img": "img/placeholder.svg"},
    {"id": 8, "title": "Ayezza No. 08", "caption": "Placeholder frame", "img": "img/placeholder.svg"},
]

CATEGORIES = [
    {
        "name": "Ayezza Zero",
        "icon": "bi-folder2",
        "images": [
            {"title": "Ayezza No. 01", "caption": "Ayezza 0 frame", "img": "img/ayezza(0).jpg"},
        ],
    },
    {
        "name": "Ayezza One",
        "icon": "bi-folder2-open",
        "images": [
            {"title": "Ayezza No. 02", "caption": "Ayezza 1 frame", "img": "img/ayezza(1).jpg"},
        ],
    },
    {
        "name": "Frames",
        "icon": "bi-folder",
        "images": [
            {"title": "Ayezza No. 03", "caption": "Placeholder frame", "img": "img/placeholder.svg"},
            {"title": "Ayezza No. 04", "caption": "Placeholder frame", "img": "img/placeholder.svg"},
            {"title": "Ayezza No. 05", "caption": "Placeholder frame", "img": "img/placeholder.svg"},
            {"title": "Ayezza No. 06", "caption": "Placeholder frame", "img": "img/placeholder.svg"},
            {"title": "Ayezza No. 07", "caption": "Placeholder frame", "img": "img/placeholder.svg"},
            {"title": "Ayezza No. 08", "caption": "Placeholder frame", "img": "img/placeholder.svg"},
        ],
    },
]


@app.route("/")
def gallery():
    return render_template("index.html", items=GALLERY_ITEMS, slides=HERO_SLIDES, categories=CATEGORIES)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
