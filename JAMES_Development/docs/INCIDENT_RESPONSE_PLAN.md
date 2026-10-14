# Incident Response Plan (IRP)
**Building Aware / JAMES Digital Twin Platform**

---

## 1. Purpose & Scope

This **Incident Response Plan (IRP)** defines the structured protocol for detecting, triaging, containing, remediating, and reviewing security incidents, critical operational outages, and data integrity failures affecting the **Building Aware (JAMES)** electrical digital twin infrastructure.

### 1.1 Scope
This policy applies to:
- **Application Services**: Cloud Run containers (`james-digital-twin`), FastAPI backends, HTMX frontends, CAD/DXF rendering engines.
- **Data Stores & Persistence**: SQLite databases (`model.db`), JSONL audit ledgers (`model.jsonl`), Google Cloud Storage (GCS) buckets, and survey catalog stores.
- **Infrastructure & Identity**: Google Cloud Platform (GCP) IAM service accounts, DNS/TLS routing (`dev.buildingaware.io`), Cloud Build CI/CD pipelines, and local field surveying sync caches.
- **Personnel**: Core engineering, platform operations, facility surveyors, and customer support.

---

## 2. Incident Response Team & Roles

| Role | Primary Responsibilities |
| :--- | :--- |
| **Incident Commander (IC)** | Holds overall authority during the incident; coordinates cross-functional response, sets severity, and approves major containment actions. |
| **Technical Lead / DevOps** | Conducts root cause analysis, implements infrastructure fixes, deploys rollbacks, or performs data restoration. |
| **Security Officer** | Investigates suspected breaches, unauthorized access, credential leakage, and leads forensic containment. |
| **Communications Lead** | Manages internal status updates and customer-facing notifications for impacted facility operators/clients. |

---

## 3. Incident Severity Classification (SEV Levels)

```
+-------------------------------------------------------------------------------+
|  SEV-1 (Critical) : Total Outage, Data Breach, or Data Corruption            |
|  SEV-2 (Major)    : Core Feature Unavailable (e.g. SLD Viewer / Survey Sync)  |
|  SEV-3 (Moderate) : Non-critical Bug / Single Facility Degradation            |
|  SEV-4 (Minor)    : Cosmetic Discrepancy / Minor UI Glitch                    |
+-------------------------------------------------------------------------------+
```

| Severity Level | Definition / Examples | Response SLA | Target Resolution |
| :--- | :--- | :--- | :--- |
| **SEV-1 (Critical)** | • Complete outage of `dev.buildingaware.io` / production.<br>• Unrecoverable database corruption or data loss.<br>• Verified unauthorized access or GCP IAM credential compromise. | **< 15 minutes** | < 2 hours |
| **SEV-2 (Major)** | • CAD/SLD engine failing across multiple facilities.<br>• Field survey data sync failing.<br>• Service response latency exceeding 5,000ms. | **< 30 minutes** | < 4 hours |
| **SEV-3 (Moderate)** | • Single facility model parsing error.<br>• Export failure for specific edge format.<br>• Transient background task timeout. | **< 2 hours** | < 24 hours |
| **SEV-4 (Minor)** | • Minor UI rendering glitch.<br>• Labeling typo in CAD title block.<br>• Non-blocking documentation discrepancy. | **< 1 business day** | Next release cycle |

---

## 4. Incident Response Lifecycle

The incident handling process follows the 6-phase NIST SP 800-61 / SANS framework:

```
+----------------+     +---------------+     +-----------------+
| 1. Preparation | --> | 2. Detection  | --> | 3. Containment  |
+----------------+     +---------------+     +-----------------+
                                                      |
+----------------+     +---------------+              v
| 6. Post-Mortem | <-- | 5. Recovery   | <-- +-----------------+
+----------------+     +---------------+     | 4. Eradication  |
                                             +-----------------+
```

### Phase 1: Preparation
- Automated Cloud Run healthchecks enabled on `http://localhost:8000/api/catalog`.
- Dual-layer audit logging of all survey and node mutations via `james_app/audit_logger.py`.
- Immutable container artifact tags stored in Google Artifact Registry / GCR.
- Automated daily backup snapshots of facility SQLite and JSONL files to GCS.

### Phase 2: Detection & Triage
1. **Detection Sources**:
   - Automated alerts (Cloud Monitoring uptime checks, Cloud Run 5xx alert policies).
   - User or surveyor reports of synchronization or rendering errors.
   - Audit log anomaly detection.
2. **Immediate Triage Actions**:
   - Incident Commander assesses blast radius and sets initial SEV level.
   - Open dedicated Incident War Room channel (Slack/Discord/Google Meet).
   - Log timestamped incident event timeline.

### Phase 3: Containment
- **Service Disruption**: If a bad release caused the outage, execute instant 100% traffic diversion to previous known-good Cloud Run revision (see Runbook §5.1).
- **Security Breach / Compromise**: Revoke compromised GCP Service Account keys; rotate API secrets in Secret Manager.
- **Data Inconsistency**: Place affected facility endpoints in read-only mode to prevent write corruption propagation.

### Phase 4: Eradication
- Identify underlying code defect, memory leak, or misconfigured infrastructure.
- Patch code in a hotfix branch; run automated test suite (`pytest tests/`).
- Build and push verified container image to Cloud Build.

### Phase 5: Recovery & Verification
- Deploy verified container revision to Cloud Run.
- Route 10% canary traffic $\to$ inspect telemetry $\to$ ramp to 100%.
- Run end-to-end integration tests on CAD SLD generation, SQLite models, and survey workflows.
- Confirm resolution with affected users/stakeholders.

### Phase 6: Post-Incident Review & Lessons Learned
- Conduct post-mortem within **48 hours** for SEV-1 and SEV-2 incidents.
- Produce a **Blameless Post-Mortem Document** identifying:
  - Root Cause Analysis (5 Whys).
  - Detection lag and response timeline.
  - Action items with owners and deadlines to prevent recurrence.

---

## 5. Technical Operational Runbooks

### 5.1 Cloud Run Instant Traffic Rollback
When a newly deployed container revision causes 500 errors or application crashes:

```bash
# 1. List recent revisions and active traffic allocation
gcloud run services describe james-digital-twin \
  --project=building-aware-test \
  --region=us-central1 \
  --format="table(status.traffic)"

# 2. Revert 100% traffic to the last known stable revision (e.g. 00029-xs7)
gcloud run services update-traffic james-digital-twin \
  --to-revisions=james-digital-twin-00029-xs7=100 \
  --project=building-aware-test \
  --region=us-central1
```

### 5.2 Database & Model Recovery from Backup
If a facility's `model.db` or `model.jsonl` encounters file corruption:

```bash
# 1. Inspect audit ledger for the facility
cd /app/data/clients/{client_id}/{facility_id}

# 2. Re-synthesize SQLite database from authoritative JSONL transaction stream
python3 -c "
from james_app.db import rebuild_db_from_jsonl
rebuild_db_from_jsonl('{client_id}', '{facility_id}')
"

# 3. If JSONL is damaged, pull the latest verified GCS snapshot
gcloud storage cp gs://building-aware-backups/{client_id}/{facility_id}/model_snapshot_latest.jsonl ./model.jsonl
```

### 5.3 GCP Service Account & Credential Rotation
In the event of suspected key exposure or unauthorized access:

```bash
# 1. List active keys for the compromised service account
gcloud iam service-accounts keys list \
  --iam-account=james-app-sa@building-aware-test.iam.gserviceaccount.com

# 2. Create replacement key and update Secret Manager
gcloud iam service-accounts keys create ./new-key.json \
  --iam-account=james-app-sa@building-aware-test.iam.gserviceaccount.com

# 3. Revoke and delete the compromised key ID
gcloud iam service-accounts keys delete {KEY_ID} \
  --iam-account=james-app-sa@building-aware-test.iam.gserviceaccount.com
```

### 5.4 Emergency Read-Only Mode
If a database engine or disk volume is failing, toggle emergency read-only enforcement via environment variable:

```bash
gcloud run services update james-digital-twin \
  --update-env-vars=READ_ONLY_MODE=true \
  --project=building-aware-test \
  --region=us-central1
```

---

## 6. Communication & Notification Templates

### 6.1 Initial Stakeholder Notification (SEV-1 / SEV-2)
> **Subject**: [INVESTIGATING] Building Aware Digital Twin Service Disruption - SEV-{1/2}  
> **Status**: Investigating  
> **Impact**: Users may experience {describe impact, e.g., inability to render CAD Single-Line Diagrams / access facility twin models}.  
> **Action Taken**: The engineering team is actively investigating the root cause. Next update will be provided in 30 minutes.

### 6.2 Incident Resolution Notification
> **Subject**: [RESOLVED] Building Aware Digital Twin Service Restored  
> **Status**: Resolved  
> **Summary**: The disruption affecting {impacted system} has been resolved. All services, CAD generation, and digital twin models are operating normally.  
> **Follow-Up**: A complete post-incident review will be conducted within 48 hours.

---

## 7. Document Revision & Maintenance

| Version | Date | Author | Description |
| :--- | :--- | :--- | :--- |
| **1.0.0** | October 2026 | Platform Engineering | Initial enterprise Incident Response Plan for Building Aware / JAMES Digital Twin. |
