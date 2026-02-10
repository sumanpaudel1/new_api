"""
SportMonks Football News API Explorer — Streamlit Frontend v3
Real data only — No demo mode. Designed for supervisor presentation.
All 5 SportMonks News endpoints with beautiful formatted output.
"""

import streamlit as st
import requests
import json
import os
from datetime import datetime

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="SportMonks News Explorer",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# CUSTOM CSS — Professional dark theme
# ──────────────────────────────────────────────

st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(160deg, #0a0a1a 0%, #1a1a3e 40%, #0d0d2b 100%);
    }

    /* Header styles */
    .hero-title {
        background: linear-gradient(90deg, #00d2ff, #3a7bd5, #00d2ff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 900;
        text-align: center;
        padding: 0.5rem 0 0.2rem;
        letter-spacing: -0.5px;
        animation: shimmer 3s linear infinite;
    }
    @keyframes shimmer {
        to { background-position: 200% center; }
    }
    .hero-sub {
        color: #8892b0;
        text-align: center;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }

    /* Live badge pulse */
    .live-dot {
        display: inline-block;
        width: 10px; height: 10px;
        background: #48bb78;
        border-radius: 50%;
        margin-right: 6px;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.3); }
    }

    /* News article card */
    .article-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.8rem;
        margin-bottom: 1.2rem;
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
    }
    .article-card:hover {
        border-color: rgba(0,210,255,0.3);
        box-shadow: 0 8px 32px rgba(0,210,255,0.08);
        transform: translateY(-1px);
    }

    /* Article title */
    .article-title {
        color: #e6f1ff;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.6rem;
        line-height: 1.4;
    }

    /* Meta info bar */
    .article-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 1rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .meta-chip {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 8px;
        padding: 4px 12px;
        font-size: 0.8rem;
        color: #8892b0;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }

    /* Article body paragraph */
    .article-paragraph {
        background: rgba(255,255,255,0.02);
        border-left: 3px solid #3a7bd5;
        padding: 0.9rem 1.2rem;
        margin-bottom: 0.6rem;
        border-radius: 0 10px 10px 0;
        color: #ccd6f6;
        font-size: 0.95rem;
        line-height: 1.75;
    }
    .article-paragraph:hover {
        background: rgba(255,255,255,0.04);
        border-left-color: #00d2ff;
    }

    /* Player mention tag */
    .player-tag {
        background: rgba(100,255,218,0.1);
        color: #64ffda;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 8px;
    }

    /* Stats box */
    .stat-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 1.4rem;
        text-align: center;
    }
    .stat-value {
        color: #00d2ff;
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.2;
    }
    .stat-label {
        color: #8892b0;
        font-size: 0.82rem;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Badges */
    .badge-pre {
        background: linear-gradient(135deg, #f6ad55, #ed8936);
        color: white; padding: 3px 14px; border-radius: 20px;
        font-size: 0.75rem; font-weight: 700; letter-spacing: 0.3px;
    }
    .badge-post {
        background: linear-gradient(135deg, #68d391, #38a169);
        color: white; padding: 3px 14px; border-radius: 20px;
        font-size: 0.75rem; font-weight: 700; letter-spacing: 0.3px;
    }
    .badge-live {
        background: linear-gradient(135deg, #fc8181, #e53e3e);
        color: white; padding: 3px 14px; border-radius: 20px;
        font-size: 0.75rem; font-weight: 700;
    }
    .badge-endpoint {
        background: rgba(0,210,255,0.12);
        border: 1px solid rgba(0,210,255,0.3);
        color: #00d2ff; padding: 3px 14px; border-radius: 20px;
        font-size: 0.75rem; font-weight: 600;
    }

    /* Endpoint info card */
    .endpoint-info {
        background: rgba(0,210,255,0.04);
        border: 1px solid rgba(0,210,255,0.15);
        border-radius: 12px;
        padding: 1rem 1.4rem;
        margin-bottom: 1rem;
    }
    .endpoint-method {
        background: #48bb78; color: white; padding: 3px 10px;
        border-radius: 6px; font-weight: 800; font-size: 0.78rem;
        display: inline-block; margin-right: 10px; letter-spacing: 0.5px;
    }
    .endpoint-url {
        color: #fbd38d; font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
        font-size: 0.85rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(10,10,26,0.97);
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Divider */
    .divider { border-top: 1px solid rgba(255,255,255,0.06); margin: 1.5rem 0; }

    /* Rate limit info */
    .rate-info {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        color: #8892b0;
        font-size: 0.82rem;
    }

    /* No data state */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        color: #8892b0;
    }
    .empty-state-icon { font-size: 3rem; margin-bottom: 1rem; }
    .empty-state-text { font-size: 1.1rem; }

    /* Welcome card */
    .welcome-card {
        background: linear-gradient(145deg, rgba(0,210,255,0.05), rgba(58,123,213,0.03));
        border: 1px solid rgba(0,210,255,0.15);
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────

BACKEND = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")

ENDPOINTS = {
    "pre_match": {
        "name": "Pre-Match News",
        "icon": "🔮",
        "badge": "badge-pre",
        "desc": "All available pre-match news articles. Expert-written, available 48+ hours before kick-off.",
        "api_url": "https://api.sportmonks.com/v3/football/news/pre-match",
        "local_path": "/api/news/pre-match",
        "needs_season": False,
    },
    "pre_match_season": {
        "name": "Pre-Match News by Season",
        "icon": "📅",
        "badge": "badge-pre",
        "desc": "Pre-match news filtered by a specific season ID.",
        "api_url": "https://api.sportmonks.com/v3/football/news/pre-match/seasons/{SEASON_ID}",
        "local_path": "/api/news/pre-match/seasons/{season_id}",
        "needs_season": True,
    },
    "pre_match_upcoming": {
        "name": "Pre-Match News (Upcoming)",
        "icon": "⏳",
        "badge": "badge-pre",
        "desc": "Pre-match news for upcoming fixtures only.",
        "api_url": "https://api.sportmonks.com/v3/football/news/pre-match/upcoming",
        "local_path": "/api/news/pre-match/upcoming",
        "needs_season": False,
    },
    "post_match": {
        "name": "Post-Match News",
        "icon": "✅",
        "badge": "badge-post",
        "desc": "AI-generated post-match articles, available immediately after the final whistle.",
        "api_url": "https://api.sportmonks.com/v3/football/news/post-match",
        "local_path": "/api/news/post-match",
        "needs_season": False,
    },
    "post_match_season": {
        "name": "Post-Match News by Season",
        "icon": "🏆",
        "badge": "badge-post",
        "desc": "Post-match news filtered by a specific season ID.",
        "api_url": "https://api.sportmonks.com/v3/football/news/post-match/seasons/{SEASON_ID}",
        "local_path": "/api/news/post-match/seasons/{season_id}",
        "needs_season": True,
    },
}


# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────

def backend_alive():
    try:
        return requests.get(f"{BACKEND}/", timeout=5).status_code == 200
    except Exception:
        return False


def call(endpoint: str, params: dict = None) -> dict:
    try:
        resp = requests.get(f"{BACKEND}{endpoint}", params=params, timeout=30)
        return resp.json()
    except requests.exceptions.ConnectionError:
        return {"error": True, "message": "Backend not running. Please start the FastAPI server first."}
    except Exception as e:
        return {"error": True, "message": str(e)}


def format_datetime(dt_str: str) -> str:
    """Human-friendly date formatting."""
    if not dt_str:
        return "N/A"
    try:
        dt = datetime.strptime(dt_str[:19], "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%b %d, %Y at %I:%M %p")
    except Exception:
        return dt_str[:16] if len(dt_str) >= 16 else dt_str


def render_article(article: dict, index: int):
    """Render a single news article as a rich card."""
    title = article.get("title", "Untitled Article")
    news_type = article.get("type", "news")
    created = article.get("created_at", "")
    updated = article.get("updated_at", "")
    fixture_id = article.get("fixture_id", "")
    article_id = article.get("id", "")
    lines = article.get("lines", [])

    # League info
    league = article.get("league", {}) or {}
    league_name = league.get("name", "") if isinstance(league, dict) else ""
    league_img = league.get("image_path", "") if isinstance(league, dict) else ""

    # Fixture info
    fixture = article.get("fixture", {}) or {}
    match_name = fixture.get("name", "") if isinstance(fixture, dict) else ""
    kick_off = fixture.get("starting_at", "") if isinstance(fixture, dict) else ""

    # Badge
    is_pre = "pre" in str(news_type).lower()
    badge_class = "badge-pre" if is_pre else "badge-post"
    badge_label = "PRE-MATCH" if is_pre else "POST-MATCH"

    # League image
    league_html = ""
    if league_img:
        league_html = f"<img src='{league_img}' width='20' style='vertical-align:middle;margin-right:4px;border-radius:3px;'>"

    # Meta chips
    meta_chips = []
    if match_name:
        meta_chips.append(f'<span class="meta-chip">⚽ {match_name}</span>')
    if league_name:
        meta_chips.append(f'<span class="meta-chip">{league_html}🏆 {league_name}</span>')
    if kick_off:
        meta_chips.append(f'<span class="meta-chip">🕐 {format_datetime(kick_off)}</span>')
    if article_id:
        meta_chips.append(f'<span class="meta-chip">🆔 {article_id}</span>')
    if created:
        meta_chips.append(f'<span class="meta-chip">📝 {format_datetime(created)}</span>')
    meta_html = "\n".join(meta_chips)

    st.markdown(f"""
    <div class="article-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.5rem;">
            <div class="article-title">{index}. {title}</div>
            <span class="{badge_class}">{badge_label}</span>
        </div>
        <div class="article-meta">
            {meta_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Article body (lines)
    if lines:
        with st.expander(f"📖 Read Full Article — {len(lines)} paragraph{'s' if len(lines) != 1 else ''}", expanded=True):
            for line in lines:
                if isinstance(line, dict):
                    text = line.get("line", line.get("text", str(line)))
                    player_id = line.get("player_id")
                    player_html = f'<span class="player-tag">Player #{player_id}</span>' if player_id else ""
                    st.markdown(f'<div class="article-paragraph">{text}{player_html}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="article-paragraph">{line}</div>', unsafe_allow_html=True)
    else:
        st.caption("No article body (lines) returned for this article.")


def render_results(data: dict, endpoint_key: str):
    """Full results renderer with stats, articles, and raw JSON."""
    if not data:
        st.warning("No response received from the API.")
        return

    if data.get("error"):
        st.error(f"API Error: {data.get('message', 'Unknown error')}")
        if data.get("status_code") == 403:
            st.info("This endpoint requires a Pro plan subscription on SportMonks.")
        return

    articles = data.get("data", [])
    pagination = data.get("pagination", {}) or {}
    rate_limit = data.get("rate_limit", {}) or {}
    subscription = data.get("subscription", [])

    # ─── Stats row ────────────────────────────
    total_articles = len(articles) if isinstance(articles, list) else 0
    total_paragraphs = 0
    if isinstance(articles, list):
        for a in articles:
            total_paragraphs += len(a.get("lines", []))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{total_articles}</div><div class="stat-label">Articles Fetched</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{total_paragraphs}</div><div class="stat-label">Total Paragraphs</div></div>', unsafe_allow_html=True)
    with c3:
        cp = pagination.get("current_page", 1)
        st.markdown(f'<div class="stat-card"><div class="stat-value">{cp}</div><div class="stat-label">Current Page</div></div>', unsafe_allow_html=True)
    with c4:
        has_more = pagination.get("has_more", False)
        st.markdown(f'<div class="stat-card"><div class="stat-value">{"Yes" if has_more else "No"}</div><div class="stat-label">More Pages</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ─── Subscription & Rate Limit ────────────
    col_left, col_right = st.columns(2)
    with col_left:
        if subscription and isinstance(subscription, list) and len(subscription) > 0:
            plans = subscription[0].get("plans", [])
            if plans:
                plan_names = ", ".join([p.get("plan", "N/A") for p in plans])
                st.markdown(f'<div class="rate-info">📋 <strong>Plan:</strong> {plan_names}</div>', unsafe_allow_html=True)
    with col_right:
        if rate_limit:
            remaining = rate_limit.get("remaining", "N/A")
            resets = rate_limit.get("resets_in_seconds", "N/A")
            entity = rate_limit.get("requested_entity", "N/A")
            st.markdown(f'<div class="rate-info">⏱ <strong>Rate Limit:</strong> {remaining} remaining | Resets in {resets}s | Entity: {entity}</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ─── Articles ─────────────────────────────
    if isinstance(articles, list) and articles:
        st.markdown(f"### 📰 News Articles ({total_articles})")
        for i, article in enumerate(articles):
            render_article(article, i + 1)
    elif isinstance(articles, list) and not articles:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📭</div>
            <div class="empty-state-text">No articles returned for this endpoint.<br>
            This may mean there are no current articles matching this filter, or try a different season ID.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.json(articles)

    # ─── Raw JSON ─────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    with st.expander("🔍 View Raw JSON Response", expanded=False):
        st.json(data)


# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────

with st.sidebar:
    st.markdown('<div class="hero-title" style="font-size:1.5rem;">⚽ SportMonks</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#8892b0;font-size:0.85rem;margin-bottom:1.5rem;">Football News API Explorer</p>', unsafe_allow_html=True)

    # Connection status
    alive = backend_alive()
    if alive:
        st.markdown('<div style="text-align:center;"><span class="live-dot"></span> <span style="color:#48bb78;font-weight:600;">Backend Connected</span></div>', unsafe_allow_html=True)
    else:
        st.error("Backend Not Running")
        st.code("python run.py", language="bash")

    st.markdown("---")

    # Live mode indicator
    st.markdown("""
    <div style="background:rgba(72,187,120,0.08);border:1px solid rgba(72,187,120,0.25);border-radius:10px;padding:0.8rem 1rem;margin-bottom:1rem;">
        <span class="live-dot"></span>
        <span style="color:#48bb78;font-weight:700;font-size:0.9rem;">LIVE MODE</span>
        <span style="color:#8892b0;font-size:0.8rem;display:block;margin-top:4px;">Fetching real data from SportMonks Pro API</span>
    </div>
    """, unsafe_allow_html=True)

    # Endpoint selector
    st.markdown("### 🎯 Select Endpoint")
    ep_choice = st.selectbox(
        "Endpoint",
        list(ENDPOINTS.keys()),
        format_func=lambda x: f"{ENDPOINTS[x]['icon']} {ENDPOINTS[x]['name']}",
        label_visibility="collapsed",
    )

    ep_info = ENDPOINTS[ep_choice]
    st.markdown(f'<p style="color:#8892b0;font-size:0.82rem;margin-top:-8px;">{ep_info["desc"]}</p>', unsafe_allow_html=True)

    st.markdown("---")

    # Parameters
    st.markdown("### ⚙️ Parameters")

    season_id = None
    if ep_info["needs_season"]:
        season_id = st.number_input("Season ID", min_value=1, value=23614, step=1,
                                     help="SportMonks Season ID (e.g., 23614 for EPL 2024/25)")

    include = st.text_input("Includes", value="fixture;league;lines",
                            help="Related data to include: fixture, league, lines")
    order = st.selectbox("Sort Order", ["desc", "asc"], help="Newest first (desc) or oldest first (asc)")
    per_page = st.slider("Articles Per Page", 1, 50, 25, help="Number of articles per request")
    page = st.number_input("Page", min_value=1, value=1, help="Pagination page number")

    st.markdown("---")

    # Fetch button
    fetch_btn = st.button("🚀 Fetch News", use_container_width=True, type="primary")

    # Fetch ALL pages button
    fetch_all_btn = st.button("📥 Fetch ALL Pages", use_container_width=True,
                               help="Fetches every page of results to show total coverage")

    st.markdown("---")
    st.markdown(f"""
    <div style="color:#4a5568;font-size:0.72rem;text-align:center;">
        API: SportMonks v3 Football<br>
        Plan: Pro (News endpoints)<br>
        <a href="https://docs.sportmonks.com/football/endpoints-and-entities/endpoints/news" target="_blank" style="color:#3a7bd5;">Documentation ↗</a>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# MAIN CONTENT
# ──────────────────────────────────────────────

st.markdown('<div class="hero-title">⚽ SportMonks Football News</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub"><span class="live-dot"></span> Real-time data from SportMonks Pro API — All 5 News Endpoints</div>', unsafe_allow_html=True)

# ─── Endpoint overview ────────────────────────
st.markdown("---")

with st.expander("📋 Available News API Endpoints (5 endpoints)", expanded=False):
    for key, ep in ENDPOINTS.items():
        st.markdown(f"""
        <div class="endpoint-info">
            <span class="endpoint-method">GET</span>
            <span class="{ep['badge']}">{ep['name']}</span>
            <div class="endpoint-url" style="margin-top:6px;">{ep['api_url']}</div>
            <div style="color:#8892b0;font-size:0.82rem;margin-top:4px;">{ep['desc']}</div>
            <div style="color:#4a5568;font-size:0.75rem;margin-top:4px;">Includes: fixture, league, lines | Pagination: supported</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")


# ──────────────────────────────────────────────
# FETCH & DISPLAY
# ──────────────────────────────────────────────

def do_fetch(p: int = 1, pp: int = 25) -> dict:
    """Execute fetch for the selected endpoint."""
    params = {"include": include, "order": order, "per_page": pp, "page": p}
    if ep_choice == "pre_match":
        return call("/api/news/pre-match", params)
    elif ep_choice == "pre_match_season":
        return call(f"/api/news/pre-match/seasons/{season_id}", params)
    elif ep_choice == "pre_match_upcoming":
        return call("/api/news/pre-match/upcoming", params)
    elif ep_choice == "post_match":
        return call("/api/news/post-match", params)
    elif ep_choice == "post_match_season":
        return call(f"/api/news/post-match/seasons/{season_id}", params)
    return {"error": True, "message": "Unknown endpoint"}


if fetch_btn:
    sel = ENDPOINTS[ep_choice]
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:0.5rem;">
        <span style="font-size:1.8rem;">{sel['icon']}</span>
        <span style="color:#e6f1ff;font-size:1.5rem;font-weight:700;">{sel['name']}</span>
        <span class="badge-live">LIVE</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="endpoint-info">
        <span class="endpoint-method">GET</span>
        <span class="endpoint-url">{sel['api_url']}</span>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Fetching live data from SportMonks API..."):
        data = do_fetch(page, per_page)

    render_results(data, ep_choice)


elif fetch_all_btn:
    sel = ENDPOINTS[ep_choice]
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:0.5rem;">
        <span style="font-size:1.8rem;">{sel['icon']}</span>
        <span style="color:#e6f1ff;font-size:1.5rem;font-weight:700;">{sel['name']} — ALL PAGES</span>
        <span class="badge-live">LIVE</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="endpoint-info">
        <span class="endpoint-method">GET</span>
        <span class="endpoint-url">{sel['api_url']}</span>
        <span style="color:#8892b0;font-size:0.8rem;margin-left:12px;">Fetching all pages...</span>
    </div>
    """, unsafe_allow_html=True)

    all_articles = []
    current_page = 1
    has_more = True
    progress_bar = st.progress(0, text="Fetching page 1...")

    while has_more:
        progress_bar.progress(min(current_page * 10, 95), text=f"Fetching page {current_page}...")
        data = do_fetch(current_page, 50)

        if data.get("error"):
            st.error(f"Error on page {current_page}: {data.get('message')}")
            break

        page_articles = data.get("data", [])
        if isinstance(page_articles, list):
            all_articles.extend(page_articles)

        pagination = data.get("pagination", {}) or {}
        has_more = pagination.get("has_more", False)
        current_page += 1

        if current_page > 50:  # Safety limit
            st.warning("Stopped at 50 pages (safety limit).")
            break

    progress_bar.progress(100, text="Done!")

    # Show combined results
    total = len(all_articles)
    total_paragraphs = sum(len(a.get("lines", [])) for a in all_articles)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{total}</div><div class="stat-label">Total Articles</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{total_paragraphs}</div><div class="stat-label">Total Paragraphs</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{current_page - 1}</div><div class="stat-label">Pages Fetched</div></div>', unsafe_allow_html=True)
    with c4:
        leagues_seen = set()
        for a in all_articles:
            lg = a.get("league", {})
            if isinstance(lg, dict) and lg.get("name"):
                leagues_seen.add(lg["name"])
        st.markdown(f'<div class="stat-card"><div class="stat-value">{len(leagues_seen)}</div><div class="stat-label">Leagues Covered</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # League breakdown
    if leagues_seen:
        st.markdown("### 🏆 Leagues Covered")
        league_cols = st.columns(min(len(leagues_seen), 4))
        for i, lg_name in enumerate(sorted(leagues_seen)):
            count = sum(1 for a in all_articles if isinstance(a.get("league", {}), dict) and a.get("league", {}).get("name") == lg_name)
            with league_cols[i % len(league_cols)]:
                st.markdown(f'<div class="stat-card" style="margin-bottom:0.5rem;"><div class="stat-value" style="font-size:1.3rem;">{count}</div><div class="stat-label">{lg_name}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if all_articles:
        st.markdown(f"### 📰 All News Articles ({total})")
        for i, article in enumerate(all_articles):
            render_article(article, i + 1)

    # Raw JSON for all
    with st.expander("🔍 View All Raw JSON Data", expanded=False):
        st.json({"total_articles": total, "pages_fetched": current_page - 1, "data": all_articles})


else:
    # ─── Welcome state ────────────────────────
    st.markdown("""
    <div class="welcome-card">
        <div style="font-size:3.5rem;margin-bottom:1rem;">📰</div>
        <div style="color:#e6f1ff;font-size:1.4rem;font-weight:700;margin-bottom:0.8rem;">
            Select an Endpoint & Click "Fetch News"
        </div>
        <div style="color:#8892b0;font-size:1rem;line-height:1.6;max-width:600px;margin:0 auto;">
            This tool fetches <strong>real football news</strong> from the SportMonks Pro API.<br>
            Choose any of the 5 news endpoints from the sidebar to see live data.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # Feature cards
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="article-card" style="text-align:center;">
            <div style="font-size:2.5rem;margin-bottom:0.8rem;">🔮</div>
            <div class="article-title" style="text-align:center;font-size:1.1rem;">Pre-Match News</div>
            <div style="color:#8892b0;font-size:0.85rem;line-height:1.5;">
                Expert-written preview articles published 48+ hours before kick-off.
                Covers UCL, EPL, La Liga, Bundesliga, Serie A, Ligue 1.
            </div>
            <div style="margin-top:0.8rem;"><span class="badge-pre">3 ENDPOINTS</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="article-card" style="text-align:center;">
            <div style="font-size:2.5rem;margin-bottom:0.8rem;">✅</div>
            <div class="article-title" style="text-align:center;font-size:1.1rem;">Post-Match News</div>
            <div style="color:#8892b0;font-size:0.85rem;line-height:1.5;">
                AI-generated match reports available immediately after the final whistle.
                Full analysis with player stats.
            </div>
            <div style="margin-top:0.8rem;"><span class="badge-post">2 ENDPOINTS</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="article-card" style="text-align:center;">
            <div style="font-size:2.5rem;margin-bottom:0.8rem;">📥</div>
            <div class="article-title" style="text-align:center;font-size:1.1rem;">Fetch ALL Pages</div>
            <div style="color:#8892b0;font-size:0.85rem;line-height:1.5;">
                Use "Fetch ALL Pages" to download every article available.
                See total coverage, league breakdown, and full content.
            </div>
            <div style="margin-top:0.8rem;"><span class="badge-endpoint">FULL COVERAGE</span></div>
        </div>
        """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────

st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#4a5568;font-size:0.78rem;padding:1rem 0;">
    SportMonks News API Explorer v3 &nbsp;•&nbsp; FastAPI + Streamlit &nbsp;•&nbsp; Real Data Only &nbsp;•&nbsp;
    <a href="https://docs.sportmonks.com/football/endpoints-and-entities/endpoints/news" target="_blank" style="color:#3a7bd5;">API Documentation ↗</a>
</div>
""", unsafe_allow_html=True)
