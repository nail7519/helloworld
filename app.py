import os
import random
from flask import Flask, render_template_string
from quotes import QUOTES

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Pop-art color themes  (bg, dot overlay, panel, text-on-panel, meta/author)
# ---------------------------------------------------------------------------
THEMES = [
    {"bg": "#FFE600", "dot": "rgba(0,0,0,0.06)", "panel": "#FF0044", "text": "#FFFFFF", "meta": "#FFE600"},
    {"bg": "#00E5FF", "dot": "rgba(0,0,0,0.06)", "panel": "#CC00AA", "text": "#FFFFFF", "meta": "#00E5FF"},
    {"bg": "#FF2200", "dot": "rgba(255,255,255,0.1)", "panel": "#FFE600", "text": "#000000", "meta": "#FF2200"},
    {"bg": "#39FF14", "dot": "rgba(0,0,0,0.06)", "panel": "#7700EE", "text": "#FFFFFF", "meta": "#39FF14"},
    {"bg": "#FF6600", "dot": "rgba(0,0,0,0.06)", "panel": "#111111", "text": "#FFFFFF", "meta": "#FF6600"},
    {"bg": "#1133FF", "dot": "rgba(255,255,255,0.1)", "panel": "#FFE600", "text": "#000000", "meta": "#FFB300"},
    {"bg": "#FF0099", "dot": "rgba(0,0,0,0.06)", "panel": "#00CCFF", "text": "#000000", "meta": "#FFFFFF"},
    {"bg": "#FFFFFF", "dot": "rgba(0,0,0,0.05)", "panel": "#FF2200", "text": "#FFFFFF", "meta": "#FF2200"},
    {"bg": "#7700EE", "dot": "rgba(255,255,255,0.1)", "panel": "#FFE600", "text": "#000000", "meta": "#FFFFFF"},
    {"bg": "#111111", "dot": "rgba(255,255,255,0.07)", "panel": "#FF2200", "text": "#FFFFFF", "meta": "#FFE600"},
]

# ---------------------------------------------------------------------------
# Google Fonts – all loaded in one request
# ---------------------------------------------------------------------------
GOOGLE_FONTS_URL = (
    "https://fonts.googleapis.com/css2?family=Bangers"
    "&family=Lilita+One"
    "&family=Fredoka+One"
    "&family=Boogaloo"
    "&family=Righteous"
    "&family=Permanent+Marker"
    "&family=Pacifico"
    "&family=Bevan"
    "&display=swap"
)

FONTS = [
    "Bangers",
    "Lilita One",
    "Fredoka One",
    "Boogaloo",
    "Righteous",
    "Permanent Marker",
    "Pacifico",
    "Bevan",
]

# (justify-content, align-items, text-align)
POSITIONS = [
    ("center", "center", "center"),
    ("flex-start", "flex-start", "left"),
    ("flex-end", "flex-end", "right"),
    ("center", "flex-start", "center"),
    ("flex-end", "center", "right"),
    ("flex-start", "center", "left"),
]

BADGE_WORDS = ["POW!", "ZAP!", "BAM!", "WOW!", "YES!", "BOOM!", "RAD!", "KAPOW!", "WHAM!", "OMG!"]

BADGE_POSITIONS = [
    "top: 24px; left: 24px;",
    "top: 24px; right: 24px;",
    "bottom: 24px; left: 24px;",
    "bottom: 24px; right: 24px;",
]

BORDER_RADII = [
    "6px",
    "32px",
    "60px",
    "0px",
    "8px 48px 8px 48px",
    "48px 8px 48px 8px",
]

# ---------------------------------------------------------------------------
# HTML / CSS template  (Jinja2 via render_template_string)
# CSS single-braces do NOT conflict with Jinja2 double-brace syntax.
# ---------------------------------------------------------------------------
TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>POP QUOTE!</title>
  <link href="{{ fonts_url }}" rel="stylesheet">
  <style>
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

    html, body {
      height: 100%;
    }

    body {
      min-height: 100vh;
      /* Ben-Day halftone dots */
      background-color: {{ bg }};
      background-image: radial-gradient(
        circle,
        {{ dot }} 14%,
        transparent 14%
      );
      background-size: 22px 22px;

      display: flex;
      justify-content: {{ justify }};
      align-items: {{ align }};
      padding: 40px 32px;

      font-family: '{{ font }}', cursive;
      cursor: pointer;
      user-select: none;
      transition: background-color 0.1s ease;
    }

    /* ── Quote panel ─────────────────────────────── */
    .wrapper {
      position: relative;
      max-width: 820px;
      width: 100%;
    }

    .quote-box {
      background: {{ panel }};
      border: 6px solid #000;
      border-radius: {{ border_radius }};
      padding: 56px 64px 44px;
      box-shadow: 14px 14px 0 #000;
      text-align: {{ text_align }};
      position: relative;
    }

    .quote-box:active {
      transform: translate(4px, 4px);
      box-shadow: 10px 10px 0 #000;
    }

    /* decorative opening quote mark */
    .open-q {
      position: absolute;
      top: 4px;
      left: 18px;
      font-size: 110px;
      line-height: 1;
      color: {{ meta }};
      opacity: 0.25;
      font-family: Georgia, 'Times New Roman', serif;
      font-weight: 900;
      pointer-events: none;
      z-index: 0;
    }

    .quote-text {
      font-family: '{{ font }}', cursive;
      font-size: clamp(20px, {{ fs }}vw, 52px);
      color: {{ text }};
      line-height: 1.45;
      letter-spacing: 0.3px;
      text-shadow: 3px 3px 0 rgba(0,0,0,0.3);
      margin-bottom: 28px;
      position: relative;
      z-index: 1;
    }

    .divider {
      width: 60px;
      height: 5px;
      background: {{ meta }};
      border: 2px solid rgba(0,0,0,0.2);
      margin-bottom: 16px;
      margin-left: {{ div_ml }};
      margin-right: {{ div_mr }};
    }

    .author {
      font-family: 'Bangers', cursive;
      font-size: clamp(18px, 2.2vw, 28px);
      color: {{ meta }};
      letter-spacing: 4px;
      text-transform: uppercase;
      text-shadow: 2px 2px 0 rgba(0,0,0,0.3);
    }

    /* ── Starburst badge ─────────────────────────── */
    .badge {
      position: fixed;
      {{ badge_pos }}
      background: {{ bg }};
      color: {{ panel }};
      font-family: 'Bangers', cursive;
      font-size: clamp(16px, 2.2vw, 28px);
      letter-spacing: 3px;
      width: 108px;
      height: 108px;
      display: flex;
      align-items: center;
      justify-content: center;
      /* 8-pointed star */
      clip-path: polygon(
        50%  0%, 62% 22%, 85% 15%, 78% 38%,
        100% 50%, 78% 62%, 85% 85%, 62% 78%,
        50% 100%, 38% 78%, 15% 85%, 22% 62%,
        0%  50%, 22% 38%, 15% 15%, 38% 22%
      );
      transform: rotate({{ badge_rot }}deg);
      filter: drop-shadow(4px 4px 0 rgba(0,0,0,0.65));
      z-index: 200;
      animation: badge-pulse 2.6s ease-in-out infinite alternate;
    }

    @keyframes badge-pulse {
      from { transform: rotate({{ badge_rot }}deg) scale(1);    }
      to   { transform: rotate({{ badge_rot_end }}deg) scale(1.13); }
    }

    /* ── Reload hint ─────────────────────────────── */
    .reload-hint {
      position: fixed;
      bottom: 14px;
      right: 18px;
      font-family: 'Bangers', cursive;
      font-size: 13px;
      letter-spacing: 2px;
      color: {{ panel }};
      background: {{ bg }};
      border: 3px solid #000;
      padding: 4px 12px;
      opacity: 0.72;
      z-index: 200;
      pointer-events: none;
    }

    /* ── Stripe accent behind panel ─────────────── */
    .stripe {
      position: absolute;
      top: -10px;
      left: 10px;
      right: -10px;
      bottom: 10px;
      background: repeating-linear-gradient(
        45deg,
        transparent,
        transparent 6px,
        rgba(0,0,0,0.08) 6px,
        rgba(0,0,0,0.08) 12px
      );
      border-radius: {{ border_radius }};
      z-index: -1;
    }
  </style>
</head>

<body onclick="location.reload()" title="Click anywhere to get a new quote!">

  <div class="badge">{{ badge_word }}</div>

  <div class="wrapper">
    <div class="stripe" aria-hidden="true"></div>
    <div class="quote-box">
      <span class="open-q" aria-hidden="true">&ldquo;</span>
      <p class="quote-text">{{ quote }}</p>
      <div class="divider"></div>
      <p class="author">&mdash;&nbsp;{{ author }}</p>
    </div>
  </div>

  <div class="reload-hint">CLICK TO RELOAD</div>

</body>
</html>"""


# ---------------------------------------------------------------------------
# Route
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    quote, author = random.choice(QUOTES)
    theme = random.choice(THEMES)
    font = random.choice(FONTS)
    justify, align, text_align = random.choice(POSITIONS)
    badge_word = random.choice(BADGE_WORDS)
    badge_pos = random.choice(BADGE_POSITIONS)
    border_radius = random.choice(BORDER_RADII)
    badge_rot = random.randint(-18, 18)
    badge_rot_end = badge_rot + random.choice([-1, 1]) * random.randint(6, 14)

    # Responsive font-size in vw units, capped by clamp() in CSS
    fs = round(max(2.0, min(4.8, 170 / len(quote))), 2)

    # Divider alignment mirrors text-align
    if text_align == "center":
        div_ml, div_mr = "auto", "auto"
    elif text_align == "right":
        div_ml, div_mr = "auto", "0"
    else:
        div_ml, div_mr = "0", "auto"

    return render_template_string(
        TEMPLATE,
        quote=quote,
        author=author,
        font=font,
        fonts_url=GOOGLE_FONTS_URL,
        justify=justify,
        align=align,
        text_align=text_align,
        badge_word=badge_word,
        badge_pos=badge_pos,
        badge_rot=badge_rot,
        badge_rot_end=badge_rot_end,
        border_radius=border_radius,
        fs=fs,
        div_ml=div_ml,
        div_mr=div_mr,
        **theme,
    )


# ---------------------------------------------------------------------------
# Entry point  (Railway injects PORT; fallback to 5000 locally)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
