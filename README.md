# POP QUOTE! 🎨

A pop-art inspired Python web app that serves a new random quote on every page load.
Built with Flask, deployable on [Railway](https://railway.app).

---

## Features

- **45 quotes** – humorous, philosophical, and optimistic, from famous thinkers, comedians, and icons
- **Every reload is unique** – randomised across:
  - 10 high-contrast pop-art color themes with Ben-Day halftone dot backgrounds
  - 8 display fonts (Bangers, Pacifico, Permanent Marker, Bevan, …)
  - 6 quote panel positions on screen
  - 6 panel border-radius shapes
  - Animated starburst badge (POW! / ZAP! / BOOM! / …) in a random corner
- **Pop-art aesthetic** – bold outlines, hard drop shadows, diagonal stripe accents, starburst badges
- **Click anywhere** to get a new quote instantly

---

## Project structure

```
.
├── app.py               # Flask application (routes + inline HTML/CSS template)
├── requirements.txt     # Python dependencies (Flask, gunicorn)
├── Procfile             # Process definition for Railway / Heroku
├── .python-version      # Python 3.11 pin for Nixpacks
├── setup.sh             # One-shot local setup: venv → install → run
└── .gitignore
```

---

## Run locally

### Option A – one command

```bash
./setup.sh
```

This script creates a `venv/`, activates it, installs all dependencies, and starts the development server.

### Option B – manual

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

---

## Deploy on Railway

1. Push this repo to GitHub (already done ✓)
2. Go to [railway.app](https://railway.app) → **New project** → **Deploy from GitHub repo**
3. Select the `helloworld` repository
4. Railway auto-detects Python via `requirements.txt` and uses the `Procfile` to start gunicorn
5. Click **Deploy** – that's it

Railway injects a `PORT` environment variable automatically; the app binds to it via:

```python
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
```

---

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Web framework | Flask 3.0 |
| Production server | gunicorn 22 |
| Fonts | Google Fonts (loaded client-side) |
| Hosting | Railway (Nixpacks build) |

---

## License

MIT
