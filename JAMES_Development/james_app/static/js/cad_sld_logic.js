/**
 * Building Aware (JAMES) - CAD Single-Line Diagram Shared Logic
 * Provides in-browser interactive vector CAD preview, zoom/pan navigation,
 * multi-sheet drawing set switching, and direct IEEE AutoCAD DXF file downloads.
 */
(function() {
  window.CadSldModalLogic = {
    attachTo(app) {
      app.showCadModal = false;
      app.cadSvgContent = '';
      app.cadLoading = false;
      app.cadZoomScale = 1.0;
      app.cadPanX = 0;
      app.cadPanY = 0;
      app.isPanningCad = false;
      app.cadPanStartX = 0;
      app.cadPanStartY = 0;
      app.cadSheets = [];
      app.selectedCadSheet = 'all';

      app.openCadSldModal = async function() {
        this.showCadModal = true;
        this.cadZoomScale = 1.0;
        this.cadPanX = 0;
        this.cadPanY = 0;
        await this.loadCadSheets();
        await this.fetchCadSvg();
      };

      app.closeCadSldModal = function() {
        this.showCadModal = false;
      };

      app.loadCadSheets = async function() {
        try {
          const client = this.client || 'zoetis';
          const facility = this.facility || 'b4';
          const resp = await fetch(`/api/clients/${encodeURIComponent(client)}/facilities/${encodeURIComponent(facility)}/cad/sheets?t=${Date.now()}`);
          if (resp.ok) {
            this.cadSheets = await resp.json();
            if (!this.cadSheets.find(s => s.sheet_id === this.selectedCadSheet)) {
              this.selectedCadSheet = 'all';
            }
          }
        } catch (e) {
          console.warn('Could not load CAD sheet list:', e);
          this.cadSheets = [{ sheet_id: 'all', sheet_no: 'E-001', title: 'Overall Single-Line Diagram' }];
        }
      };

      app.onCadSheetChange = async function(sheetId) {
        this.selectedCadSheet = sheetId;
        this.cadZoomScale = 1.0;
        this.cadPanX = 0;
        this.cadPanY = 0;
        await this.fetchCadSvg();
      };

      app.fetchCadSvg = async function() {
        this.cadLoading = true;
        try {
          const client = this.client || 'zoetis';
          const facility = this.facility || 'b4';
          const sheet = this.selectedCadSheet || 'all';
          const resp = await fetch(`/api/clients/${encodeURIComponent(client)}/facilities/${encodeURIComponent(facility)}/cad/svg?sheet=${encodeURIComponent(sheet)}&t=${Date.now()}`);
          if (!resp.ok) throw new Error('Failed to compile CAD Single-Line Diagram');
          this.cadSvgContent = await resp.text();
        } catch (err) {
          console.error('Error loading CAD SVG:', err);
          this.cadSvgContent = `<div class="p-8 text-center text-rose-400 font-mono text-sm">Failed to generate CAD SLD preview: ${err.message}</div>`;
        } finally {
          this.cadLoading = false;
        }
      };

      app.downloadCadDxf = function() {
        const client = this.client || 'zoetis';
        const facility = this.facility || 'b4';
        const sheet = this.selectedCadSheet || 'all';
        window.location.href = `/api/clients/${encodeURIComponent(client)}/facilities/${encodeURIComponent(facility)}/cad/dxf?sheet=${encodeURIComponent(sheet)}`;
      };

      app.zoomInCad = function() {
        if (this.cadZoomScale < 4.0) this.cadZoomScale = Math.round((this.cadZoomScale + 0.2) * 10) / 10;
      };

      app.zoomOutCad = function() {
        if (this.cadZoomScale > 0.3) this.cadZoomScale = Math.round((this.cadZoomScale - 0.2) * 10) / 10;
      };

      app.resetCadZoom = function() {
        this.cadZoomScale = 1.0;
        this.cadPanX = 0;
        this.cadPanY = 0;
      };

      app.onCadWheel = function(e) {
        if (e.deltaY < 0) {
          this.zoomInCad();
        } else {
          this.zoomOutCad();
        }
      };

      app.startCadPan = function(e) {
        if (e.button !== 0) return; // Left click only
        this.isPanningCad = true;
        this.cadPanStartX = e.clientX - this.cadPanX;
        this.cadPanStartY = e.clientY - this.cadPanY;
      };

      app.doCadPan = function(e) {
        if (!this.isPanningCad) return;
        this.cadPanX = e.clientX - this.cadPanStartX;
        this.cadPanY = e.clientY - this.cadPanStartY;
      };

      app.endCadPan = function() {
        this.isPanningCad = false;
      };
    }
  };

  // Global helper functions
  window.openCadSldModal = function() {
    const appInstance = window.alpineApp || window.__sldAppInstance || window.__surveyAppInstance || window.__catalogAppInstance;
    if (appInstance && typeof appInstance.openCadSldModal === 'function') {
      appInstance.openCadSldModal();
    }
  };
})();
