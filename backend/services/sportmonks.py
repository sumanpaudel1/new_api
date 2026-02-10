"""
SportMonks API Service Module.
Handles all HTTP requests to the SportMonks Football News API (Pro plan).
Endpoints: Pre-Match News, Post-Match News, Season & Upcoming filters.
"""

import httpx
from typing import Optional
from backend.config import settings


class SportMonksService:
    """Service class for interacting with SportMonks News API endpoints."""

    def __init__(self):
        self.base_url = settings.sportmonks_base_url
        self.api_token = settings.sportmonks_api_token
        self.timeout = 30.0

    def _build_params(
        self,
        include: Optional[str] = None,
        order: Optional[str] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ) -> dict:
        params = {"api_token": self.api_token}
        if include:
            params["include"] = include
        if order:
            params["order"] = order
        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page
        return params

    async def _make_request(self, url: str, params: dict) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                return {
                    "error": True,
                    "status_code": e.response.status_code,
                    "message": f"HTTP {e.response.status_code}: {e.response.text[:500]}",
                }
            except httpx.RequestError as e:
                return {"error": True, "message": f"Request Error: {str(e)}"}
            except Exception as e:
                return {"error": True, "message": f"Unexpected Error: {str(e)}"}

    # ──────────────────────────────────────────────
    # NEWS ENDPOINTS (Pro plan — real data)
    # ──────────────────────────────────────────────

    async def get_pre_match_news(
        self, include="fixture.participants;league;lines", order="desc", per_page=25, page=1
    ):
        """GET Pre-Match News — all available pre-match articles."""
        url = f"{self.base_url}/news/pre-match"
        return await self._make_request(
            url, self._build_params(include, order, per_page, page)
        )

    async def get_pre_match_news_by_season(
        self, season_id: int, include="fixture.participants;league;lines", order="desc", per_page=25, page=1
    ):
        """GET Pre-Match News by Season ID."""
        url = f"{self.base_url}/news/pre-match/seasons/{season_id}"
        return await self._make_request(
            url, self._build_params(include, order, per_page, page)
        )

    async def get_pre_match_news_upcoming(
        self, include="fixture.participants;league;lines", order="desc", per_page=25, page=1
    ):
        """GET Pre-Match News for Upcoming Fixtures."""
        url = f"{self.base_url}/news/pre-match/upcoming"
        return await self._make_request(
            url, self._build_params(include, order, per_page, page)
        )

    async def get_post_match_news(
        self, include="fixture.participants;league;lines", order="desc", per_page=25, page=1
    ):
        """GET Post-Match News — all post-match articles."""
        url = f"{self.base_url}/news/post-match"
        return await self._make_request(
            url, self._build_params(include, order, per_page, page)
        )

    async def get_post_match_news_by_season(
        self, season_id: int, include="fixture.participants;league;lines", order="desc", per_page=25, page=1
    ):
        """GET Post-Match News by Season ID."""
        url = f"{self.base_url}/news/post-match/seasons/{season_id}"
        return await self._make_request(
            url, self._build_params(include, order, per_page, page)
        )


sportmonks_service = SportMonksService()
