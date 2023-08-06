import json
import secrets
import time
from pathlib import Path
from typing import Dict, List, Optional

from melon_translate_client import module
from melon_translate_client.request import fetch_all, fetch_all_par
from melon_translate_client.settings import (
    TRANSLATE_CACHE_VIEW_TTL,
    TRANSLATE_ENABLED,
    TRANSLATE_TTL_JITTER,
    log,
)
from redis_om import Field, HashModel, NotFoundError, get_redis_connection


def check_view_refresh(cls_method):
    """Check if view is expired and refresh it if needed."""

    def _wrapper(cls, language, key):
        """Wrapper for cls_method."""
        fetched_key = cls_method(cls, language, key)

        if isinstance(fetched_key, TranslateKey):
            views = []

            for vw in fetched_key.views.split(","):
                query = (TranslateView.name == vw) & (
                    TranslateView.language == language
                )
                try:
                    view = TranslateView.find(query).first()
                    if view and view.expired():
                        log.info(f"FOUND VIEW EXPIRED - REFRESHING {view.name}")
                        views.append(view.name)
                except NotFoundError:
                    log.info(f"View `{vw}` not found for language `{language}`")
                    TranslateView(name=vw, language=language).refresh()

            if views:
                log.info(f"Refreshing views `{views}` for language `{language}`")
                TranslateView.refresh_bulk(language, views)

        return fetched_key.translation

    return _wrapper


class TranslateKey(HashModel):
    """Translate model."""

    snake_name: Optional[str] = Field(index=True)
    id_name: Optional[str] = Field(index=True)
    views: Optional[str] = Field(index=True, full_text_search=True)
    occurrences: Optional[str] = Field(index=True, full_text_search=True)
    usage_context: Optional[str]
    flags: Optional[str] = ""
    translation: Optional[str]
    language: Optional[str] = Field(index=True)
    updated_at: int = Field(default_factory=lambda: int(time.time()))

    class Meta:
        global_key_prefix = "melon_translate"
        model_key_prefix = "translate_key"

    @classmethod
    @check_view_refresh
    def by_key(cls, language: str, key: str) -> "TranslateKey":
        """Finds translation by snake_name or id_name. In case of not found, returns key itself."""
        qs = cls.find(
            ((cls.snake_name == key) | (cls.id_name == key))
            & (cls.language == language)
        )

        for item in qs:
            if item.snake_name == key or item.id_name == key:
                # NOTE: Actual result received from the client invocation will be translation itself due to the decorator.
                return item
        else:
            raise NotFoundError

    @classmethod
    def from_svc(cls, key_obj: dict, pipeline) -> Optional["TranslateKey"]:
        _id = key_obj.get("id")
        if not _id:
            return None

        _id = str(_id)
        _key = key_obj.get("key")
        _data = cls(
            pk=_id,
            snake_name=_key.get("snake_name"),
            id_name=_key.get("id_name"),
            views=",".join(_key.get("views")),
            translation=key_obj.get("translation"),
            language=key_obj.get("language"),
        )
        _data.save(pipeline=pipeline)
        return _data


class TranslateView(HashModel):
    """View model."""

    name: str = Field(index=True)
    language: str = Field(index=True)
    updated_at: int = Field(default_factory=lambda: int(time.time()))

    class Meta:
        global_key_prefix = "melon_translate"
        model_key_prefix = "translate_view"

    @classmethod
    def refresh_bulk(cls, language: str, view_names: List[str], page_size=1000) -> int:
        """Refreshes all views in bulk."""
        n_writes = 0
        pipeline = get_redis_connection().pipeline()

        with module.translate_module.lock_context() as ctx:
            if not ctx:
                log.error(
                    f"Failed to acquire lock for refresh_bulk `{language}`:`{view_names}`"
                )
                return 0

            for view in view_names:
                try:
                    view = TranslateView.find(
                        (TranslateView.name == view)
                        & (TranslateView.language == language)
                    ).first()
                    view.updated_at = int(time.time())
                    view.save(pipeline=pipeline)
                except NotFoundError:
                    TranslateView(
                        name=view,
                        language=language,
                        updated_at=int(time.time()),
                    ).save(pipeline=pipeline)
            pipeline.execute()

            for result_list in fetch_all_par(
                [language], view_names, page_size=page_size
            ):
                keys = [TranslateKey.from_svc(obj, pipeline) for obj in result_list]
                n_writes += len(keys)
                pipeline.execute()

        return n_writes

    def refresh(self, page_size=1000) -> int:
        """Fetches all keys for current view and language and caches them."""
        pipeline = get_redis_connection().pipeline()

        with module.translate_module.lock_context() as ctx:
            if not ctx:
                log.error(f"Failed to acquire lock for view `{self.name}` refresh")
                return 0

            fetched_keys = fetch_all(
                language=self.language,
                views=[self.name],
                page_size=page_size,
            )

        for obj in fetched_keys:
            TranslateKey.from_svc(obj, pipeline=pipeline)

        self.updated_at = int(time.time())
        self.save(pipeline=pipeline)
        pipeline.execute()

        return len(fetched_keys)

    def expired(self) -> bool:
        """Check if view is expired."""
        jitter = secrets.randbelow(TRANSLATE_TTL_JITTER + 1)
        expected_time = int(time.time()) - (TRANSLATE_CACHE_VIEW_TTL + jitter)
        return self.updated_at < expected_time

    def keys(self, default_attr="snake_name") -> Dict[str, str]:
        """Get all keys corresponding to a view."""
        all_keys = TranslateKey.find(
            (TranslateKey.views % self.name) & (TranslateKey.language == self.language)
        ).all()

        return {getattr(key, default_attr): key.translation for key in all_keys}


if TRANSLATE_ENABLED:
    setattr(module, "translate_module", module.TranslateClientModule())
