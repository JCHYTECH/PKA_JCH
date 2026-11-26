#!/usr/bin/env python3
"""Publie des images et lit les statistiques Instagram via Meta Graph API."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests

DEFAULT_API_VERSION = "v26.0"
DEFAULT_INSIGHT_METRICS = "reach,likes,comments,shares,saved"
KEYCHAIN_ACCOUNT = "wildlens"
REQUEST_TIMEOUT = 30


class InstagramError(RuntimeError):
    pass


def keychain_value(service: str) -> str:
    try:
        result = subprocess.run(
            [
                "security",
                "find-generic-password",
                "-s",
                service,
                "-a",
                KEYCHAIN_ACCOUNT,
                "-w",
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise InstagramError(f"Lecture du Keychain impossible pour {service} : {exc}") from exc
    value = result.stdout.strip()
    if result.returncode != 0 or not value:
        raise InstagramError(
            f"Entrée Keychain absente : service {service}, compte {KEYCHAIN_ACCOUNT}."
        )
    return value


def credentials() -> tuple[str, str]:
    token = os.environ.get("IG_GRAPH_TOKEN") or keychain_value("IG_GRAPH_TOKEN")
    user_id = os.environ.get("IG_USER_ID") or keychain_value("IG_USER_ID")
    return token, user_id


def validate_image_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise InstagramError("L’image doit utiliser une URL HTTPS publique.")
    if Path(parsed.path).suffix.lower() == ".png":
        raise InstagramError("Instagram exige un JPEG ; les PNG ne sont pas acceptés.")


def read_caption(args: argparse.Namespace) -> str:
    if args.caption_file:
        try:
            caption = args.caption_file.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise InstagramError(f"Lecture de la légende impossible : {exc}") from exc
    else:
        caption = args.caption.strip()
    if not caption:
        raise InstagramError("La légende ne peut pas être vide.")
    if len(caption) > 2200:
        raise InstagramError("La légende dépasse la limite Instagram de 2200 caractères.")
    return caption


class InstagramClient:
    def __init__(self, token: str, user_id: str, api_version: str = DEFAULT_API_VERSION):
        self.user_id = user_id
        self.base_url = f"https://graph.facebook.com/{api_version}"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        try:
            response = self.session.request(
                method,
                f"{self.base_url}/{path.lstrip('/')}",
                timeout=REQUEST_TIMEOUT,
                **kwargs,
            )
        except requests.RequestException as exc:
            raise InstagramError(f"Requête Meta impossible : {exc}") from exc
        try:
            payload = response.json()
        except ValueError as exc:
            raise InstagramError(
                f"Réponse Meta non JSON (HTTP {response.status_code})."
            ) from exc
        if not response.ok or "error" in payload:
            error = payload.get("error", {})
            message = error.get("message", "Erreur Meta inconnue")
            code = error.get("code", response.status_code)
            raise InstagramError(f"Meta Graph API ({code}) : {message}")
        return payload

    def account(self) -> dict[str, Any]:
        return self.request(
            "GET",
            self.user_id,
            params={"fields": "id,username,media_count"},
        )

    def create_container(self, image_url: str, caption: str) -> str:
        payload = self.request(
            "POST",
            f"{self.user_id}/media",
            data={"image_url": image_url, "caption": caption},
        )
        container_id = payload.get("id")
        if not container_id:
            raise InstagramError("Meta n’a pas renvoyé d’identifiant de conteneur.")
        return str(container_id)

    def wait_for_container(self, container_id: str, timeout: int, interval: float) -> None:
        deadline = time.monotonic() + timeout
        while True:
            payload = self.request(
                "GET",
                container_id,
                params={"fields": "status_code,status"},
            )
            status = payload.get("status_code")
            if status == "FINISHED":
                return
            if status in {"ERROR", "EXPIRED"}:
                detail = payload.get("status", "aucun détail fourni")
                raise InstagramError(f"Conteneur {container_id} en échec ({status}) : {detail}")
            if time.monotonic() >= deadline:
                raise InstagramError(
                    f"Conteneur {container_id} toujours non publiable après {timeout} secondes."
                )
            time.sleep(interval)

    def publish_container(self, container_id: str) -> str:
        payload = self.request(
            "POST",
            f"{self.user_id}/media_publish",
            data={"creation_id": container_id},
        )
        media_id = payload.get("id")
        if not media_id:
            raise InstagramError("Meta n’a pas renvoyé d’identifiant de publication.")
        return str(media_id)

    def recent_media(self, limit: int, with_insights: bool = False) -> dict[str, Any]:
        payload = self.request(
            "GET",
            f"{self.user_id}/media",
            params={
                "fields": (
                    "id,caption,media_type,media_url,permalink,timestamp,"
                    "like_count,comments_count"
                ),
                "limit": limit,
            },
        )
        if with_insights:
            for media in payload.get("data", []):
                media["insights"] = self.insights(media["id"], DEFAULT_INSIGHT_METRICS)
        return payload

    def insights(self, media_id: str, metrics: str) -> list[dict[str, Any]]:
        payload = self.request(
            "GET",
            f"{media_id}/insights",
            params={"metric": metrics},
        )
        return payload.get("data", [])


def build_client(args: argparse.Namespace) -> InstagramClient:
    token, user_id = credentials()
    return InstagramClient(token, user_id, args.api_version)


def cmd_account(args: argparse.Namespace) -> None:
    print(json.dumps(build_client(args).account(), ensure_ascii=False, indent=2))


def cmd_publish(args: argparse.Namespace) -> None:
    validate_image_url(args.image_url)
    caption = read_caption(args)
    if not args.confirm:
        print(
            json.dumps(
                {
                    "mode": "simulation",
                    "network_requests": 0,
                    "image_url": args.image_url,
                    "caption_characters": len(caption),
                    "next_step": "Ajouter --confirm pour publier réellement.",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return
    client = build_client(args)
    container_id = client.create_container(args.image_url, caption)
    client.wait_for_container(container_id, args.timeout, args.poll_interval)
    media_id = client.publish_container(container_id)
    print(
        json.dumps(
            {"container_id": container_id, "media_id": media_id, "published": True},
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_media(args: argparse.Namespace) -> None:
    payload = build_client(args).recent_media(args.limit, args.with_insights)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def cmd_insights(args: argparse.Namespace) -> None:
    data = build_client(args).insights(args.media_id, args.metrics)
    print(json.dumps({"data": data}, ensure_ascii=False, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publication et statistiques Instagram WildLens"
    )
    parser.add_argument("--api-version", default=DEFAULT_API_VERSION)
    subparsers = parser.add_subparsers(dest="command", required=True)

    account = subparsers.add_parser("account", help="Vérifier l’accès au compte Instagram")
    account.set_defaults(func=cmd_account)

    publish = subparsers.add_parser("publish", help="Publier une image JPEG")
    publish.add_argument("--image-url", required=True, help="URL HTTPS publique du JPEG")
    captions = publish.add_mutually_exclusive_group(required=True)
    captions.add_argument("--caption", help="Légende et hashtags")
    captions.add_argument("--caption-file", type=Path, help="Fichier texte de la légende")
    publish.add_argument(
        "--confirm",
        action="store_true",
        help="Publier réellement ; sans cette option, simulation locale uniquement",
    )
    publish.add_argument("--timeout", type=int, default=120)
    publish.add_argument("--poll-interval", type=float, default=5)
    publish.set_defaults(func=cmd_publish)

    media = subparsers.add_parser("media", help="Lister les publications récentes")
    media.add_argument("--limit", type=int, default=5, choices=range(1, 26))
    media.add_argument("--with-insights", action="store_true")
    media.set_defaults(func=cmd_media)

    insights = subparsers.add_parser("insights", help="Lire les statistiques d’un média")
    insights.add_argument("--media-id", required=True)
    insights.add_argument("--metrics", default=DEFAULT_INSIGHT_METRICS)
    insights.set_defaults(func=cmd_insights)

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        args.func(args)
    except InstagramError as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
