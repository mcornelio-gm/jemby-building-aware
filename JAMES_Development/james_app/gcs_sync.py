"""
JAMES Cloud Storage Persistence & Synchronization Engine.

Provides bidirectional synchronization between local ephemeral container storage
(/app/data) and durable Google Cloud Storage (GCS) buckets.
Ensures zero data loss across Cloud Run revisions, cold starts, and container lifecycles.
"""

import os
import sys
import time
import logging
import threading
import asyncio
from pathlib import Path
from typing import Optional, List

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.getenv("JAMES_DATA_DIR", str(BASE_DIR / "data")))
GCS_DATA_BUCKET = os.getenv("GCS_DATA_BUCKET", "building-aware-data-storage-774200339208")

logger = logging.getLogger("james.gcs_sync")
logger.setLevel(logging.INFO)

_client = None
_bucket = None
_init_attempted = False


def _get_gcs_bucket():
    """Lazily initialize Google Cloud Storage client and bucket handle."""
    global _client, _bucket, _init_attempted
    if _bucket is not None:
        return _bucket
    if _init_attempted:
        return None

    _init_attempted = True
    if not GCS_DATA_BUCKET:
        logger.info("GCS_DATA_BUCKET not configured. Running with local filesystem only.")
        return None

    try:
        from google.cloud import storage
        _client = storage.Client()
        _bucket = _client.bucket(GCS_DATA_BUCKET)
        logger.info(f"Successfully connected to durable GCS storage bucket: gs://{GCS_DATA_BUCKET}")
        return _bucket
    except Exception as e:
        logger.warning(f"Could not connect to GCS bucket '{GCS_DATA_BUCKET}': {e}. Using local storage.")
        return None


def hydrate_from_gcs() -> int:
    """
    On app startup: Download all persistent files from GCS.
    In ephemeral container runtimes (Cloud Run), any non-empty remote object in GCS
    is the authoritative durable state and overrides local container image seeds.
    Returns the count of hydrated files.
    """
    bucket = _get_gcs_bucket()
    if not bucket:
        return 0

    downloaded_count = 0
    try:
        prefix = "data/"
        blobs = list(bucket.list_blobs(prefix=prefix))
        logger.info(f"Checking {len(blobs)} remote objects in gs://{GCS_DATA_BUCKET}/data/ for hydration...")

        for blob in blobs:
            rel_name = blob.name[len(prefix):] if blob.name.startswith(prefix) else blob.name
            if not rel_name or rel_name.endswith("/"):
                continue

            target_file = DATA_DIR / rel_name
            target_file.parent.mkdir(parents=True, exist_ok=True)

            # In Cloud Run, GCS is the authoritative source of truth.
            # Download any non-empty blob so container image defaults never clobber production data.
            if blob.size and blob.size > 0:
                blob.download_to_filename(str(target_file))
                downloaded_count += 1
                logger.info(f"Hydrated from GCS: {rel_name} ({blob.size} bytes)")

        logger.info(f"GCS Hydration complete. {downloaded_count} files synchronized.")
    except Exception as e:
        logger.error(f"Error during GCS hydration: {e}")

    return downloaded_count


def sync_file_to_gcs_sync(local_path: Path) -> bool:
    """
    Synchronously push a single mutated file to GCS.
    Essential for Cloud Run request handlers where background threads are frozen
    by CPU throttling immediately after HTTP responses finish.
    """
    try:
        bucket = _get_gcs_bucket()
        if not bucket:
            return False
        if not local_path.exists():
            return False

        try:
            rel_path = local_path.relative_to(DATA_DIR)
        except ValueError:
            rel_path = local_path.name

        blob_name = f"data/{rel_path}"
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(str(local_path))
        logger.info(f"Synchronously persisted to GCS: {blob_name}")
        return True
    except Exception as e:
        logger.warning(f"Failed to synchronously sync {local_path} to GCS: {e}")
        return False


def sync_file_to_gcs_async(local_path: Path) -> None:
    """Non-blocking background thread to push a single mutated file to GCS."""
    def _upload():
        sync_file_to_gcs_sync(local_path)

    threading.Thread(target=_upload, daemon=True).start()


def sync_client_facility_to_gcs(client_id: str, facility_id: str, synchronous: bool = True) -> None:
    """Synchronize an entire client facility SQLite db and companion files to GCS."""
    facility_dir = DATA_DIR / "clients" / client_id / facility_id
    if not facility_dir.exists():
        return

    for item in facility_dir.glob("*"):
        if item.is_file() and not item.name.endswith("-journal") and not item.name.endswith("-wal"):
            if synchronous:
                sync_file_to_gcs_sync(item)
            else:
                sync_file_to_gcs_async(item)


def sync_all_data_to_gcs() -> None:
    """Full synchronization sweep of all data files to GCS."""
    bucket = _get_gcs_bucket()
    if not bucket or not DATA_DIR.exists():
        return

    for path in DATA_DIR.rglob("*"):
        if path.is_file():
            if path.name.endswith("-journal") or path.name.endswith("-wal") or path.name.startswith("."):
                continue
            sync_file_to_gcs_async(path)


async def background_gcs_sync_worker(interval_seconds: int = 45):
    """Periodic background task that periodically ensures all files are mirrored to GCS."""
    while True:
        try:
            await asyncio.sleep(interval_seconds)
            sync_all_data_to_gcs()
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.debug(f"Background sync worker tick error: {e}")
