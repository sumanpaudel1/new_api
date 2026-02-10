"""
FastAPI Backend for SportMonks News API Explorer.
Proxies SportMonks Football News API — real data from Pro plan.
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from backend.services.sportmonks import sportmonks_service
from backend.config import settings

app = FastAPI(
    title="SportMonks News API Explorer",
    description="FastAPI backend — Real SportMonks Football News API (Pro plan)",
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────
# HEALTH
# ──────────────────────────────────────────────

@app.get("/", tags=["Health"])
async def root():
    return {"status": "running", "message": "SportMonks News API Explorer v3 — LIVE"}


@app.get("/api/token-status", tags=["Health"])
async def token_status():
    token = settings.sportmonks_api_token
    configured = token and token != "YOUR_TOKEN_HERE" and token.strip('"') != "YOUR_TOKEN_HERE"
    clean = token.strip('"') if token else ""
    return {"configured": configured, "token_preview": f"{clean[:8]}..." if configured else "NOT SET"}


# ──────────────────────────────────────────────
# NEWS ENDPOINTS — PRE-MATCH (Real API data)
# ──────────────────────────────────────────────

@app.get("/api/news/pre-match", tags=["News — Pre-Match"])
async def get_pre_match_news(
    include: Optional[str] = Query("fixture.participants;league;lines"),
    order: Optional[str] = Query("desc"),
    per_page: Optional[int] = Query(50),
    page: Optional[int] = Query(1),
):
    """All available pre-match news articles (LIVE from SportMonks)."""
    return await sportmonks_service.get_pre_match_news(include, order, per_page, page)


@app.get("/api/news/pre-match/seasons/{season_id}", tags=["News — Pre-Match"])
async def get_pre_match_news_by_season(
    season_id: int,
    include: Optional[str] = Query("fixture.participants;league;lines"),
    order: Optional[str] = Query("desc"),
    per_page: Optional[int] = Query(50),
    page: Optional[int] = Query(1),
):
    """Pre-match news filtered by season ID (LIVE)."""
    return await sportmonks_service.get_pre_match_news_by_season(season_id, include, order, per_page, page)


@app.get("/api/news/pre-match/upcoming", tags=["News — Pre-Match"])
async def get_pre_match_news_upcoming(
    include: Optional[str] = Query("fixture.participants;league;lines"),
    order: Optional[str] = Query("desc"),
    per_page: Optional[int] = Query(50),
    page: Optional[int] = Query(1),
):
    """Pre-match news for upcoming fixtures (LIVE)."""
    return await sportmonks_service.get_pre_match_news_upcoming(include, order, per_page, page)


# ──────────────────────────────────────────────
# NEWS ENDPOINTS — POST-MATCH (Real API data)
# ──────────────────────────────────────────────

@app.get("/api/news/post-match", tags=["News — Post-Match"])
async def get_post_match_news(
    include: Optional[str] = Query("fixture.participants;league;lines"),
    order: Optional[str] = Query("desc"),
    per_page: Optional[int] = Query(50),
    page: Optional[int] = Query(1),
):
    """All available post-match news articles (LIVE from SportMonks)."""
    return await sportmonks_service.get_post_match_news(include, order, per_page, page)


@app.get("/api/news/post-match/seasons/{season_id}", tags=["News — Post-Match"])
async def get_post_match_news_by_season(
    season_id: int,
    include: Optional[str] = Query("fixture.participants;league;lines"),
    order: Optional[str] = Query("desc"),
    per_page: Optional[int] = Query(50),
    page: Optional[int] = Query(1),
):
    """Post-match news filtered by season ID (LIVE)."""
    return await sportmonks_service.get_post_match_news_by_season(season_id, include, order, per_page, page)
