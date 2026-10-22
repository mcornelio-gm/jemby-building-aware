# Cloud Run Persistence & Deployment Architecture

## Google Cloud Storage (GCS) Durable Storage
- **Bucket**: `gs://building-aware-data-storage-774200339208`
- **Object Versioning**: Enabled.
- **Authoritative Hydration**: In [james_app/gcs_sync.py](file:///Users/michaelcornelio/jemby/jemby_solutions/jemby_gcp/JAMES_Development/james_app/gcs_sync.py), `hydrate_from_gcs()` unconditionally pulls all non-empty files from GCS on startup. Container image file defaults never overwrite live production databases.
- **Synchronous Persistence**: User mutations (password resets, user profile updates) and facility site configs must be saved synchronously via `sync_file_to_gcs_sync()` within the HTTP request lifecycle. Cloud Run throttles container CPU to near zero outside active requests, so detached daemon threads must not be used for critical mutations.
- **Docker Build Context**: [JAMES_Development/.dockerignore](file:///Users/michaelcornelio/jemby/jemby_solutions/jemby_gcp/JAMES_Development/.dockerignore) excludes `data/users.db`, `data/users.json`, `data/audit.jsonl`, and SQLite journal files so local developer machine states are never baked into container images.
- **Background Sweeps**: `background_gcs_sync_worker` runs sequentially (every 300s via `asyncio.to_thread`) to avoid socket connection exhaustion or SSL EOF errors on Cloud Run.

## Pending Verification Reminder
- **Password Persistence Check**: Michael Cornelio changed his password on 2026-10-21. After the next container build and deployment, verify that his password remains intact and does not revert to default credentials.
