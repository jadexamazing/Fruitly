import streamlit as st
import numpy as np
from PIL import Image
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Fruitly · Fruit Scanner",
    page_icon="🍓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CUSTOM CSS  —  deep mauve · dusty sage · warm taupe
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:          #1E1A1F;
    --surface:     #2A2330;
    --surface2:    #322A3A;
    --border:      rgba(180,150,180,.15);
    --mauve:       #C9A8C0;
    --mauve-deep:  #9B6B95;
    --sage:        #8BAF8E;
    --sage-dim:    #5A7B5D;
    --taupe:       #C4AD99;
    --terra:       #C47E6A;
    --text:        #EDE0E8;
    --text-muted:  #8C7A90;
    --text-dim:    #5E5062;
    --shadow:      rgba(0,0,0,.4);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
    background-color: var(--bg);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 5rem; max-width: 1200px; margin: 0 auto; }

/* Ambient layered glow */
body::before {
    content: "";
    position: fixed; inset: 0;
    background-image:
        radial-gradient(ellipse 60% 40% at 95%   0%, rgba(155,107,149,.20) 0%, transparent 55%),
        radial-gradient(ellipse 50% 35% at  5% 100%, rgba(139,175,142,.14) 0%, transparent 55%),
        radial-gradient(ellipse 35% 28% at 50%  52%, rgba(196,126,106,.07) 0%, transparent 60%);
    pointer-events: none; z-index: 0;
}

/* Botanical canvas pinned behind everything */
#bg-botanical {
    position: fixed; inset: 0;
    width: 100vw; height: 100vh;
    pointer-events: none; z-index: 0;
    opacity: 1;
}

/* ── Hero ── */
.hero { text-align:center; padding: 3rem 1rem 1.8rem; }
.hero-badge {
    display: inline-block;
    background: rgba(201,168,192,.08);
    color: var(--mauve);
    font-size: .67rem; font-weight: 500;
    letter-spacing: .18em; text-transform: uppercase;
    padding: .38rem 1.1rem; border-radius: 999px;
    margin-bottom: 1rem;
    border: 1px solid rgba(201,168,192,.22);
}
.hero h1 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.4rem; font-weight: 600;
    color: var(--text); margin: 0 0 .5rem;
    line-height: 1.1; letter-spacing: -.01em;
}
.hero h1 span { color: var(--mauve); font-style: italic; }
.hero p { color: var(--text-muted); font-size: .95rem; font-weight: 300; margin: 0; }

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(201,168,192,.28), transparent);
    margin: 2rem 0; border: none;
}

/* ── Card ── */
.card {
    background: var(--surface);
    border-radius: 18px; padding: 1.8rem 2rem;
    box-shadow: 0 8px 32px var(--shadow);
    border: 1px solid var(--border);
    margin-bottom: 1.4rem;
    position: relative; overflow: hidden;
}
.card::before {
    content: ""; position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--mauve-deep), var(--sage-dim), var(--terra));
    opacity: .65;
}

/* ── Section title ── */
.section-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.2rem; font-weight: 600;
    color: var(--text); margin-bottom: 1rem;
    display: flex; align-items: center; gap: .5rem;
}
.section-title .dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--mauve); display: inline-block; flex-shrink: 0;
}

/* ── Result hero ── */
.result-hero {
    text-align: center; padding: 2rem 1.5rem;
    background: linear-gradient(135deg, rgba(155,107,149,.16) 0%, rgba(139,175,142,.10) 100%);
    border-radius: 16px; margin-bottom: 1.4rem;
    border: 1px solid rgba(201,168,192,.13);
}
.result-hero .fruit-emoji {
    font-size: 3.8rem; margin-bottom: .4rem; display: block;
    filter: drop-shadow(0 4px 12px rgba(0,0,0,.5));
}
.result-hero .fruit-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.6rem; font-weight: 600;
    color: var(--text); text-transform: capitalize;
    margin-bottom: .5rem; letter-spacing: -.01em;
}
.result-hero .confidence-pill {
    display: inline-block;
    background: linear-gradient(135deg, var(--mauve-deep), #7A5077);
    color: #F5EEF5; font-size: .82rem; font-weight: 500;
    padding: .32rem 1rem; border-radius: 999px; letter-spacing: .02em;
}

/* ── Progress bars ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--mauve-deep), var(--mauve)) !important;
    border-radius: 999px !important;
}
.stProgress > div > div {
    background: rgba(201,168,192,.1) !important;
    border-radius: 999px !important; height: 8px !important;
}

/* ── Chips ── */
.chip-grid { display:flex; flex-wrap:wrap; gap:.45rem; margin-top:.5rem; }
.chip {
    background: rgba(201,168,192,.1); color: var(--mauve);
    border: 1px solid rgba(201,168,192,.2); border-radius: 999px;
    padding: .26rem .8rem; font-size: .8rem;
}
.chip.green  { background:rgba(139,175,142,.1); color:var(--sage);  border-color:rgba(139,175,142,.25); }
.chip.orange { background:rgba(196,126,106,.1); color:var(--terra); border-color:rgba(196,126,106,.25); }
.chip.taupe  { background:rgba(196,173,153,.1); color:var(--taupe); border-color:rgba(196,173,153,.25); }

.caution-item {
    font-size: .8rem;
    color: #7A9EBF;
    line-height: 1.5;
    padding: .3rem 0 .3rem .2rem;
    border-left: 2px solid rgba(122,158,191,.25);
    padding-left: .7rem;
    margin-bottom: .5rem;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px; background: var(--surface2);
    border-radius: 14px; padding: 5px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    background: transparent; border-radius: 10px;
    color: var(--text-muted); font-weight: 500;
    font-size: .88rem; padding: .48rem 1.4rem; border: none;
}
.stTabs [aria-selected="true"] {
    background: var(--surface) !important;
    color: var(--mauve) !important;
    box-shadow: 0 2px 10px var(--shadow);
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.4rem; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--mauve-deep), #7A4F78) !important;
    color: #F5EEF5 !important; border: none !important;
    border-radius: 12px !important; font-family:'DM Sans',sans-serif !important;
    font-weight: 500 !important; font-size: .88rem !important;
    padding: .55rem 1.6rem !important;
    box-shadow: 0 4px 16px rgba(155,107,149,.28) !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(155,107,149,.4) !important;
}
.reset-btn > button {
    background: rgba(255,255,255,.04) !important;
    color: var(--text-muted) !important;
    box-shadow: none !important; font-size: .82rem !important;
    padding: .4rem 1.1rem !important;
    border: 1px solid var(--border) !important;
}
.reset-btn > button:hover {
    background: rgba(255,255,255,.07) !important;
    transform: none !important; box-shadow: none !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] section {
    border: 1.5px dashed rgba(201,168,192,.28) !important;
    border-radius: 14px !important;
    background: rgba(201,168,192,.04) !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: rgba(201,168,192,.48) !important;
}

/* ── Camera ── */
[data-testid="stCameraInput"] > div {
    border-radius: 14px !important; overflow: hidden;
    border: 1px solid var(--border) !important;
}

.stImage img { border-radius: 12px; }
.stSpinner > div { border-top-color: var(--mauve) !important; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--surface2); border-radius: 999px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FRUIT INFO  —  Apple, Banana, Pineapple, Cucumber, Orange, Strawberry
# ─────────────────────────────────────────────
FRUIT_INFO = {
    "apple": {
        "emoji": "🍎",
        "benefits": ["Rich in dietary fiber & pectin", "High in Vitamin C & antioxidants", "Supports heart & gut health", "Linked to lower diabetes risk"],
        "pros":     ["Widely available year-round", "Affordable & portable", "Long shelf life", "Versatile in sweet & savory recipes"],
        "cons":     ["High in natural sugars", "Pesticide residue risk — wash well", "May cause bloating in sensitive individuals"],
        "avoid":    ["People with fructose intolerance", "Those on very low-sugar diets", "Individuals with latex-fruit allergy syndrome"],
        "cautions": ["Apple seeds contain amygdalin — avoid consuming in large amounts", "Unpeeled apples may carry pesticide residue — opt for organic when possible", "Applesauce or juice removes fiber — whole fruit is always preferred"],
    },
    "banana": {
        "emoji": "🍌",
        "benefits": ["Excellent potassium source", "Quick, sustained energy boost", "Rich in Vitamin B6 & magnesium", "Supports digestive regularity"],
        "pros":     ["Very affordable", "No prep needed", "Natural sweetener substitute", "Great pre/post-workout snack"],
        "cons":     ["High glycemic index when overripe", "Short shelf life once ripe", "Higher in carbs than most fruits"],
        "avoid":    ["People with chronic kidney disease (high potassium)", "Those managing type 2 diabetes closely", "Individuals with banana or latex allergy"],
        "cautions": ["Overripe bananas spike blood sugar faster — choose firm, slightly green ones for lower GI", "Avoid eating on an empty stomach if prone to acid reflux", "High potassium content can be dangerous for those on potassium-sparing diuretics"],
    },
    "pineapple": {
        "emoji": "🍍",
        "benefits": ["Contains bromelain — aids digestion", "Very high in Vitamin C", "Anti-inflammatory properties", "Supports immune function"],
        "pros":     ["Bold tropical flavor", "Works in sweet & savory dishes", "Canned version available year-round"],
        "cons":     ["Can irritate mouth tissue", "High natural sugar content", "Prep and coring is time-consuming"],
        "avoid":    ["Pregnant women in large amounts (bromelain may stimulate uterine contractions)", "People with pineapple or bromelain allergy", "Those with gastric ulcers or severe acid reflux"],
        "cautions": ["Bromelain can interact with blood thinners like warfarin — consult a doctor", "May tenderize meat proteins — avoid eating large amounts before dental procedures", "Canned pineapple in syrup has significantly higher sugar — choose juice-packed or fresh"],
    },
    "cucumber": {
        "emoji": "🥒",
        "benefits": ["96% water — deeply hydrating", "Very low in calories", "Contains antioxidants & silica", "Supports skin hydration from within"],
        "pros":     ["Extremely low calorie", "Refreshing raw snack", "Easy to grow at home", "No prep needed for most uses"],
        "cons":     ["Low in macro-nutrients", "Can be bitter if not fresh", "Short shelf life once cut"],
        "avoid":    ["People with cucumber or gourd allergy", "Those with sensitive digestive systems prone to bloating", "Individuals on blood-thinning medication (Vitamin K content)"],
        "cautions": ["Bitter cucumbers may contain cucurbitacins — discard any extremely bitter specimens", "Waxed store cucumbers should be peeled or thoroughly scrubbed", "Eating very large quantities may cause fluid imbalances due to high water content"],
    },
    "orange": {
        "emoji": "🍊",
        "benefits": ["Exceptionally high in Vitamin C", "Boosts immune system", "Rich in folate & thiamine", "Supports collagen production"],
        "pros":     ["Naturally hydrating", "Great for fresh juice", "Good dietary fiber source"],
        "cons":     ["Acidic — may irritate sensitive stomachs", "High in natural sugars", "Peeling can be messy"],
        "avoid":    ["People with GERD or chronic acid reflux", "Those with citrus allergy", "Individuals with mouth ulcers or canker sores"],
        "cautions": ["Orange juice lacks fiber and delivers sugar faster — whole fruit is preferable", "Can erode tooth enamel — rinse mouth with water after eating", "May interact with certain medications (similar to grapefruit in some cases — check with your doctor)"],
    },
    "strawberry": {
        "emoji": "🍓",
        "benefits": ["Among highest Vitamin C fruits", "Rich in anthocyanin antioxidants", "Anti-inflammatory & heart-protective", "Supports brain health"],
        "pros":     ["Low in calories", "Naturally sweet with no prep", "Versatile in desserts, drinks & salads"],
        "cons":     ["Highly perishable", "Pesticide residue concern", "Out-of-season varieties can be bland"],
        "avoid":    ["People with strawberry or salicylate allergy", "Those prone to kidney stones (high oxalate content)", "Individuals with histamine intolerance"],
        "cautions": ["One of the highest-pesticide fruits — strongly recommended to buy organic", "High oxalate content — moderate intake if prone to kidney stones", "Unwashed strawberries may harbor surface bacteria — always rinse thoroughly before eating"],
    },
}

def get_fruit_info(label: str):
    label_clean = label.strip().lower()
    for key in FRUIT_INFO:
        if key in label_clean or label_clean in key:
            return FRUIT_INFO[key], key
    return None, label_clean

# ─────────────────────────────────────────────
# MODEL LOADING
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    model_path  = "keras_model.h5"
    labels_path = "labels.txt"
    errors = []

    if not os.path.exists(model_path):
        errors.append("`keras_model.h5` not found — place it in the same folder as this script.")
    if not os.path.exists(labels_path):
        errors.append("`labels.txt` not found — place it in the same folder as this script.")
    if errors:
        return None, [], errors

    try:
        import tensorflow as tf
        # Fix for TF 2.13+ where tf.keras may not be directly accessible
        try:
            from tensorflow import keras
        except ImportError:
            import keras
        model = keras.models.load_model(model_path, compile=False)
    except Exception as e:
        return None, [], [f"Failed to load model: {e}"]

    with open(labels_path, "r") as f:
        labels = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(" ", 1)
            labels.append(parts[1] if len(parts) == 2 and parts[0].isdigit() else line)

    return model, labels, []

# ─────────────────────────────────────────────
# PREPROCESSING
# ─────────────────────────────────────────────
def preprocess_image(img: Image.Image, target_size=(224, 224)) -> np.ndarray:
    """Teachable Machine MobileNet: resize to 224×224, normalize to [-1, 1]."""
    img = img.convert("RGB").resize(target_size, Image.LANCZOS)
    arr = np.array(img, dtype=np.float32)
    arr = (arr / 127.5) - 1.0
    return np.expand_dims(arr, axis=0)

def predict(model, labels: list, img: Image.Image):
    preds = model.predict(preprocess_image(img), verbose=0)[0]
    return sorted(zip(labels, preds.tolist()), key=lambda x: x[1], reverse=True)

# ─────────────────────────────────────────────
# RESULTS RENDERER
# ─────────────────────────────────────────────
def render_results(results):
    top_label, top_conf = results[0]
    info, _ = get_fruit_info(top_label)
    emoji   = info["emoji"] if info else "🍑"

    st.markdown(f"""
    <div class="result-hero">
        <span class="fruit-emoji">{emoji}</span>
        <div class="fruit-name">{top_label.capitalize()}</div>
        <span class="confidence-pill">{top_conf * 100:.1f}% confidence</span>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title"><span class="dot"></span>Confidence Breakdown</div>', unsafe_allow_html=True)
        for label, conf in results:
            is_top = label == top_label
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'margin-bottom:.25rem;font-size:.86rem;'
                f'font-weight:{"600" if is_top else "400"};'
                f'color:{"#EDE0E8" if is_top else "#8C7A90"}">'
                f'<span>{"✦ " if is_top else ""}{label.capitalize()}</span>'
                f'<span>{conf * 100:.1f}%</span></div>',
                unsafe_allow_html=True,
            )
            st.progress(float(conf))
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        if info:
            # Benefits
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title"><span class="dot"></span>Benefits</div>', unsafe_allow_html=True)
            chips = "".join(f'<span class="chip">{b}</span>' for b in info["benefits"])
            st.markdown(f'<div class="chip-grid">{chips}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Pros & Cons
            st.markdown('<div class="card">', unsafe_allow_html=True)
            pc1, pc2 = st.columns(2)
            with pc1:
                st.markdown('<div class="section-title" style="font-size:1rem"><span class="dot" style="background:#8BAF8E"></span>Pros</div>', unsafe_allow_html=True)
                chips = "".join(f'<span class="chip green">{p}</span>' for p in info["pros"])
                st.markdown(f'<div class="chip-grid">{chips}</div>', unsafe_allow_html=True)
            with pc2:
                st.markdown('<div class="section-title" style="font-size:1rem"><span class="dot" style="background:#C47E6A"></span>Cons</div>', unsafe_allow_html=True)
                chips = "".join(f'<span class="chip orange">{c}</span>' for c in info["cons"])
                st.markdown(f'<div class="chip-grid">{chips}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Who Should Avoid & Cautions
            st.markdown('<div class="card">', unsafe_allow_html=True)
            av1, av2 = st.columns(2)
            with av1:
                st.markdown('<div class="section-title" style="font-size:1rem"><span class="dot" style="background:#C4AD99"></span>Who Should Avoid</div>', unsafe_allow_html=True)
                chips = "".join(f'<span class="chip taupe">{a}</span>' for a in info["avoid"])
                st.markdown(f'<div class="chip-grid">{chips}</div>', unsafe_allow_html=True)
            with av2:
                st.markdown('<div class="section-title" style="font-size:1rem"><span class="dot" style="background:#7A9EBF"></span>Cautions</div>', unsafe_allow_html=True)
                for c in info["cautions"]:
                    st.markdown(f'<div class="caution-item">⚠ {c}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.info(f"No info found for **{top_label}**. Add it to `FRUIT_INFO` in the source.")
            st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# BACKGROUND  —  botanical SVG art layer
# ─────────────────────────────────────────────
BOTANICAL_BG = """
<svg id="bg-botanical" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice">
  <defs>
    <radialGradient id="glow1" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#9B6B95" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#9B6B95" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow2" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#5A7B5D" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#5A7B5D" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow3" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#C47E6A" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#C47E6A" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Soft glow orbs -->
  <ellipse cx="1340" cy="80"  rx="320" ry="220" fill="url(#glow1)"/>
  <ellipse cx="80"   cy="820" rx="280" ry="200" fill="url(#glow2)"/>
  <ellipse cx="720"  cy="460" rx="200" ry="160" fill="url(#glow3)"/>

  <!-- ── Top-right corner botanical cluster ── -->
  <!-- Large leaf -->
  <g opacity="0.22" transform="translate(1290,10) rotate(25)">
    <path d="M0,0 C20,60 60,110 30,180 C0,110 -20,60 0,0Z" fill="#8BAF8E"/>
    <line x1="0" y1="0" x2="30" y2="180" stroke="#5A7B5D" stroke-width="1" opacity="0.5"/>
    <line x1="0" y1="40"  x2="20"  y2="55"  stroke="#5A7B5D" stroke-width="0.7" opacity="0.4"/>
    <line x1="5" y1="80"  x2="25"  y2="100" stroke="#5A7B5D" stroke-width="0.7" opacity="0.4"/>
    <line x1="8" y1="120" x2="26"  y2="140" stroke="#5A7B5D" stroke-width="0.7" opacity="0.4"/>
  </g>
  <!-- Medium leaf -->
  <g opacity="0.17" transform="translate(1370,60) rotate(-15)">
    <path d="M0,0 C15,45 45,85 22,140 C0,85 -15,45 0,0Z" fill="#C9A8C0"/>
    <line x1="0" y1="0" x2="22" y2="140" stroke="#9B6B95" stroke-width="0.8" opacity="0.4"/>
  </g>
  <!-- Thin wispy stem -->
  <g opacity="0.15" transform="translate(1310,0)">
    <path d="M0,0 C-10,40 10,80 -5,130" stroke="#C4AD99" stroke-width="1.2" fill="none"/>
    <circle cx="-5" cy="130" r="3" fill="#C4AD99"/>
    <circle cx="2"  cy="95"  r="2" fill="#C4AD99"/>
    <circle cx="-8" cy="60"  r="2" fill="#C4AD99"/>
  </g>
  <!-- Small accent leaves -->
  <g opacity="0.13" transform="translate(1410,20) rotate(40)">
    <path d="M0,0 C8,25 25,45 12,75 C0,45 -8,25 0,0Z" fill="#8BAF8E"/>
  </g>
  <g opacity="0.12" transform="translate(1430,110) rotate(-30)">
    <path d="M0,0 C6,18 18,35 9,58 C0,35 -6,18 0,0Z" fill="#C9A8C0"/>
  </g>

  <!-- ── Bottom-left corner cluster ── -->
  <g opacity="0.20" transform="translate(20,750) rotate(-20)">
    <path d="M0,0 C18,55 55,100 28,165 C0,100 -18,55 0,0Z" fill="#8BAF8E"/>
    <line x1="0" y1="0" x2="28" y2="165" stroke="#5A7B5D" stroke-width="1" opacity="0.45"/>
    <line x1="0" y1="50"  x2="18"  y2="65"  stroke="#5A7B5D" stroke-width="0.7" opacity="0.35"/>
    <line x1="4" y1="100" x2="22"  y2="118" stroke="#5A7B5D" stroke-width="0.7" opacity="0.35"/>
  </g>
  <g opacity="0.15" transform="translate(-10,820) rotate(10)">
    <path d="M0,0 C12,40 38,75 19,125 C0,75 -12,40 0,0Z" fill="#9B6B95"/>
    <line x1="0" y1="0" x2="19" y2="125" stroke="#7A5077" stroke-width="0.8" opacity="0.4"/>
  </g>
  <!-- Berry stem bottom left -->
  <g opacity="0.16" transform="translate(100,800)">
    <path d="M0,0 C8,-30 -5,-65 12,-95" stroke="#C4AD99" stroke-width="1.1" fill="none"/>
    <circle cx="12" cy="-95" r="4"  fill="#C47E6A" opacity="0.7"/>
    <circle cx="2"  cy="-65" r="3"  fill="#C47E6A" opacity="0.55"/>
    <circle cx="-2" cy="-35" r="2.5" fill="#C9A8C0" opacity="0.6"/>
  </g>
  <g opacity="0.12" transform="translate(55,870) rotate(-35)">
    <path d="M0,0 C6,20 20,38 10,62 C0,38 -6,20 0,0Z" fill="#C9A8C0"/>
  </g>

  <!-- ── Top-left scattered petals ── -->
  <g opacity="0.10" transform="translate(80,60) rotate(15)">
    <ellipse cx="0" cy="0" rx="6" ry="18" fill="#C9A8C0"/>
  </g>
  <g opacity="0.09" transform="translate(55,90) rotate(-20)">
    <ellipse cx="0" cy="0" rx="5" ry="14" fill="#8BAF8E"/>
  </g>
  <g opacity="0.08" transform="translate(110,45) rotate(40)">
    <ellipse cx="0" cy="0" rx="4" ry="12" fill="#C47E6A"/>
  </g>

  <!-- ── Bottom-right scattered ── -->
  <g opacity="0.09" transform="translate(1360,820) rotate(-25)">
    <ellipse cx="0" cy="0" rx="5" ry="16" fill="#8BAF8E"/>
  </g>
  <g opacity="0.08" transform="translate(1400,870) rotate(30)">
    <ellipse cx="0" cy="0" rx="4" ry="13" fill="#C9A8C0"/>
  </g>

  <!-- ── Floating fine dots / spores ── -->
  <g opacity="0.18" fill="#C9A8C0">
    <circle cx="200"  cy="150" r="1.5"/>
    <circle cx="340"  cy="80"  r="1"/>
    <circle cx="480"  cy="200" r="1.5"/>
    <circle cx="620"  cy="60"  r="1"/>
    <circle cx="800"  cy="170" r="1.5"/>
    <circle cx="950"  cy="90"  r="1"/>
    <circle cx="1100" cy="140" r="1.5"/>
    <circle cx="1220" cy="200" r="1"/>
  </g>
  <g opacity="0.13" fill="#8BAF8E">
    <circle cx="150"  cy="700" r="1.5"/>
    <circle cx="310"  cy="780" r="1"/>
    <circle cx="500"  cy="830" r="1.5"/>
    <circle cx="700"  cy="750" r="1"/>
    <circle cx="900"  cy="820" r="1.5"/>
    <circle cx="1080" cy="760" r="1"/>
    <circle cx="1250" cy="840" r="1.5"/>
  </g>

  <!-- ── Delicate geometric rings (mid-screen accent) ── -->
  <circle cx="1380" cy="450" r="60"  fill="none" stroke="#9B6B95" stroke-width="0.5" opacity="0.12"/>
  <circle cx="1380" cy="450" r="90"  fill="none" stroke="#9B6B95" stroke-width="0.4" opacity="0.07"/>
  <circle cx="60"   cy="400" r="50"  fill="none" stroke="#5A7B5D" stroke-width="0.5" opacity="0.11"/>
  <circle cx="60"   cy="400" r="75"  fill="none" stroke="#5A7B5D" stroke-width="0.4" opacity="0.07"/>

  <!-- ── Thin arc lines (top decorative) ── -->
  <path d="M1200,0 Q1320,80 1440,40"   fill="none" stroke="#C9A8C0" stroke-width="0.6" opacity="0.12"/>
  <path d="M1150,0 Q1300,100 1440,80"  fill="none" stroke="#8BAF8E" stroke-width="0.5" opacity="0.09"/>
  <path d="M0,860 Q120,780 240,900"    fill="none" stroke="#C9A8C0" stroke-width="0.6" opacity="0.11"/>
  <path d="M0,900 Q160,820 300,900"    fill="none" stroke="#8BAF8E" stroke-width="0.5" opacity="0.08"/>
</svg>
"""

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    # Inject botanical background SVG
    st.markdown(BOTANICAL_BG, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">
        <div class="hero-badge">✦ &nbsp; AI-Powered Fruit Scanner &nbsp; ✦</div>
        <h1>Meet <span>Fruitly</span></h1>
        <p>Snap or upload a fruit — get instant AI identification &amp; nutrition insights.</p>
    </div>
    <hr class="divider">
    """, unsafe_allow_html=True)

    with st.spinner("Initialising model..."):
        model, labels, errors = load_model()

    if errors:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.error("Could not initialise the scanner:")
        for e in errors:
            st.markdown(f"- {e}")
        st.markdown("""
        **Setup:**
        1. Place `keras_model.h5` and `labels.txt` in the same folder as this script.
        2. Run `streamlit run fruit_scanner_app.py`
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    for key in ("result_img", "results"):
        if key not in st.session_state:
            st.session_state[key] = None

    tab_cam, tab_upload = st.tabs(["  📷  Camera  ", "  🖼️  Upload  "])

    with tab_cam:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title"><span class="dot"></span>Capture a Fruit</div>', unsafe_allow_html=True)
        cam_img = st.camera_input("Point your camera at a fruit and take a photo")
        if cam_img:
            img = Image.open(cam_img)
            with st.spinner("Analysing..."):
                results = predict(model, labels, img)
            st.session_state.result_img = img
            st.session_state.results    = results
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_upload:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title"><span class="dot"></span>Upload an Image</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Choose a JPG or PNG file", type=["jpg", "jpeg", "png"])
        if uploaded:
            img = Image.open(uploaded)
            st.image(img, caption="Preview", width=300)
            if st.button("Identify Fruit"):
                with st.spinner("Analysing..."):
                    results = predict(model, labels, img)
                st.session_state.result_img = img
                st.session_state.results    = results
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.results:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center;margin-bottom:1.4rem">
            <span style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;color:#EDE0E8;letter-spacing:.01em">
                Detection Results
            </span>
        </div>
        """, unsafe_allow_html=True)
        render_results(st.session_state.results)

        st.markdown('<div class="reset-btn" style="text-align:center;margin-top:1rem">', unsafe_allow_html=True)
        if st.button("✕  Clear Results"):
            st.session_state.result_img = None
            st.session_state.results    = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <hr class="divider" style="margin-top:3.5rem">
    <p style="text-align:center;color:#5E5062;font-size:.75rem;margin-top:1rem;letter-spacing:.04em">
        FRUITLY &nbsp;·&nbsp; Powered by Teachable Machine &amp; TensorFlow &nbsp;·&nbsp; Made with ♡
    </p>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
