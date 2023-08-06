from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ultima_scraper_api.apis.onlyfans import SiteContent
from ultima_scraper_api.apis.onlyfans.classes.extras import endpoint_links

if TYPE_CHECKING:
    from ultima_scraper_api.apis.onlyfans.classes.user_model import (
        AuthModel,
        create_user,
    )


class create_post(SiteContent):
    def __init__(self, option: dict[str, Any], user: AuthModel | create_user) -> None:
        SiteContent.__init__(self, option, user)
        self.responseType: str = option.get("responseType")
        self.createdAt: str = option.get("postedAt")
        self.postedAtPrecise: str = option.get("postedAtPrecise")
        self.expiredAt: Any = option.get("expiredAt")
        text: str = option.get("text", "")
        self.text = str(text or "")
        raw_text: str = option.get("rawText", "")
        self.rawText = str(raw_text or "")
        self.lockedText: bool = option.get("lockedText")
        self.isFavorite: bool = option.get("isFavorite")
        self.isReportedByMe: bool = option.get("isReportedByMe")
        self.canReport: bool = option.get("canReport")
        self.canDelete: bool = option.get("canDelete")
        self.canComment: bool = option.get("canComment")
        self.canEdit: bool = option.get("canEdit")
        self.isPinned: bool = option.get("isPinned")
        self.favoritesCount: int = option.get("favoritesCount")
        self.mediaCount: int = option.get("mediaCount", 0)
        self.isMediaReady: bool = option.get("isMediaReady")
        self.voting: list = option.get("voting")
        self.isOpened: bool = option.get("isOpened")
        self.canToggleFavorite: bool = option.get("canToggleFavorite")
        self.streamId: Any = option.get("streamId")
        self.price: Any = option.get("price")
        self.hasVoting: bool = option.get("hasVoting")
        self.isAddedToBookmarks: bool = option.get("isAddedToBookmarks")
        self.isArchived: bool = option.get("isArchived")
        self.isDeleted: bool = option.get("isDeleted")
        self.hasUrl: bool = option.get("hasUrl")
        self.commentsCount: int = option.get("commentsCount")
        self.mentionedUsers: list = option.get("mentionedUsers")
        self.linkedUsers: list = option.get("linkedUsers")
        self.linkedPosts: list = option.get("linkedPosts")
        self.canViewMedia: bool = option.get("canViewMedia")
        self.preview: list[int] = option.get("preview", [])
        self.canPurchase: bool = option.get("canPurchase")
        self.comments: list[Any] = []

    def get_author(self):
        return self.author

    async def get_comments(self):
        epl = endpoint_links()
        link = epl.list_comments(self.responseType, self.id)
        links = epl.create_links(link, self.commentsCount)
        if links:
            results = await self.author.scrape_manager.bulk_scrape(links)
            self.comments = results
        return self.comments

    async def favorite(self):
        link = endpoint_links(
            identifier=f"{self.responseType}s",
            identifier2=self.id,
            identifier3=self.author.id,
        ).favorite
        results = await self.author.get_session_manager().json_request(
            link, method="POST"
        )
        self.isFavorite = True
        return results
