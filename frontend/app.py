"""
SportMonks Football News API Explorer — Streamlit Frontend v4
Simplified UI for non-technical users with English football focus.
Auto-loads latest news. Parameters hidden by default.
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
    page_title="Football News Explorer",
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

    /* Match Banner with Team Logos */
    .match-banner {
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, rgba(10,10,40,0.95) 0%, rgba(20,20,60,0.8) 50%, rgba(10,10,40,0.95) 100%);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 1.5rem 1rem;
        margin-bottom: 1.2rem;
        gap: 1rem;
        position: relative;
        overflow: hidden;
    }
    .match-banner::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(ellipse at center, rgba(0,210,255,0.06) 0%, transparent 70%);
        pointer-events: none;
    }
    .team-side {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        flex: 1;
        z-index: 1;
    }
    .team-logo {
        width: 68px;
        height: 68px;
        object-fit: contain;
        filter: drop-shadow(0 4px 12px rgba(0,0,0,0.4));
        transition: transform 0.3s ease;
    }
    .team-logo:hover {
        transform: scale(1.12);
    }
    .team-logo-placeholder {
        width: 68px;
        height: 68px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        background: rgba(255,255,255,0.05);
        border-radius: 50%;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .team-name-label {
        color: #ccd6f6;
        font-size: 0.82rem;
        font-weight: 700;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        max-width: 120px;
        line-height: 1.3;
    }
    .vs-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.4rem;
        z-index: 1;
        min-width: 60px;
    }
    .vs-badge {
        background: linear-gradient(135deg, #00d2ff, #3a7bd5);
        color: white;
        font-weight: 900;
        font-size: 0.9rem;
        padding: 5px 14px;
        border-radius: 10px;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(0,210,255,0.25);
    }
    .league-badge-img {
        width: 32px;
        height: 32px;
        object-fit: contain;
        filter: drop-shadow(0 2px 6px rgba(0,0,0,0.3));
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

    /* League filter section */
    .league-section {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.8rem;
    }
    .league-section-title {
        color: #e6f1ff;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 0.5rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }

    /* Auto-load info */
    .filter-info {
        background: rgba(72,187,120,0.06);
        border: 1px solid rgba(72,187,120,0.15);
        border-radius: 12px;
        padding: 1rem 1.4rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    .filter-info span {
        color: #48bb78;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────

BACKEND = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")

# English football leagues & competitions for quick filters
ENGLISH_LEAGUES = {
    "Premier League": {"icon": "🏆", "keywords": ["premier league"]},
    "Championship": {"icon": "🥈", "keywords": ["championship"]},
    "League One": {"icon": "🥉", "keywords": ["league one"]},
    "League Two": {"icon": "4️⃣", "keywords": ["league two"]},
}

DOMESTIC_CUPS = {
    "FA Cup": {"icon": "🏅", "keywords": ["fa cup"]},
    "Carabao Cup": {"icon": "🍵", "keywords": ["carabao", "efl cup", "league cup"]},
}

EUROPEAN_COMPETITIONS = {
    "Champions League": {"icon": "⭐", "keywords": ["champions league", "ucl"]},
    "Europa League": {"icon": "🌍", "keywords": ["europa league"]},
    "Conference League": {"icon": "🌐", "keywords": ["conference league"]},
}

# Simple news type options for the user
NEWS_TYPES = {
    "latest": {"name": "📰 Latest News", "desc": "Most recent pre-match & post-match combined"},
    "upcoming": {"name": "🔮 Upcoming Matches", "desc": "Pre-match previews for upcoming fixtures"},
    "post_match": {"name": "✅ Match Results", "desc": "Post-match reports & analysis"},
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


def match_league_filter(league_name: str, selected_filters: list) -> bool:
    """Check if a league name matches any of the selected filter keywords."""
    if not selected_filters:
        return True  # No filter = show all
    if not league_name:
        return False

    league_lower = league_name.lower()

    all_filters = {}
    all_filters.update(ENGLISH_LEAGUES)
    all_filters.update(DOMESTIC_CUPS)
    all_filters.update(EUROPEAN_COMPETITIONS)

    for filter_name in selected_filters:
        if filter_name in all_filters:
            for keyword in all_filters[filter_name]["keywords"]:
                if keyword in league_lower:
                    return True
    return False


def filter_articles_by_league(articles: list, selected_filters: list) -> list:
    """Filter articles by selected league/competition filters."""
    if not selected_filters:
        return articles
    filtered = []
    for article in articles:
        league = article.get("league", {}) or {}
        league_name = league.get("name", "") if isinstance(league, dict) else ""
        if match_league_filter(league_name, selected_filters):
            filtered.append(article)
    return filtered


def render_article(article: dict, index: int):
    """Render a single news article as a rich card with team images."""
    title = article.get("title", "Untitled Article")
    news_type = article.get("type", "news")
    created = article.get("created_at", "")
    lines = article.get("lines", [])

    # League info
    league = article.get("league", {}) or {}
    league_name = league.get("name", "") if isinstance(league, dict) else ""
    league_img = league.get("image_path", "") if isinstance(league, dict) else ""

    # Fixture info
    fixture = article.get("fixture", {}) or {}
    match_name = fixture.get("name", "") if isinstance(fixture, dict) else ""
    kick_off = fixture.get("starting_at", "") if isinstance(fixture, dict) else ""

    # Participants (teams) with images
    participants = fixture.get("participants", []) if isinstance(fixture, dict) else []
    home_team = None
    away_team = None
    for p in participants:
        if isinstance(p, dict):
            meta = p.get("meta", {}) or {}
            location = meta.get("location", "")
            if location == "home":
                home_team = p
            elif location == "away":
                away_team = p
    # Fallback: use first two participants if no home/away distinction
    if not home_team and not away_team and len(participants) >= 2:
        home_team = participants[0]
        away_team = participants[1]
    elif not home_team and not away_team and len(participants) == 1:
        home_team = participants[0]

    # Build match banner HTML with team logos
    banner_html = ""
    if home_team or away_team:
        home_img = home_team.get("image_path", "") if home_team else ""
        home_name = home_team.get("name", "Home") if home_team else ""
        away_img = away_team.get("image_path", "") if away_team else ""
        away_name = away_team.get("name", "Away") if away_team else ""
        league_badge = f"<img src='{league_img}' class='league-badge-img'>" if league_img else ""

        home_logo_html = f'<img src="{home_img}" class="team-logo" alt="{home_name}">' if home_img else '<div class="team-logo-placeholder">🏠</div>'
        away_logo_html = f'<img src="{away_img}" class="team-logo" alt="{away_name}">' if away_img else '<div class="team-logo-placeholder">✈️</div>'

        banner_html = f"""
        <div class="match-banner">
            <div class="team-side">
                {home_logo_html}
                <div class="team-name-label">{home_name}</div>
            </div>
            <div class="vs-section">
                {league_badge}
                <div class="vs-badge">VS</div>
            </div>
            <div class="team-side">
                {away_logo_html}
                <div class="team-name-label">{away_name}</div>
            </div>
        </div>
        """

    # Badge
    is_pre = "pre" in str(news_type).lower()
    badge_class = "badge-pre" if is_pre else "badge-post"
    badge_label = "PRE-MATCH" if is_pre else "POST-MATCH"

    # League image for meta chip
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
    if created:
        meta_chips.append(f'<span class="meta-chip">📝 {format_datetime(created)}</span>')
    meta_html = "\n".join(meta_chips)

    st.markdown(f"""
    <div class="article-card">
        {banner_html}
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
        with st.expander(f"📖 Read Full Article — {len(lines)} paragraph{'s' if len(lines) != 1 else ''}", expanded=False):
            for line in lines:
                if isinstance(line, dict):
                    text = line.get("line", line.get("text", str(line)))
                    player_id = line.get("player_id")
                    player_html = f'<span class="player-tag">Player #{player_id}</span>' if player_id else ""
                    st.markdown(f'<div class="article-paragraph">{text}{player_html}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="article-paragraph">{line}</div>', unsafe_allow_html=True)


def render_stats_row(articles: list, pagination: dict = None):
    """Show stats cards for the fetched data."""
    total_articles = len(articles)
    total_paragraphs = sum(len(a.get("lines", [])) for a in articles)

    leagues_seen = set()
    for a in articles:
        lg = a.get("league", {})
        if isinstance(lg, dict) and lg.get("name"):
            leagues_seen.add(lg["name"])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{total_articles}</div><div class="stat-label">Articles</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{total_paragraphs}</div><div class="stat-label">Paragraphs</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{len(leagues_seen)}</div><div class="stat-label">Leagues</div></div>', unsafe_allow_html=True)
    with c4:
        if pagination:
            has_more = pagination.get("has_more", False)
            st.markdown(f'<div class="stat-card"><div class="stat-value">{"Yes" if has_more else "No"}</div><div class="stat-label">More Pages</div></div>', unsafe_allow_html=True)
        else:
            pre_count = sum(1 for a in articles if "pre" in str(a.get("type", "")).lower())
            post_count = total_articles - pre_count
            label = f"{pre_count}P / {post_count}R"
            st.markdown(f'<div class="stat-card"><div class="stat-value" style="font-size:1.4rem;">{label}</div><div class="stat-label">Preview / Results</div></div>', unsafe_allow_html=True)


def render_league_breakdown(articles: list):
    """Show which leagues are covered."""
    league_counts = {}
    for a in articles:
        lg = a.get("league", {})
        if isinstance(lg, dict) and lg.get("name"):
            name = lg["name"]
            league_counts[name] = league_counts.get(name, 0) + 1

    if league_counts:
        sorted_leagues = sorted(league_counts.items(), key=lambda x: x[1], reverse=True)
        num_cols = min(len(sorted_leagues), 5)
        if num_cols > 0:
            cols = st.columns(num_cols)
            for i, (lg_name, count) in enumerate(sorted_leagues[:10]):
                with cols[i % num_cols]:
                    st.markdown(f'<div class="stat-card" style="margin-bottom:0.5rem;padding:0.8rem;"><div class="stat-value" style="font-size:1.3rem;">{count}</div><div class="stat-label" style="font-size:0.7rem;">{lg_name}</div></div>', unsafe_allow_html=True)


def render_results_section(data: dict, selected_filters: list):
    """Full results renderer with filtering support."""
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

    if not isinstance(articles, list):
        st.json(data)
        return

    # Apply league filter
    filtered_articles = filter_articles_by_league(articles, selected_filters)

    # Filter indicator
    if selected_filters and len(filtered_articles) != len(articles):
        st.markdown(f"""
        <div class="filter-info">
            Showing <span>{len(filtered_articles)}</span> of {len(articles)} articles matching your league filters
        </div>
        """, unsafe_allow_html=True)

    # Stats row
    render_stats_row(filtered_articles, pagination)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # League breakdown
    if filtered_articles:
        render_league_breakdown(filtered_articles)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Subscription & Rate Limit (compact)
    if subscription or rate_limit:
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
                st.markdown(f'<div class="rate-info">⏱ <strong>Rate Limit:</strong> {remaining} remaining</div>', unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Articles
    if filtered_articles:
        st.markdown(f"### 📰 News Articles ({len(filtered_articles)})")
        for i, article in enumerate(filtered_articles):
            render_article(article, i + 1)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📭</div>
            <div class="empty-state-text">No articles match your current filters.<br>
            Try selecting different leagues or removing filters to see all news.</div>
        </div>
        """, unsafe_allow_html=True)

    # Raw JSON
    with st.expander("🔍 View Raw JSON Response", expanded=False):
        st.json(data)


# ──────────────────────────────────────────────
# SESSION STATE INIT
# ──────────────────────────────────────────────

if "news_data" not in st.session_state:
    st.session_state.news_data = None
if "news_type" not in st.session_state:
    st.session_state.news_type = "latest"
if "auto_loaded" not in st.session_state:
    st.session_state.auto_loaded = False


# ──────────────────────────────────────────────
# SIDEBAR — Simplified for non-tech users
# ──────────────────────────────────────────────

with st.sidebar:
    st.markdown('<div class="hero-title" style="font-size:1.5rem;">⚽ Football News</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#8892b0;font-size:0.85rem;margin-bottom:1.5rem;">English Football News Explorer</p>', unsafe_allow_html=True)

    # Connection status
    alive = backend_alive()
    if alive:
        st.markdown('<div style="text-align:center;"><span class="live-dot"></span> <span style="color:#48bb78;font-weight:600;">Connected</span></div>', unsafe_allow_html=True)
    else:
        st.error("Backend Not Running")
        st.code("python run.py", language="bash")

    st.markdown("---")

    # ─── News Type — Simple selection ─────────
    st.markdown("### 📰 News Type")
    news_type = st.radio(
        "What would you like to see?",
        list(NEWS_TYPES.keys()),
        format_func=lambda x: NEWS_TYPES[x]["name"],
        label_visibility="collapsed",
        index=0,
    )
    st.markdown(f'<p style="color:#8892b0;font-size:0.8rem;margin-top:-8px;">{NEWS_TYPES[news_type]["desc"]}</p>', unsafe_allow_html=True)

    st.markdown("---")

    # ─── League Quick Filters ─────────────────
    st.markdown("### 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Filter by League")
    st.markdown('<p style="color:#8892b0;font-size:0.78rem;margin-top:-8px;">Select leagues to filter (leave all unchecked to see everything)</p>', unsafe_allow_html=True)

    selected_filters = []

    # English Leagues
    st.markdown('<div class="league-section"><div class="league-section-title">🏟️ English Leagues</div></div>', unsafe_allow_html=True)
    for league_name, info in ENGLISH_LEAGUES.items():
        if st.checkbox(f"{info['icon']} {league_name}", key=f"filter_{league_name}"):
            selected_filters.append(league_name)

    # Domestic Cups
    st.markdown('<div class="league-section"><div class="league-section-title">🏅 Domestic Cups</div></div>', unsafe_allow_html=True)
    for cup_name, info in DOMESTIC_CUPS.items():
        if st.checkbox(f"{info['icon']} {cup_name}", key=f"filter_{cup_name}"):
            selected_filters.append(cup_name)

    # European Competitions
    st.markdown('<div class="league-section"><div class="league-section-title">⭐ European Competitions</div></div>', unsafe_allow_html=True)
    for comp_name, info in EUROPEAN_COMPETITIONS.items():
        if st.checkbox(f"{info['icon']} {comp_name}", key=f"filter_{comp_name}"):
            selected_filters.append(comp_name)

    st.markdown("---")

    # ─── Fetch Button ─────────────────────────
    fetch_btn = st.button("🔄 Refresh News", use_container_width=True, type="primary")

    st.markdown("---")

    # ─── Advanced Settings — Hidden by default ─
    with st.expander("⚙️ Advanced Settings", expanded=False):
        st.markdown('<p style="color:#8892b0;font-size:0.78rem;">For advanced users only. Default values work great!</p>', unsafe_allow_html=True)

        include = st.text_input("Includes", value="fixture.participants;league;lines",
                                help="Related data to include: fixture.participants, league, lines")
        order = st.selectbox("Sort Order", ["desc", "asc"],
                             help="Newest first (desc) or oldest first (asc)")
        per_page = st.slider("Articles Per Page", 1, 50, 50,
                             help="Number of articles per request")
        page = st.number_input("Page", min_value=1, value=1,
                               help="Pagination page number")
        season_id = st.number_input("Season ID (for season endpoints)", min_value=1, value=23614, step=1,
                                    help="SportMonks Season ID (e.g., 23614 for EPL 2024/25)")

    st.markdown("---")
    st.markdown("""
    <div style="color:#4a5568;font-size:0.72rem;text-align:center;">
        SportMonks v3 Football API<br>
        <a href="https://docs.sportmonks.com/football/endpoints-and-entities/endpoints/news" target="_blank" style="color:#3a7bd5;">Documentation ↗</a>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Set defaults for advanced params if expander not opened
# ──────────────────────────────────────────────

try:
    _ = include
except NameError:
    include = "fixture.participants;league;lines"
try:
    _ = order
except NameError:
    order = "desc"
try:
    _ = per_page
except NameError:
    per_page = 50
try:
    _ = page
except NameError:
    page = 1
try:
    _ = season_id
except NameError:
    season_id = 23614


# ──────────────────────────────────────────────
# FETCH FUNCTIONS
# ──────────────────────────────────────────────

def fetch_news(ntype: str, p: int = 1, pp: int = 50) -> dict:
    """Fetch news based on the simple news type selector."""
    params = {"include": include, "order": order, "per_page": pp, "page": p}

    if ntype == "latest":
        return call("/api/news/pre-match", params)
    elif ntype == "upcoming":
        return call("/api/news/pre-match/upcoming", params)
    elif ntype == "post_match":
        return call("/api/news/post-match", params)
    return {"error": True, "message": "Unknown news type"}


def fetch_combined_latest(pp: int = 50) -> dict:
    """Fetch both pre-match and post-match for the 'Latest News' view."""
    params = {"include": include, "order": order, "per_page": pp, "page": 1}

    pre_data = call("/api/news/pre-match", params)
    post_data = call("/api/news/post-match", params)

    combined_articles = []
    pagination = {}
    rate_limit = {}
    subscription = []

    if not pre_data.get("error") and isinstance(pre_data.get("data"), list):
        combined_articles.extend(pre_data["data"])
        pagination = pre_data.get("pagination", {})
        rate_limit = pre_data.get("rate_limit", {})
        subscription = pre_data.get("subscription", [])

    if not post_data.get("error") and isinstance(post_data.get("data"), list):
        combined_articles.extend(post_data["data"])

    # Sort combined by created_at desc
    combined_articles.sort(
        key=lambda x: x.get("created_at", "") or "",
        reverse=True
    )

    return {
        "data": combined_articles,
        "pagination": pagination,
        "rate_limit": rate_limit,
        "subscription": subscription,
    }


# ──────────────────────────────────────────────
# MAIN CONTENT
# ──────────────────────────────────────────────

st.markdown('<div class="hero-title">⚽ Football News Explorer</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub"><span class="live-dot"></span> Live English Football News — Premier League, Championship, FA Cup, Champions League & More</div>', unsafe_allow_html=True)

# ─── Quick competition overview ───────────────
st.markdown("---")

with st.expander("ℹ️ Competitions Covered", expanded=False):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="article-card" style="text-align:center;padding:1.2rem;">
            <div style="font-size:1.5rem;margin-bottom:0.5rem;">🏟️</div>
            <div class="article-title" style="text-align:center;font-size:0.95rem;">English Leagues</div>
            <div style="color:#8892b0;font-size:0.82rem;line-height:1.8;">
                🏆 Premier League<br>
                🥈 Championship<br>
                🥉 League One<br>
                4️⃣ League Two
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="article-card" style="text-align:center;padding:1.2rem;">
            <div style="font-size:1.5rem;margin-bottom:0.5rem;">🏅</div>
            <div class="article-title" style="text-align:center;font-size:0.95rem;">Domestic Cups</div>
            <div style="color:#8892b0;font-size:0.82rem;line-height:1.8;">
                🏅 FA Cup<br>
                🍵 Carabao Cup (EFL Cup)
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="article-card" style="text-align:center;padding:1.2rem;">
            <div style="font-size:1.5rem;margin-bottom:0.5rem;">⭐</div>
            <div class="article-title" style="text-align:center;font-size:0.95rem;">European Competitions</div>
            <div style="color:#8892b0;font-size:0.82rem;line-height:1.8;">
                ⭐ Champions League<br>
                🌍 Europa League<br>
                🌐 Europa Conference League
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")


# ──────────────────────────────────────────────
# AUTO-LOAD or MANUAL FETCH
# ──────────────────────────────────────────────

should_fetch = False

# Manual refresh button pressed
if fetch_btn:
    should_fetch = True
    st.session_state.news_data = None  # Clear cache to force re-fetch

# Auto-load on first visit
if not st.session_state.auto_loaded and alive:
    should_fetch = True
    st.session_state.auto_loaded = True

if should_fetch and alive:
    type_info = NEWS_TYPES[news_type]

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:0.5rem;">
        <span style="color:#e6f1ff;font-size:1.5rem;font-weight:700;">{type_info['name']}</span>
        <span class="badge-live">LIVE</span>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Fetching latest football news..."):
        if news_type == "latest":
            data = fetch_combined_latest(per_page)
        else:
            data = fetch_news(news_type, page, per_page)

    st.session_state.news_data = data
    st.session_state.news_type = news_type
    render_results_section(data, selected_filters)

elif st.session_state.news_data and alive:
    # Re-render cached data (when filters change, no re-fetch needed)
    type_info = NEWS_TYPES.get(st.session_state.news_type, NEWS_TYPES["latest"])
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:0.5rem;">
        <span style="color:#e6f1ff;font-size:1.5rem;font-weight:700;">{type_info['name']}</span>
        <span class="badge-live">LIVE</span>
    </div>
    """, unsafe_allow_html=True)
    render_results_section(st.session_state.news_data, selected_filters)

elif not alive:
    st.markdown("""
    <div class="welcome-card">
        <div style="font-size:3.5rem;margin-bottom:1rem;">🔌</div>
        <div style="color:#e6f1ff;font-size:1.4rem;font-weight:700;margin-bottom:0.8rem;">
            Connecting to Server...
        </div>
        <div style="color:#8892b0;font-size:1rem;line-height:1.6;max-width:600px;margin:0 auto;">
            The backend server is not reachable. Please make sure it's running.
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="welcome-card">
        <div style="font-size:3.5rem;margin-bottom:1rem;">📰</div>
        <div style="color:#e6f1ff;font-size:1.4rem;font-weight:700;margin-bottom:0.8rem;">
            Click "Refresh News" to Load Articles
        </div>
        <div style="color:#8892b0;font-size:1rem;line-height:1.6;max-width:600px;margin:0 auto;">
            Select a news type from the sidebar and click Refresh to see the latest football news.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────

st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#4a5568;font-size:0.78rem;padding:1rem 0;">
    Football News Explorer &nbsp;•&nbsp; Powered by SportMonks v3 API &nbsp;•&nbsp; Live Data &nbsp;•&nbsp;
    <a href="https://docs.sportmonks.com/football/endpoints-and-entities/endpoints/news" target="_blank" style="color:#3a7bd5;">API Docs ↗</a>
</div>
""", unsafe_allow_html=True)
