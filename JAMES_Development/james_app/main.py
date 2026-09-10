"""FastAPI Web Application Routes and HTMX API Controllers."""

import os
import re
import uuid
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

from fastapi import FastAPI, Form, File, UploadFile, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm.attributes import flag_modified

from james_app.catalog import get_catalog, get_equipment_schema
from james_app.master_catalog import get_master_catalog
from james_app.dot_compiler import compile_project_to_dot, compile_facility_to_dot
from james_app.models import Edge, Node, Project
from james_app import storage, db
from james_app.knowledge_base import KnowledgeBaseManager
from james_app.integrity_audit import (
    audit_facility_system_integrity,
    generate_markdown_report,
    generate_csv_report,
    generate_txt_report,
    generate_pdf_report
)
from james_app.checklists import (
    get_all_checklists,
    get_checklist_by_id,
    get_checklists_for_domain,
    load_master_checklists
)

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Building Aware - Electrical Digital Twin", version="1.2.0")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/", response_class=RedirectResponse)
def root():
    """Redirect root access to Survey workbench."""
    return RedirectResponse(url="/survey")


@app.get("/api/catalog")
def api_get_catalog():
    """Return legacy JSON Master Catalog schemas."""
    return get_catalog()


@app.get("/catalog", response_class=HTMLResponse)
def get_catalog_studio_view(
    request: Request,
    client: Optional[str] = None,
    facility: Optional[str] = None,
    client_id: Optional[str] = None,
    facility_id: Optional[str] = None
):
    """Render the full Master Catalog Studio UI for parts management and CRUD."""
    active_client = (client or client_id or "zoetis").strip().lower()
    active_facility = (facility or facility_id or "b4").strip().lower()
    return templates.TemplateResponse(
        request=request,
        name="catalog_studio.html",
        context={
            "client_id": active_client,
            "facility_id": active_facility,
            "master_catalog_items": get_master_catalog().get_all_items(),
            "manufacturers": get_master_catalog().get_manufacturers(),
            "stats": get_master_catalog().get_catalog_stats()
        }
    )


@app.get("/api/catalog/stats")
def api_get_catalog_stats():
    """Return summary statistics across all catalog equipment."""
    return get_master_catalog().get_catalog_stats()


@app.get("/api/catalog/manufacturers")
def api_get_catalog_manufacturers(domain: Optional[str] = None, type_tag: Optional[str] = None):
    """Retrieve manufacturers filtered by domain and/or type_tag."""
    return get_master_catalog().get_manufacturers(domain=domain, type_tag=type_tag)


@app.get("/api/catalog/items")
def api_get_catalog_items(
    manufacturer: Optional[str] = None,
    domain: Optional[str] = None,
    type_tag: Optional[str] = None,
    q: Optional[str] = None
):
    """Retrieve catalog items filtered by manufacturer, domain, type_tag, or query."""
    return get_master_catalog().filter_items(
        manufacturer=manufacturer,
        domain=domain,
        type_tag=type_tag,
        query=q
    )


@app.get("/api/catalog/custom-breakers")
def api_get_all_custom_breakers():
    """Retrieve deduplicated list of uncataloged/custom breakers discovered across all facility schedules."""
    return db.get_custom_breakers()


@app.get("/api/clients/{client_id}/facilities/{facility_id}/custom-breakers")
def api_get_facility_custom_breakers(client_id: str, facility_id: str):
    """Retrieve custom breakers discovered in a specific client facility's panel schedules."""
    clean_c = client_id.strip().lower()
    clean_f = facility_id.strip().lower()
    return db.get_custom_breakers(client_id=clean_c, facility_id=clean_f)


@app.get("/api/catalog/items/{part_number}")
def api_get_catalog_item(part_number: str):
    """Retrieve single item specification by part number."""
    item = get_master_catalog().get_item(part_number)
    if not item:
        raise HTTPException(status_code=404, detail=f"Part number '{part_number}' not found in catalog")
    return item


@app.post("/api/catalog/items")
async def api_create_catalog_item(request: Request):
    """Create a new item in the Master Catalog and persist to manufacturer JSON."""
    data = await request.json()
    try:
        created = get_master_catalog().add_item(data)
        return {"status": "success", "item": created}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create catalog item: {e}")


@app.put("/api/catalog/items/{part_number}")
async def api_update_catalog_item(part_number: str, request: Request):
    """Update an existing catalog item and persist changes to disk."""
    data = await request.json()
    try:
        updated = get_master_catalog().update_item(part_number, data)
        return {"status": "success", "item": updated}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update catalog item: {e}")


@app.delete("/api/catalog/items/{part_number}")
def api_delete_catalog_item(part_number: str):
    """Delete an item from the Master Catalog and update disk."""
    deleted = get_master_catalog().delete_item(part_number)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Part '{part_number}' not found.")
    return {"status": "success", "message": f"Part '{part_number}' deleted."}


@app.post("/api/catalog/clone/{part_number}")
async def api_clone_catalog_item(part_number: str, request: Request):
    """Clone an existing catalog item with a new part number and optional overrides."""
    data = await request.json()
    new_pn = data.get("new_part_number")
    if not new_pn:
        raise HTTPException(status_code=400, detail="Missing 'new_part_number' in request payload.")

    overrides = data.get("overrides", {})
    try:
        cloned = get_master_catalog().clone_item(part_number, new_pn, overrides)
        return {"status": "success", "item": cloned}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clone catalog item: {e}")


# ==========================================
# ELECTRICAL INSPECTION CHECKLISTS ENDPOINTS
# ==========================================

@app.get("/api/checklists")
def api_get_all_checklists():
    """Returns all parsed inspection checklists from the master Excel workbook."""
    return get_all_checklists()


@app.get("/api/checklists/domain/{domain_id}")
def api_get_domain_checklists(domain_id: str, type_tag: Optional[str] = None):
    """Returns mapped checklists applicable for a specific equipment domain and type tag."""
    return get_checklists_for_domain(domain_id, type_tag or "")


@app.get("/api/checklists/{chk_id}")
def api_get_checklist_by_id(chk_id: str):
    """Returns a single checklist definition by its ID."""
    chk = get_checklist_by_id(chk_id)
    if not chk:
        raise HTTPException(status_code=404, detail=f"Checklist '{chk_id}' not found")
    return chk


@app.post("/api/checklists/reload")
def api_reload_checklists():
    """Forces dynamic reload and re-parsing of the master Excel workbook."""
    checklists = load_master_checklists(force_reload=True)
    return {
        "status": "success",
        "reloaded_count": len(checklists),
        "checklists": [c["id"] for c in checklists]
    }


@app.post("/api/catalog/import")
async def api_import_catalog_items(request: Request):
    """Bulk import items from JSON payload."""
    data = await request.json()
    items = data.get("items", [])
    if not isinstance(items, list):
        raise HTTPException(status_code=400, detail="'items' array is required.")

    overwrite = data.get("overwrite", True)
    result = get_master_catalog().import_items(items, overwrite=overwrite)
    return {"status": "success", "result": result}


@app.get("/api/catalog/export")
def api_export_catalog_items(
    domain: Optional[str] = None,
    manufacturer: Optional[str] = None,
    format: str = "json"
):
    """Export catalog items as JSON or CSV."""
    items = get_master_catalog().export_items(domain=domain, manufacturer=manufacturer)
    if format.lower() == "csv":
        import io
        import csv
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Part Number", "Manufacturer", "Series", "Domain", "Type Tag",
            "Type Name", "Description", "Voltage", "Amps", "AIC", "kVA", "Slots", "UPC"
        ])
        for it in items:
            sp = it.get("specs", {})
            dc = it.get("docs", {})
            writer.writerow([
                it.get("part_number", ""),
                it.get("manufacturer", ""),
                it.get("series", ""),
                it.get("domain", ""),
                it.get("type_tag", ""),
                it.get("type_name", ""),
                it.get("description", ""),
                sp.get("voltage", ""),
                sp.get("amps", ""),
                sp.get("aic", ""),
                sp.get("kva", ""),
                sp.get("total_slots", sp.get("slots", "")),
                dc.get("upc", "")
            ])
        return PlainTextResponse(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=master_catalog_export.csv"})
    
    return JSONResponse(content={"manufacturer": manufacturer or "All", "items": items})


@app.get("/api/catalog/search")
def api_search_catalog(q: str = "", limit: int = 100):
    """Search catalog items by query string."""
    return get_master_catalog().search(query=q, limit=limit)


@app.get("/projects/{project_id}", response_class=HTMLResponse)
def get_project_workspace(request: Request, project_id: str):
    """Render main application UI workspace for a project."""
    project = storage.load_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    catalog = get_catalog()
    return templates.TemplateResponse(
        request=request,
        name="base.html",
        context={
            "project": project,
            "catalog": catalog
        }
    )


@app.get("/api/catalog")
def api_get_catalog():
    """Return JSON Master Catalog schemas."""
    return get_catalog()


@app.get("/api/projects/{project_id}")
def api_get_project(project_id: str):
    """Return JSON project graph representation."""
    project = storage.load_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project.model_dump()


@app.get("/api/projects/{project_id}/dot", response_class=PlainTextResponse)
def api_get_project_dot(project_id: str):
    """Compile and return Graphviz DOT text representation of project."""
    project = storage.load_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return compile_project_to_dot(project)


@app.get("/api/projects/{project_id}/nodes/{node_id}/form", response_class=HTMLResponse)
def get_node_form(request: Request, project_id: str, node_id: str):
    """Return HTMX HTML dynamic attribute form snippet for a node."""
    project = storage.load_project(project_id)
    if not project or node_id not in project.nodes:
        raise HTTPException(status_code=404, detail="Node not found")
    
    node = project.nodes[node_id]
    schema = get_equipment_schema(node.type)
    
    return templates.TemplateResponse(
        request=request,
        name="components/node_form.html",
        context={
            "project_id": project_id,
            "node_id": node_id,
            "node": node,
            "schema": schema
        }
    )


@app.post("/api/projects/{project_id}/nodes/{node_id}", response_class=HTMLResponse)
async def update_node(request: Request, project_id: str, node_id: str):
    """Save updated node attributes and return updated form snippet with refresh trigger."""
    project = storage.load_project(project_id)
    if not project or node_id not in project.nodes:
        raise HTTPException(status_code=404, detail="Node not found")

    form_data = await request.form()
    node = project.nodes[node_id]

    if "label" in form_data:
        node.label = str(form_data["label"])

    # Update dynamic field data
    schema = get_equipment_schema(node.type)
    new_data = {}
    if schema and "fields" in schema:
        for field_key, field_meta in schema["fields"].items():
            input_name = f"field_{field_key}"
            if input_name in form_data:
                raw_val = form_data[input_name]
                if field_meta["type"] == "number" and raw_val != "":
                    try:
                        val = float(raw_val) if "." in str(raw_val) else int(raw_val)
                    except ValueError:
                        val = raw_val
                else:
                    val = raw_val
                new_data[field_key] = val

    node.data = new_data
    storage.save_project(project)

    response = templates.TemplateResponse(
        request=request,
        name="components/node_form.html",
        context={
            "project_id": project_id,
            "node_id": node_id,
            "node": node,
            "schema": schema
        }
    )
    response.headers["HX-Trigger"] = "refreshDiagram"
    return response


@app.delete("/api/projects/{project_id}/nodes/{node_id}", response_class=HTMLResponse)
def delete_node(project_id: str, node_id: str):
    """Delete a node and its attached edges from project graph."""
    project = storage.load_project(project_id)
    if not project or node_id not in project.nodes:
        raise HTTPException(status_code=404, detail="Node not found")

    del project.nodes[node_id]
    # Remove connected edges
    project.edges = [e for e in project.edges if e.from_node != node_id and e.to_node != node_id]
    storage.save_project(project)

    response = HTMLResponse(content='<div class="text-emerald-600 text-sm font-medium p-4 bg-emerald-50 rounded-lg">Equipment deleted successfully.</div>')
    response.headers["HX-Trigger"] = "refreshDiagram"
    return response


@app.post("/api/projects/{project_id}/nodes", response_class=HTMLResponse)
def add_node_from_catalog(request: Request, project_id: str, type_code: str):
    """Instantiate new equipment node from catalog into project."""
    project = storage.load_project(project_id)
    schema = get_equipment_schema(type_code)
    if not project or not schema:
        raise HTTPException(status_code=404, detail="Project or equipment schema not found")

    # Generate unique node ID
    base_id = f"{type_code}_{len(project.nodes) + 1}"
    node_id = base_id
    counter = 1
    while node_id in project.nodes:
        node_id = f"{base_id}_{counter}"
        counter += 1

    # Extract default field data from schema
    default_data = {}
    for field_key, field_meta in schema.get("fields", {}).items():
        if "default" in field_meta:
            default_data[field_key] = field_meta["default"]

    new_node = Node(
        type=type_code,
        label=f"{schema['symbol_code']}-{node_id}",
        data=default_data
    )
    project.nodes[node_id] = new_node
    storage.save_project(project)

    response = templates.TemplateResponse(
        request=request,
        name="components/node_form.html",
        context={
            "project_id": project_id,
            "node_id": node_id,
            "node": new_node,
            "schema": schema
        }
    )
    response.headers["HX-Trigger"] = "refreshDiagram"
    return response


@app.get("/api/projects/{project_id}/edges/{edge_id}/form", response_class=HTMLResponse)
def get_edge_form(request: Request, project_id: str, edge_id: str):
    """Return HTMX form snippet for an edge."""
    project = storage.load_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    edge = next((e for e in project.edges if e.id == edge_id), None)
    if not edge:
        raise HTTPException(status_code=404, detail="Edge not found")

    return templates.TemplateResponse(
        request=request,
        name="components/edge_form.html",
        context={
            "project_id": project_id,
            "edge": edge
        }
    )


@app.post("/api/projects/{project_id}/edges/{edge_id}", response_class=HTMLResponse)
async def update_edge(request: Request, project_id: str, edge_id: str):
    """Update edge feeder data and return updated form with refresh trigger."""
    project = storage.load_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    edge = next((e for e in project.edges if e.id == edge_id), None)
    if not edge:
        raise HTTPException(status_code=404, detail="Edge not found")

    form_data = await request.form()
    new_data = {}
    for key in ["breaker", "fuse", "cable", "length_ft"]:
        if key in form_data and form_data[key] != "":
            raw_val = form_data[key]
            if key == "length_ft":
                try:
                    val = float(raw_val) if "." in str(raw_val) else int(raw_val)
                except ValueError:
                    val = raw_val
            else:
                val = raw_val
            new_data[key] = val

    edge.data = new_data
    storage.save_project(project)

    response = templates.TemplateResponse(
        request=request,
        name="components/edge_form.html",
        context={
            "project_id": project_id,
            "edge": edge
        }
    )
    response.headers["HX-Trigger"] = "refreshDiagram"
    return response


@app.delete("/api/projects/{project_id}/edges/{edge_id}", response_class=HTMLResponse)
def delete_edge(project_id: str, edge_id: str):
    """Delete an edge connection from project graph."""
    project = storage.load_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.edges = [e for e in project.edges if e.id != edge_id]
    storage.save_project(project)

    response = HTMLResponse(content='<div class="text-emerald-600 text-sm font-medium p-4 bg-emerald-50 rounded-lg">Feeder connection deleted.</div>')
    response.headers["HX-Trigger"] = "refreshDiagram"
    return response


@app.post("/api/projects/{project_id}/edges", response_class=HTMLResponse)
def create_edge(
    request: Request,
    project_id: str,
    from_node: str = Form(...),
    from_port: str = Form(...),
    to_node: str = Form(...),
    to_port: str = Form(...),
    breaker: Optional[str] = Form(None)
):
    """Create new feeder edge connecting two node ports."""
    project = storage.load_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    edge_id = f"edge_{from_node.lower()}_{to_node.lower()}_{uuid.uuid4().hex[:4]}"
    edge_data = {}
    if breaker:
        edge_data["breaker"] = breaker

    new_edge = Edge(
        id=edge_id,
        from_node=from_node,
        from_port=from_port,
        to_node=to_node,
        to_port=to_port,
        data=edge_data
    )
    project.edges.append(new_edge)
    storage.save_project(project)

    response = templates.TemplateResponse(
        request=request,
        name="components/edge_form.html",
        context={
            "project_id": project_id,
            "edge": new_edge
        }
    )
    response.headers["HX-Trigger"] = "refreshDiagram"
    return response


# --- JEMBY Digital Twin: Focused Panel Endpoints ---
from james_app.panel_twin import (
    PanelTwin,
    SystemType,
    MainsType,
    BreakerStatus,
    DownstreamLoad,
    UpstreamFeed,
    create_empty_panel,
    add_breaker_to_panel
)
from james_app.panel_compiler import compile_panel_to_dot

PANEL_REGISTRY: dict[str, PanelTwin] = {}


def get_demo_panels():
    """Generate sample focused panel digital twin instances."""
    # 1. Empty 42-Space Panel
    empty_42 = create_empty_panel(
        panel_id="empty_42",
        name="MAIN DISTRIBUTION PANEL",
        total_spaces=42,
        mains_rating_amps=400,
        system_type=SystemType.THREE_PHASE_208Y_120V,
        mains_type=MainsType.MCB
    )

    # 2. Populated Demo Panel (1P, 2P, 3P with upstream feed and downstream loads)
    pop = create_empty_panel(
        panel_id="demo_populated",
        name="MAIN DISTRIBUTION PANEL",
        total_spaces=42,
        mains_rating_amps=400,
        system_type=SystemType.THREE_PHASE_208Y_120V,
        mains_type=MainsType.MCB
    )
    pop.upstream_feed = UpstreamFeed(
        source_id="Utility_Grid",
        name="Utility Grid",
        voltage_label="120/208V Main Service"
    )

    # Slot 1 & 2: 1-Pole Breakers
    add_breaker_to_panel(pop, slot_start=1, poles=1, amps=20, description="Lighting Cir 1")
    add_breaker_to_panel(pop, slot_start=2, poles=1, amps=20, description="Receptacles Lab")

    # Slot 3: 3-Pole Breaker (3, 5, 7) -> RTU-1
    add_breaker_to_panel(pop, slot_start=3, poles=3, amps=50, description="RTU-1 Rooftop Unit", target_load_id="rtu_1")
    pop.downstream_loads["rtu_1"] = DownstreamLoad(
        load_id="rtu_1",
        name="RTU-1 Rooftop Unit",
        rating_label="50A 208V 3-Phase",
        kva=15.0
    )

    # Slot 4: 1-Pole Breaker
    add_breaker_to_panel(pop, slot_start=4, poles=1, amps=20, description="Server Room Dedicated")

    # Slot 13: 2-Pole Breaker (13, 15) -> EV Charger
    add_breaker_to_panel(pop, slot_start=13, poles=2, amps=50, description="EV Level 2 Charger", target_load_id="ev_1")
    pop.downstream_loads["ev_1"] = DownstreamLoad(
        load_id="ev_1",
        name="EV Charging Station",
        rating_label="50A 208V 2-Pole",
        kva=10.4
    )

    # Slot 18: 2-Pole Breaker (18, 20) -> Water Heater
    add_breaker_to_panel(pop, slot_start=18, poles=2, amps=30, description="Water Heater", target_load_id="wh_1")
    pop.downstream_loads["wh_1"] = DownstreamLoad(
        load_id="wh_1",
        name="Commercial Water Heater",
        rating_label="30A 208V 2-Pole",
        kva=6.0
    )

    return {"empty_42": empty_42, "demo_populated": pop}


@app.get("/panels/{panel_id}", response_class=HTMLResponse)
def get_focused_panel_view(request: Request, panel_id: str):
    """Render Focused Panelboard Digital Twin workspace."""
    panels = get_demo_panels()
    panel = panels.get(panel_id)
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")

    return templates.TemplateResponse(
        request=request,
        name="panel_view.html",
        context={
            "panel": panel
        }
    )


@app.get("/api/panels/{panel_id}")
def api_get_panel_json(panel_id: str):
    """Return JSON Digital Twin payload for a panel."""
    panels = get_demo_panels()
    panel = panels.get(panel_id)
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")
    return panel.model_dump()


@app.get("/api/panels/{panel_id}/dot", response_class=PlainTextResponse)
def api_get_panel_dot(panel_id: str):
    """Return compiled Graphviz DOT string for focused panel view."""
    panels = get_demo_panels()
    panel = panels.get(panel_id)
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")
    return compile_panel_to_dot(panel)


@app.get("/equipment-selector", response_class=HTMLResponse)
def get_equipment_selector_view():
    """Serve interactive cascading equipment selector popup demo."""
    popup_path = Path(__file__).resolve().parent.parent / "docs" / "equipment_picker_popup.html"
    if popup_path.exists():
        return HTMLResponse(content=popup_path.read_text(encoding="utf-8"))
    raise HTTPException(status_code=404, detail="Popup template not found")


@app.get("/survey", response_class=HTMLResponse)
@app.get("/cockpit", response_class=HTMLResponse)
@app.get("/field-collector", response_class=HTMLResponse)
@app.get("/field-collector-htmx", response_class=HTMLResponse)
def get_survey_view(
    request: Request,
    client: Optional[str] = None,
    facility: Optional[str] = None,
    client_id: Optional[str] = None,
    facility_id: Optional[str] = None
):
    """Serve modern Jinja2 + HTML + SQLite + JSON + FastAPI + HTMX + Alpine.js + Tailwind Survey Workbench."""
    active_client = (client or client_id or "zoetis").strip().lower()
    active_facility = (facility or facility_id or "b4").strip().lower()

    # Ensure client facility SQLite DB is initialized/seeded if demo
    if active_client == "zoetis" and active_facility == "b4":
        db.seed_demo_facility(active_client, active_facility)
    else:
        db.get_engine(active_client, active_facility)

    with db.get_session(active_client, active_facility) as session:
        records = session.query(db.NodeRecord).order_by(db.NodeRecord.survey_sequence.asc()).all()
        initial_nodes = [
            {
                "id": r.id,
                "tag": r.tag,
                "name": r.name,
                "object_class": r.object_class,
                "domain": r.domain,
                "type_tag": r.type_tag,
                "type_name": r.type_name,
                "room": r.room,
                "fed_from": r.fed_from,
                "voltage": r.voltage,
                "amps": r.amps,
                "aic": r.aic,
                "is_panel": bool(r.is_panel),
                "slots": r.slots,
                "survey_sequence": r.survey_sequence,
                "status": r.status,
                "attributes": r.attributes,
            }
            for r in records
        ]

    return templates.TemplateResponse(
        request=request,
        name="survey.html",
        context={
            "client_id": active_client,
            "facility_id": active_facility,
            "initial_nodes": initial_nodes,
            "master_catalog_items": get_master_catalog().get_all_items(),
        }
    )


@app.get("/api/clients/{client_id}/facilities/{facility_id}/nodes")
def api_get_client_nodes(client_id: str, facility_id: str):
    """Retrieve all equipment nodes from client-isolated SQLite database."""
    clean_c = client_id.strip().lower()
    clean_f = facility_id.strip().lower()
    if clean_c == "zoetis" and clean_f == "b4":
        db.seed_demo_facility(clean_c, clean_f)
    else:
        db.get_engine(clean_c, clean_f)

    with db.get_session(clean_c, clean_f) as session:
        records = session.query(db.NodeRecord).order_by(db.NodeRecord.survey_sequence.asc()).all()
        nodes_list = [
            {
                "id": r.id,
                "tag": r.tag,
                "name": r.name,
                "object_class": r.object_class,
                "domain": r.domain,
                "type_tag": r.type_tag,
                "type_name": r.type_name,
                "room": r.room,
                "fed_from": r.fed_from,
                "voltage": r.voltage,
                "amps": r.amps,
                "aic": r.aic,
                "is_panel": bool(r.is_panel),
                "slots": r.slots,
                "survey_sequence": r.survey_sequence,
                "status": r.status,
                "attributes": r.attributes,
            }
            for r in records
        ]
        return JSONResponse(content=nodes_list, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})


def _safe_float(val, default: float = 0.0) -> float:
    if val is None or val == "":
        return default
    try:
        cleaned = re.sub(r"[^\d.]+", "", str(val))
        return float(cleaned) if cleaned else default
    except (ValueError, TypeError):
        return default


def _safe_int(val, default: int = 0) -> int:
    if val is None or val == "":
        return default
    try:
        cleaned = re.sub(r"[^\d]+", "", str(val))
        return int(cleaned) if cleaned else default
    except (ValueError, TypeError):
        return default


@app.post("/api/clients/{client_id}/facilities/{facility_id}/nodes")
async def api_upsert_client_node(request: Request, client_id: str, facility_id: str):
    """Upsert an equipment node into client SQLite database and sync companion JSONL."""
    data = await request.json()
    node_id = data.get("id") or f"s_{uuid.uuid4().hex[:8]}"
    tag = (data.get("tag") or "EQ-1").strip()

    with db.get_session(client_id, facility_id) as session:
        # Enforce unique equipment tags across the client facility
        duplicate = session.query(db.NodeRecord).filter(
            db.NodeRecord.tag.ilike(tag),
            db.NodeRecord.id != node_id
        ).first()
        if duplicate:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "error": "DUPLICATE_TAG",
                    "message": f"Equipment tag '{tag}' is already in use by '{duplicate.name}' ({duplicate.id}). Tags must be unique within a facility."
                }
            )

        node = session.query(db.NodeRecord).filter_by(id=node_id).first()
        if not node:
            count = session.query(db.NodeRecord).count()
            node = db.NodeRecord(
                id=node_id,
                tag=tag,
                name=data.get("name", "Equipment"),
                object_class=data.get("object_class", "GenericEquipmentObject"),
                domain=data.get("domain", "sources"),
                type_tag=data.get("type_tag", "GEN"),
                type_name=data.get("type_name", "Equipment"),
                room=data.get("room", "Main Electrical Room 101"),
                fed_from=data.get("fed_from"),
                voltage=data.get("voltage", "480Y/277V"),
                amps=_safe_float(data.get("amps"), 225.0),
                aic=_safe_float(data.get("aic"), 65.0),
                is_panel=1 if data.get("is_panel") else 0,
                slots=_safe_int(data.get("slots"), 42),
                survey_sequence=count + 1,
                status=data.get("status", "STAGED"),
                attributes=dict(data.get("attributes", {})),
            )
            session.add(node)
        else:
            node.tag = tag
            node.name = data.get("name", node.name)
            node.domain = data.get("domain", node.domain)
            node.type_tag = data.get("type_tag", node.type_tag)
            node.type_name = data.get("type_name", node.type_name)
            node.room = data.get("room", node.room)
            node.fed_from = data.get("fed_from")
            node.voltage = data.get("voltage", node.voltage)
            node.amps = _safe_float(data.get("amps"), node.amps if node.amps is not None else 225.0)
            node.aic = _safe_float(data.get("aic"), node.aic if node.aic is not None else 65.0)
            node.is_panel = 1 if data.get("is_panel") else 0
            node.slots = _safe_int(data.get("slots"), node.slots if node.slots is not None else 42)
            node.attributes = dict(data.get("attributes", {}))
            flag_modified(node, "attributes")
        session.commit()

    db.export_to_jsonl(client_id, facility_id)
    return {"status": "success", "id": node_id}


@app.delete("/api/clients/{client_id}/facilities/{facility_id}/nodes/{node_id}")
def api_delete_client_node(client_id: str, facility_id: str, node_id: str):
    """Delete an equipment node from client SQLite database and sync companion JSONL."""
    with db.get_session(client_id, facility_id) as session:
        node = session.query(db.NodeRecord).filter_by(id=node_id).first()
        if node:
            session.delete(node)
            session.commit()
    db.export_to_jsonl(client_id, facility_id)
    return {"status": "deleted", "id": node_id}


@app.get("/api/clients/{client_id}/facilities/{facility_id}/export/jsonl", response_class=PlainTextResponse)
def api_export_jsonl(client_id: str, facility_id: str):
    """Export and download companion JSONL representation of facility."""
    jsonl_path = db.export_to_jsonl(client_id, facility_id)
    return PlainTextResponse(content=jsonl_path.read_text(encoding="utf-8"), media_type="application/x-ndjson")


@app.get("/api/clients/{client_id}/facilities/{facility_id}/audit")
def api_get_facility_audit(client_id: str, facility_id: str):
    """Execute System Integrity Audit over facility equipment nodes and return scorecard."""
    clean_c = client_id.strip().lower()
    clean_f = facility_id.strip().lower()
    if clean_c == "zoetis" and clean_f == "b4":
        db.seed_demo_facility(clean_c, clean_f)
    else:
        db.get_engine(clean_c, clean_f)

    with db.get_session(clean_c, clean_f) as session:
        records = session.query(db.NodeRecord).order_by(db.NodeRecord.survey_sequence.asc()).all()
        node_dicts = [
            {
                "id": r.id,
                "tag": r.tag,
                "name": r.name,
                "object_class": r.object_class,
                "domain": r.domain,
                "type_tag": r.type_tag,
                "type_name": r.type_name,
                "room": r.room,
                "fed_from": r.fed_from,
                "voltage": r.voltage,
                "amps": r.amps,
                "aic": r.aic,
                "is_panel": bool(r.is_panel),
                "slots": r.slots,
                "survey_sequence": r.survey_sequence,
                "status": r.status,
                "attributes": r.attributes or {},
            }
            for r in records
        ]
        return audit_facility_system_integrity(node_dicts, client=clean_c, facility=clean_f)


@app.get("/api/clients/{client_id}/facilities/{facility_id}/audit/export")
def api_export_facility_audit(client_id: str, facility_id: str, format: str = "md", inline: bool = False):
    """Export System Integrity Audit in PDF, Markdown (with TOC), CSV, JSON, or Plain Text."""
    clean_c = client_id.strip().lower()
    clean_f = facility_id.strip().lower()
    if clean_c == "zoetis" and clean_f == "b4":
        db.seed_demo_facility(clean_c, clean_f)
    else:
        db.get_engine(clean_c, clean_f)

    with db.get_session(clean_c, clean_f) as session:
        records = session.query(db.NodeRecord).order_by(db.NodeRecord.survey_sequence.asc()).all()
        node_dicts = [
            {
                "id": r.id,
                "tag": r.tag,
                "name": r.name,
                "object_class": r.object_class,
                "domain": r.domain,
                "type_tag": r.type_tag,
                "type_name": r.type_name,
                "room": r.room,
                "fed_from": r.fed_from,
                "voltage": r.voltage,
                "amps": r.amps,
                "aic": r.aic,
                "is_panel": bool(r.is_panel),
                "slots": r.slots,
                "survey_sequence": r.survey_sequence,
                "status": r.status,
                "attributes": r.attributes or {},
            }
            for r in records
        ]
        audit_data = audit_facility_system_integrity(node_dicts, client=clean_c, facility=clean_f)

    fmt = format.strip().lower()
    filename_base = f"{clean_c}_{clean_f}_system_integrity_audit"

    if fmt == "pdf":
        pdf_bytes = generate_pdf_report(audit_data, client=clean_c, facility=clean_f)
        disp = "inline" if inline else "attachment"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'{disp}; filename="{filename_base}.pdf"'}
        )
    elif fmt == "csv":
        csv_content = generate_csv_report(audit_data)
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{filename_base}.csv"'}
        )
    elif fmt == "json":
        return JSONResponse(
            content=audit_data,
            headers={"Content-Disposition": f'attachment; filename="{filename_base}.json"'}
        )
    elif fmt == "txt":
        txt_content = generate_txt_report(audit_data, client=clean_c, facility=clean_f)
        return PlainTextResponse(
            content=txt_content,
            headers={"Content-Disposition": f'attachment; filename="{filename_base}.txt"'}
        )
    else:  # Default to Markdown with TOC (.md)
        md_content = generate_markdown_report(audit_data, client=clean_c, facility=clean_f)
        return PlainTextResponse(
            content=md_content,
            media_type="text/markdown; charset=utf-8",
            headers={"Content-Disposition": f'attachment; filename="{filename_base}.md"'}
        )


@app.get("/api/clients/{client_id}/facilities/{facility_id}/dot", response_class=PlainTextResponse)
def api_get_client_facility_dot(client_id: str, facility_id: str, mode: str = "macro"):
    """Compile and return Graphviz record-and-port DOT text representation of facility digital twin."""
    clean_c = client_id.strip().lower()
    clean_f = facility_id.strip().lower()
    if clean_c == "zoetis" and clean_f == "b4":
        db.seed_demo_facility(clean_c, clean_f)
    else:
        db.get_engine(clean_c, clean_f)

    with db.get_session(clean_c, clean_f) as session:
        records = session.query(db.NodeRecord).order_by(db.NodeRecord.survey_sequence.asc()).all()
        node_dicts = [
            {
                "id": r.id,
                "tag": r.tag,
                "name": r.name,
                "object_class": r.object_class,
                "domain": r.domain,
                "type_tag": r.type_tag,
                "type_name": r.type_name,
                "room": r.room,
                "fed_from": r.fed_from,
                "voltage": r.voltage,
                "amps": r.amps,
                "aic": r.aic,
                "is_panel": bool(r.is_panel),
                "slots": r.slots,
                "survey_sequence": r.survey_sequence,
                "status": r.status,
                "attributes": r.attributes or {},
            }
            for r in records
        ]
        dot_content = compile_facility_to_dot(node_dicts, mode=mode)
        return PlainTextResponse(content=dot_content, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})


@app.get("/clients/{client_id}/facilities/{facility_id}/sld", response_class=HTMLResponse)
def get_client_facility_sld(request: Request, client_id: str, facility_id: str):
    """Render the full interactive Graphviz record-and-port Single-Line Diagram view."""
    return templates.TemplateResponse(
        request=request,
        name="sld_view.html",
        context={
            "client_id": client_id,
            "facility_id": facility_id,
            "master_catalog_items": get_master_catalog().get_all_items(),
        }
    )


@app.get("/api/workspace/facilities")
def api_list_workspace_facilities():
    """List all client companies, facility folders, and their SQLite model.db statistics."""
    return db.list_all_client_facilities()


@app.post("/api/workspace/facilities")
async def api_create_workspace_facility(request: Request):
    """Create a new client company folder, facility folder, and initialize model.db."""
    try:
        data = await request.json()
    except Exception:
        data = {}
    client_id = str(data.get("client_id", "")).strip()
    facility_id = str(data.get("facility_id", "")).strip()
    seed = bool(data.get("seed", False))

    if not client_id or not facility_id:
        raise HTTPException(status_code=400, detail="client_id and facility_id are required.")

    result = db.create_client_facility(client_id, facility_id, seed=seed)
    return result


@app.delete("/api/workspace/facilities/{client_id}/{facility_id}")
def api_delete_workspace_facility(client_id: str, facility_id: str):
    """Delete a client facility folder and its SQLite model.db database."""
    clean_c = client_id.strip().lower()
    clean_f = facility_id.strip().lower()
    if clean_c == "zoetis" and clean_f == "b4":
        raise HTTPException(status_code=400, detail="Cannot delete default demo facility 'zoetis/b4'.")
    
    deleted = db.delete_client_facility(clean_c, clean_f)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Facility '{clean_f}' under client '{clean_c}' not found.")
    return {"status": "success", "message": f"Facility '{clean_f}' deleted successfully."}


# =============================================================================
# KNOWLEDGE BASE & FULL-TEXT SEARCH (FTS5) API
# =============================================================================

from james_app.knowledge_base import KnowledgeBaseManager
_kb_manager = None


def get_kb() -> KnowledgeBaseManager:
    global _kb_manager
    if _kb_manager is None:
        _kb_manager = KnowledgeBaseManager()
    return _kb_manager


@app.get("/api/kb/search")
def api_kb_search(
    q: str,
    category: Optional[str] = None,
    limit: int = 10
):
    """
    Full-Text Search against the Build Aware Knowledge Base with BM25 ranking and snippet highlighting.
    """
    query_str = (q or "").strip()
    if not query_str:
        return {"query": "", "count": 0, "results": []}

    kb = get_kb()
    results = kb.search(query=query_str, category=category, limit=limit)
    return {
        "query": query_str,
        "count": len(results),
        "results": results
    }


@app.get("/api/kb/stats")
def api_kb_stats():
    """Returns Knowledge Base indexing statistics."""
    kb = get_kb()
    return kb.get_stats()


@app.post("/api/kb/ingest/text")
async def api_kb_ingest_text(request: Request):
    """Ingest a single text document or FAQ chunk into the Knowledge Base."""
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    title = str(data.get("title", "")).strip()
    body_text = str(data.get("body_text", "")).strip()
    if not title or not body_text:
        raise HTTPException(status_code=400, detail="'title' and 'body_text' are required.")

    kb = get_kb()
    chunk_id = kb.ingest_chunk(
        source_file=data.get("source_file", "adhoc_faq.txt"),
        source_type=data.get("source_type", "faq"),
        category=data.get("category", "workflow"),
        title=title,
        section_heading=data.get("section_heading", "General"),
        body_text=body_text,
        tags=data.get("tags", ""),
        page_number=data.get("page_number")
    )
    return {"status": "success", "chunk_id": chunk_id, "message": f"Ingested chunk into KB with ID {chunk_id}."}


@app.post("/api/kb/ingest/file")
async def api_kb_ingest_file(
    file: UploadFile = File(...),
    category: Optional[str] = Form(None)
):
    """Upload and parse a document file (.md, .pdf, .html, .txt) into the Knowledge Base."""
    import tempfile
    ext = Path(file.filename).suffix.lower()
    if ext not in (".md", ".markdown", ".pdf", ".html", ".htm", ".txt", ".json"):
        raise HTTPException(status_code=400, detail=f"Unsupported file format '{ext}'. Supported: .md, .pdf, .html, .txt, .json")

    PROJECT_ROOT = BASE_DIR.parent
    kb_storage_dir = PROJECT_ROOT / "data" / "knowledge_base"
    kb_storage_dir.mkdir(parents=True, exist_ok=True)
    permanent_path = kb_storage_dir / file.filename

    with open(permanent_path, "wb") as f_perm:
        content = await file.read()
        f_perm.write(content)

    try:
        kb = get_kb()
        count = kb.ingest_file(str(permanent_path), category=category)
        with kb._get_connection() as con:
            con.execute("UPDATE kb_documents SET source_file = ? WHERE source_file = ?", (file.filename, permanent_path.name))
            con.commit()
    except Exception as e:
        logger.error(f"Failed to ingest uploaded KB file {file.filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process and index file: {str(e)}")

    return {
        "status": "success",
        "filename": file.filename,
        "chunks_indexed": count,
        "message": f"Successfully indexed {count} chunks from '{file.filename}' into Knowledge Base."
    }


@app.get("/api/kb/view/{filename:path}")
def api_kb_view_file(filename: str):
    """
    Serve knowledge base documents (PDFs, Markdown, HTML, text) inline for in-browser viewing.
    Browsers natively support deep-linking to specific PDF pages using the URL hash '#page=N'.
    """
    clean_name = os.path.basename(filename.strip())
    if not clean_name:
        raise HTTPException(status_code=400, detail="Invalid filename")

    PROJECT_ROOT = BASE_DIR.parent
    # Search potential source directories
    search_dirs = [
        PROJECT_ROOT / "faq",
        PROJECT_ROOT / "data" / "faq",
        PROJECT_ROOT / "data" / "knowledge_base",
        PROJECT_ROOT / "docs" / "faq",
        PROJECT_ROOT / "docs",
        PROJECT_ROOT,
        PROJECT_ROOT.parent,
        BASE_DIR / "static",
    ]

    target_path = None
    # 1. Direct candidates
    for s_dir in search_dirs:
        candidate = s_dir / clean_name
        if candidate.exists() and candidate.is_file():
            target_path = candidate
            break

    # 2. Recursive fallback for nested subfolders (e.g. faq/safety/...)
    if not target_path:
        for s_dir in search_dirs:
            if s_dir.exists() and s_dir.is_dir():
                found = list(s_dir.rglob(clean_name))
                if found and found[0].is_file():
                    target_path = found[0]
                    break

    if not target_path:
        raise HTTPException(
            status_code=404,
            detail=f"Document '{clean_name}' not found in Knowledge Base repository."
        )

    ext = target_path.suffix.lower()
    media_types = {
        ".pdf": "application/pdf",
        ".md": "text/plain; charset=utf-8",
        ".markdown": "text/plain; charset=utf-8",
        ".txt": "text/plain; charset=utf-8",
        ".html": "text/html; charset=utf-8",
        ".htm": "text/html; charset=utf-8",
        ".json": "application/json",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }
    media_type = media_types.get(ext, "application/octet-stream")

    return FileResponse(
        path=str(target_path),
        media_type=media_type,
        headers={
            "Content-Disposition": f'inline; filename="{clean_name}"',
            "Cache-Control": "public, max-age=3600",
        }
    )


@app.get("/kb/viewer/{filename:path}", response_class=HTMLResponse)
def kb_web_viewer(
    request: Request,
    filename: str,
    page: int = 1,
    title: Optional[str] = None,
    section: Optional[str] = None
):
    """
    Dedicated in-browser Web PDF Viewer powered by Mozilla PDF.js.
    Renders pure HTML5 Canvas in the browser tab, preventing external Adobe Acrobat desktop/plugin hijack.
    """
    clean_name = os.path.basename(filename.strip())
    return templates.TemplateResponse(
        request=request,
        name="pdf_viewer.html",
        context={
            "filename": clean_name,
            "initial_page": max(1, page),
            "title": title or clean_name,
            "section": section
        }
    )






