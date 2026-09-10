/**
 * Building Aware - Shared Equipment Form & Electrical Hierarchy Logic
 * Reusable helper methods and computed getters for Survey Workbench and Single-Line Diagram (SLD).
 */
(function() {
  window.EquipmentFormSharedLogic = {
    // 10 Standard Digital Twin Domains
    domains: [
      { id: 'sources', name: 'Power Sources', icon: '⚡', color: 'indigo' },
      { id: 'transformers', name: 'Transformers', icon: '🔄', color: 'purple' },
      { id: 'switches', name: 'Switches & ATS', icon: '🔀', color: 'amber' },
      { id: 'panels', name: 'Panelboards & MCC', icon: '🗄️', color: 'sky' },
      { id: 'power_quality', name: 'Power Quality & UPS', icon: '🔋', color: 'emerald' },
      { id: 'loads', name: 'Electrical Loads', icon: '⚙️', color: 'rose' },
      { id: 'cables', name: 'Conductors & Feeders', icon: '🔌', color: 'teal' },
      { id: 'metering', name: 'Meters & Monitors', icon: '📊', color: 'blue' },
      { id: 'renewables', name: 'Solar & Renewables', icon: '☀️', color: 'yellow' },
      { id: 'generic', name: 'Generic / Unclassified', icon: '📦', color: 'slate' },
    ],

    // Complete Equipment Types Catalog across all 10 Domains
    typesCatalog: {
      sources: [
        { tag: 'UTIL', name: 'Utility Service Entrance', desc: 'Primary electric utility service termination', volts: '480Y/277V 3Ø 4W', amps: 2500, aic: 100, defaultTag: 'UTIL-1' },
        { tag: 'GEN', name: 'Emergency Diesel Generator', desc: 'On-site standby emergency generator', volts: '480Y/277V', amps: 1200, aic: 35, defaultTag: 'GEN-1' },
        { tag: 'PV', name: 'Solar PV Inverter', desc: 'Commercial solar photovoltaic inverter array', volts: '480V 3Ø', amps: 200, aic: 22, defaultTag: 'PV-1' },
      ],
      switches: [
        { tag: 'ATS', name: 'Automatic Transfer Switch (ATS)', desc: 'Automatic switching between Normal & Emergency sources', volts: '480Y/277V', amps: 400, aic: 65, defaultTag: 'ATS-1' },
        { tag: 'MTS', name: 'Manual Transfer Switch (MTS)', desc: 'Manual breaker/switch interlock transfer', volts: '480Y/277V', amps: 200, aic: 35, defaultTag: 'MTS-1' },
        { tag: 'DISC', name: 'Safety Disconnect Switch', desc: 'Heavy duty fused/non-fused disconnect', volts: '480V 3Ø', amps: 100, aic: 200, defaultTag: 'DS-1' },
      ],
      panels: [
        { tag: 'LP', name: 'Lighting Branch Panel (LP)', desc: '42-slot 208Y/120V lighting & receptacle panel', volts: '208Y/120V 3Ø 4W', amps: 225, aic: 22, is_panel: 1, defaultSlots: 42, defaultTag: 'LP-1' },
        { tag: 'MDP', name: 'Main Distribution Panel (MDP)', desc: 'Central service entrance switchboard / panel', volts: '480Y/277V 3Ø 4W', amps: 1200, aic: 65, is_panel: 1, defaultSlots: 42, defaultTag: 'MDP-1' },
        { tag: 'MCC', name: 'Motor Control Center (MCC)', desc: 'Grouped motor starters and VFD buckets', volts: '480V 3Ø 3W', amps: 800, aic: 65, is_panel: 1, defaultSlots: 30, defaultTag: 'MCC-1' },
        { tag: 'MSB', name: 'Main Switchboard (MSB)', desc: 'High-capacity distribution switchboard', volts: '480Y/277V 3Ø 4W', amps: 2500, aic: 100, is_panel: 1, defaultSlots: 60, defaultTag: 'MSB-1' },
        { tag: 'DP', name: 'Distribution Panelboard (DP)', desc: 'Intermediate power distribution feeder panel', volts: '480Y/277V 3Ø 4W', amps: 400, aic: 42, is_panel: 1, defaultSlots: 42, defaultTag: 'DP-1' },
        { tag: 'RP', name: 'Receptacle Branch Panel (RP)', desc: 'Appliance and convenience branch circuits', volts: '208Y/120V 3Ø 4W', amps: 100, aic: 14, is_panel: 1, defaultSlots: 30, defaultTag: 'RP-1' },
        { tag: 'SUB', name: 'Sub-Panelboard', desc: 'Remote floor or zone sub-panelboard', volts: '208Y/120V 3Ø 4W', amps: 125, aic: 10, is_panel: 1, defaultSlots: 24, defaultTag: 'SUB-1' },
      ],
      transformers: [
        { tag: 'XFMR-D', name: 'Dry-Type Step-Down Transformer', desc: 'General purpose 480V to 208Y/120V dry step-down', volts: '480V Pri / 208Y/120V Sec', amps: 208, aic: 14, defaultTag: 'T-1' },
        { tag: 'XFMR-O', name: 'Oil-Filled Padmount Transformer', desc: 'Utility outdoor oil-insulated substation unit', volts: '13.8kV Pri / 480V Sec', amps: 1200, aic: 65, defaultTag: 'TX-1' },
        { tag: 'XFMR-K', name: 'K-Factor Harmonic Transformer', desc: 'Harmonic mitigating K-13 rated transformer', volts: '480V Pri / 208Y/120V Sec', amps: 300, aic: 22, defaultTag: 'TK-1' },
      ],
      power_quality: [
        { tag: 'UPS', name: 'Uninterruptible Power Supply (UPS)', desc: 'Double-conversion online battery backup system', volts: '480V 3Ø', amps: 250, aic: 42, defaultTag: 'UPS-1' },
        { tag: 'TVSS', name: 'Surge Protective Device (SPD/TVSS)', desc: 'Transient voltage surge suppressor', volts: '480Y/277V', amps: 100, aic: 200, defaultTag: 'SPD-1' },
        { tag: 'PDU', name: 'Power Distribution Unit (PDU)', desc: 'Data center cabinet power distribution unit', volts: '208Y/120V', amps: 150, aic: 22, is_panel: 1, defaultSlots: 42, defaultTag: 'PDU-1' },
      ],
      loads: [
        { tag: 'CHLR', name: 'Water-Cooled Chiller', desc: 'Central mechanical plant centrifugal chiller', volts: '480V 3Ø', amps: 350, aic: 65, defaultTag: 'CH-1' },
        { tag: 'AHU', name: 'Air Handling Unit (AHU)', desc: 'HVAC supply and return fan system', volts: '480V 3Ø', amps: 45, aic: 22, defaultTag: 'AHU-1' },
        { tag: 'PUMP', name: 'Hydronic Circulating Pump', desc: 'Centrifugal motor pump assembly', volts: '480V 3Ø', amps: 30, aic: 22, defaultTag: 'P-1' },
        { tag: 'EVC', name: 'EV Fast Charger Station', desc: 'Commercial Level 3 DC Fast Charger', volts: '480V 3Ø', amps: 125, aic: 65, defaultTag: 'EV-1' },
      ],
      cables: [
        { tag: 'FEEDER', name: 'Conduit & Feeder Run', desc: 'Sub-distribution bus or THHN conduit raceway', volts: '480V 3Ø', amps: 400, aic: 65, defaultTag: 'FDR-1' },
        { tag: 'BUS', name: 'Electrical Busway Run', desc: 'Overhead plug-in bus duct run', volts: '480V 3Ø', amps: 800, aic: 65, defaultTag: 'BUS-1' },
      ],
      metering: [
        { tag: 'METER', name: 'Digital Power Meter', desc: 'Multi-function tenant revenue submeter', volts: '480V 3Ø', amps: 5, aic: 10, defaultTag: 'MTR-1' },
      ],
      renewables: [
        { tag: 'BESS', name: 'Battery Energy Storage System', desc: 'Utility scale grid-tied battery storage', volts: '480V 3Ø', amps: 400, aic: 65, defaultTag: 'BESS-1' },
      ],
      generic: [
        { tag: 'GENERIC', name: 'Unclassified Asset', desc: 'Custom facility asset or junction enclosure', volts: '480V', amps: 100, aic: 22, defaultTag: 'EQ-1' },
      ]
    },

    // Modal state defaults
    showEquipmentPicker: false,
    pickerSearch: '',
    pickerDomainFilter: 'all',

    // Inspection Checklists state
    activeDomainChecklists: [],
    selectedChecklistTab: null,
    checklistFilter: 'all', // 'all' | 'deficient' | 'pending' | 'pass'
    checklistLoading: false,
    checklistInspectorInput: '',

    async loadDomainChecklists(domainId, typeTag) {
      const d = (domainId || (this.form && this.form.domain) || 'panels').toLowerCase();
      const t = (typeTag || (this.form && this.form.type_tag) || '').toUpperCase();
      this.checklistLoading = true;
      try {
        const res = await fetch(`/api/checklists/domain/${encodeURIComponent(d)}?type_tag=${encodeURIComponent(t)}`);
        if (res.ok) {
          const data = await res.json();
          this.activeDomainChecklists = Array.isArray(data) ? data : [];
          if (this.activeDomainChecklists.length > 0) {
            if (!this.selectedChecklistTab || !this.activeDomainChecklists.some(c => c.id === this.selectedChecklistTab)) {
              this.selectedChecklistTab = this.activeDomainChecklists[0].id;
            }
          }
        }
      } catch (err) {
        console.error('Failed to load domain checklists:', err);
      } finally {
        this.checklistLoading = false;
      }
    },

    ensureChecklistsObject() {
      if (!this.form) return {};
      if (!this.form.checklists || typeof this.form.checklists !== 'object') {
        this.form.checklists = {};
      }
      return this.form.checklists;
    },

    getChecklistItemState(chkId, itemNo) {
      const root = this.ensureChecklistsObject();
      if (!root[chkId]) return { status: 'pending', notes: '', show_note: false };
      const item = root[chkId][itemNo] || root[chkId][String(itemNo)];
      if (!item) return { status: 'pending', notes: '', show_note: false };
      if (typeof item === 'string') return { status: item, notes: '', show_note: false };
      return {
        status: item.status || 'pending',
        notes: item.notes || '',
        show_note: !!item.show_note,
        timestamp: item.timestamp || ''
      };
    },

    setChecklistStatus(chkId, itemNo, status) {
      const root = this.ensureChecklistsObject();
      if (!root[chkId]) root[chkId] = {};
      const current = this.getChecklistItemState(chkId, itemNo);
      const newStatus = current.status === status ? 'pending' : status;
      root[chkId][itemNo] = {
        ...current,
        status: newStatus,
        show_note: (newStatus === 'deficient' || newStatus === 'fail') ? true : current.show_note,
        timestamp: new Date().toISOString()
      };
      if (this.form) {
        this.form.checklists = { ...root };
      }
    },

    setChecklistNotes(chkId, itemNo, notes) {
      const root = this.ensureChecklistsObject();
      if (!root[chkId]) root[chkId] = {};
      const current = this.getChecklistItemState(chkId, itemNo);
      root[chkId][itemNo] = {
        ...current,
        notes: notes,
        timestamp: new Date().toISOString()
      };
      if (this.form) {
        this.form.checklists = { ...root };
      }
    },

    toggleChecklistNote(chkId, itemNo) {
      const root = this.ensureChecklistsObject();
      if (!root[chkId]) root[chkId] = {};
      const current = this.getChecklistItemState(chkId, itemNo);
      root[chkId][itemNo] = {
        ...current,
        show_note: !current.show_note
      };
      if (this.form) {
        this.form.checklists = { ...root };
      }
    },

    appendChecklistPresetNote(chkId, itemNo, preset) {
      const current = this.getChecklistItemState(chkId, itemNo);
      let updated = (current.notes || '').trim();
      if (updated) {
        if (!updated.includes(preset)) {
          updated = `${updated}; ${preset}`;
        }
      } else {
        updated = preset;
      }
      this.setChecklistNotes(chkId, itemNo, updated);
    },

    markAllChecklist(chkId, status) {
      const chk = (this.activeDomainChecklists || []).find(c => c.id === chkId);
      if (!chk || !chk.items) return;
      const root = this.ensureChecklistsObject();
      if (!root[chkId]) root[chkId] = {};
      chk.items.forEach(item => {
        const itemNo = item.item_no;
        const current = this.getChecklistItemState(chkId, itemNo);
        root[chkId][itemNo] = {
          ...current,
          status: status,
          timestamp: new Date().toISOString()
        };
      });
      if (this.form) {
        this.form.checklists = { ...root };
      }
    },

    getChecklistStats(chkId) {
      const chk = (this.activeDomainChecklists || []).find(c => c.id === chkId);
      if (!chk || !chk.items) return { total: 0, passed: 0, deficient: 0, na: 0, pending: 0, pct: 0, isComplete: false };
      let passed = 0, deficient = 0, na = 0, pending = 0;
      chk.items.forEach(item => {
        const state = this.getChecklistItemState(chkId, item.item_no);
        if (state.status === 'pass') passed++;
        else if (state.status === 'deficient' || state.status === 'fail') deficient++;
        else if (state.status === 'na') na++;
        else pending++;
      });
      const total = chk.items.length;
      const evaluated = passed + deficient + na;
      const pct = total > 0 ? Math.round((evaluated / total) * 100) : 0;
      return { total, passed, deficient, na, pending, pct, isComplete: (total > 0 && evaluated === total) };
    },

    getOverallChecklistStats() {
      const list = this.activeDomainChecklists || [];
      let total = 0, passed = 0, deficient = 0, na = 0, pending = 0;
      list.forEach(chk => {
        const s = this.getChecklistStats(chk.id);
        total += s.total;
        passed += s.passed;
        deficient += s.deficient;
        na += s.na;
        pending += s.pending;
      });
      const evaluated = passed + deficient + na;
      const pct = total > 0 ? Math.round((evaluated / total) * 100) : 0;
      const isComplete = total > 0 && evaluated === total;
      const status = !isComplete ? 'incomplete' : (deficient > 0 ? 'deficient' : 'compliant');
      return { total, passed, deficient, na, pending, pct, isComplete, status };
    },

    normalizeScheduleRows(rawSchedule, slotCount = 42) {
      const slots = Number(slotCount) || 42;
      const phases = ['A', 'B', 'C'];
      const phaseColors = ['text-red-500 font-bold', 'text-blue-500 font-bold', 'text-emerald-500 font-bold'];
      const rawList = Array.isArray(rawSchedule) ? rawSchedule : [];
      const rawMap = {};
      rawList.forEach(r => {
        if (r && r.leftSlot) {
          rawMap[r.leftSlot] = r;
        }
      });

      const normalized = [];
      for (let i = 1; i <= slots; i += 2) {
        const phaseIdx = Math.floor((i - 1) / 2) % 3;
        const existing = rawMap[i] || {};
        normalized.push({
          leftSlot: i,
          leftDesc: existing.leftDesc || '',
          leftTrip: existing.leftTrip || '',
          leftPoles: existing.leftPoles || 1,
          leftType: existing.leftType || 'MCCB',
          leftWire: existing.leftWire || '12 AWG Cu',
          leftTargetLoad: existing.leftTargetLoad || '',
          leftParentSlot: existing.leftParentSlot !== undefined ? existing.leftParentSlot : null,
          leftIsGanged: !!existing.leftIsGanged,
          rightSlot: existing.rightSlot || (i + 1),
          rightDesc: existing.rightDesc || '',
          rightTrip: existing.rightTrip || '',
          rightPoles: existing.rightPoles || 1,
          rightType: existing.rightType || 'MCCB',
          rightWire: existing.rightWire || '12 AWG Cu',
          rightTargetLoad: existing.rightTargetLoad || '',
          rightParentSlot: existing.rightParentSlot !== undefined ? existing.rightParentSlot : null,
          rightIsGanged: !!existing.rightIsGanged,
          ...existing,
          leftSlot: i,
          rightSlot: i + 1,
          phase: phases[phaseIdx],
          phaseColor: phaseColors[phaseIdx]
        });
      }
      return normalized;
    },

    getChecklistSignoff() {
      if (!this.form) return null;
      if (this.form.checklist_signoff && typeof this.form.checklist_signoff === 'object') {
        return this.form.checklist_signoff;
      }
      return null;
    },

    signOffChecklist(inspectorName) {
      if (!this.form) return;
      const stats = this.getOverallChecklistStats();
      const inspector = (inspectorName || this.checklistInspectorInput || 'Field Inspector').trim();
      const signoffData = {
        inspector: inspector,
        timestamp: new Date().toISOString(),
        status: stats.deficient > 0 ? 'Deficiencies Found' : 'Compliant',
        is_complete: stats.isComplete,
        passed_items: stats.passed,
        deficient_items: stats.deficient,
        total_items: stats.total,
        compliance_pct: stats.pct
      };
      this.form.checklist_signoff = signoffData;
      if (typeof this.toast === 'function') {
        this.toast(`✅ Inspection signed off by ${inspector} (${signoffData.status})`);
      }
    },

    clearChecklistSignoff() {
      if (!this.form) return;
      this.form.checklist_signoff = null;
      if (typeof this.toast === 'function') {
        this.toast('Sign-off cleared.');
      }
    },

    /**
     * Universal node pool accessor across Survey, SLD, and Standalone modes.
     */
    getNodePool() {
      if (Array.isArray(this.stack) && this.stack.length > 0) return this.stack;
      if (Array.isArray(this.allNodes) && this.allNodes.length > 0) return this.allNodes;
      if (Array.isArray(window.facilityNodes) && window.facilityNodes.length > 0) return window.facilityNodes;
      return [];
    },

    /**
     * Check if current equipment is panel equipment (panelboard, switchboard, distribution).
     */
    isPanelEquipment() {
      if (this.form) {
        if (this.form.is_panel) return true;
        const d = (this.form.domain || '').toLowerCase();
        if (d === 'panels') return true;
      }
      if (this.editingNode) {
        if (this.editingNode.is_panel) return true;
        const d = (this.editingNode.domain || '').toLowerCase();
        if (d === 'panels') return true;
      }
      return false;
    },

    /**
     * Check if current equipment is dual-source (ATS, MTS, STS).
     */
    isDualSourceEquipment() {
      const typeTag = (this.form && (this.form.type_tag || this.form.type_code || '')) || (this.selectedType ? this.selectedType.tag : '');
      const typeName = (this.form && (this.form.type_name || this.form.name || '')) || (this.selectedType ? this.selectedType.name : '');
      const domain = (this.form && this.form.domain) || (this.selectedDomain ? this.selectedDomain.id : '');
      const combined = `${typeTag} ${typeName} ${domain}`.toUpperCase();
      return combined.includes('ATS') || combined.includes('MTS') || combined.includes('STS') || combined.includes('TRANSFER SWITCH') || combined.includes('DUAL');
    },

    /**
     * Determine label for primary vs secondary/alternate feeds.
     */
    getSourceLabel(sIdx) {
      if (this.isDualSourceEquipment()) {
        return sIdx === 0 ? 'Normal Power Source' : (sIdx === 1 ? 'Emergency Power Source' : `Alternate Source #${sIdx + 1}`);
      }
      return sIdx === 0 ? 'Primary Upstream Feed' : `Secondary Feed #${sIdx + 1}`;
    },

    /**
     * Add new upstream source slot.
     */
    addUpstreamSource() {
      if (!this.form) return;
      const sources = Array.isArray(this.form.upstream_sources) ? [...this.form.upstream_sources] : [''];
      sources.push('');
      this.form.upstream_sources = sources;
    },

    /**
     * Remove upstream source slot.
     */
    removeUpstreamSource(sIdx) {
      if (!this.form || !Array.isArray(this.form.upstream_sources)) return;
      const sources = [...this.form.upstream_sources];
      sources.splice(sIdx, 1);
      if (sources.length === 0) {
        sources.push('');
      }
      this.form.upstream_sources = sources;
      this.form.fed_from = sources[0] || '';
    },

    /**
     * Handle upstream source change event.
     */
    onUpstreamSourceChange(sIdx, val) {
      if (!this.form) return;
      const cleanVal = val ? String(val).trim() : '';
      const sources = Array.isArray(this.form.upstream_sources) ? [...this.form.upstream_sources] : [''];
      while (sources.length <= sIdx) {
        sources.push('');
      }
      sources[sIdx] = cleanVal;
      this.form.upstream_sources = sources;
      if (sIdx === 0) {
        this.form.fed_from = cleanVal;
      }
    },

    /**
     * Conductor sizing lookup by continuous ampacity.
     */
    getConductor(amps) {
      const a = Number(amps) || 0;
      if (a <= 20) return '12 AWG Cu';
      if (a <= 30) return '10 AWG Cu';
      if (a <= 60) return '4 AWG Cu';
      if (a <= 100) return '3 AWG Cu';
      if (a <= 225) return '4/0 AWG Cu';
      if (a <= 400) return '500 kcmil Cu';
      if (a <= 800) return '2x 500 kcmil Cu';
      return '4x 500 kcmil Cu';
    },

    /**
     * Auto-increments a tag prefix based on existing items in the facility node pool.
     */
    generateNextTag(defaultTagPrefix) {
      const pool = this.getNodePool();
      const basePrefix = (defaultTagPrefix || 'EQ').split('-')[0];
      let maxNum = 0;
      const regex = new RegExp(`^${basePrefix}-(\\d+)$`, 'i');
      pool.forEach(item => {
        if (!item || !item.tag) return;
        const match = String(item.tag).trim().match(regex);
        if (match) {
          const num = parseInt(match[1], 10);
          if (num > maxNum) maxNum = num;
        }
      });
      return `${basePrefix}-${maxNum + 1}`;
    },

    /**
     * Open Equipment Picker Modal.
     */
    openEquipmentPicker() {
      this.pickerSearch = '';
      this.pickerDomainFilter = 'all';
      this.showEquipmentPicker = true;
    },

    /**
     * Close Equipment Picker Modal.
     */
    closeEquipmentPicker() {
      this.showEquipmentPicker = false;
      this.pickerSearch = '';
    },

    /**
     * Computes filtered archetypes for the Equipment Picker Modal.
     */
    get filteredPickerItems() {
      const q = (this.pickerSearch || '').trim().toLowerCase();
      const selectedDom = this.pickerDomainFilter || 'all';
      const results = [];
      const domainsList = this.domains || [];

      domainsList.forEach(dom => {
        if (selectedDom !== 'all' && dom.id !== selectedDom) return;
        const types = (this.typesCatalog && this.typesCatalog[dom.id]) || [];
        types.forEach(t => {
          if (!q) {
            results.push({ ...t, domainId: dom.id, domainName: dom.name, domainIcon: dom.icon, domainColor: dom.color });
          } else {
            const matches = (
              t.tag.toLowerCase().includes(q) ||
              t.name.toLowerCase().includes(q) ||
              (t.desc && t.desc.toLowerCase().includes(q)) ||
              dom.name.toLowerCase().includes(q)
            );
            if (matches) {
              results.push({ ...t, domainId: dom.id, domainName: dom.name, domainIcon: dom.icon, domainColor: dom.color });
            }
          }
        });
      });

      return results;
    },

    /**
     * Computes eligible upstream equipment with cycle prevention & domain hierarchy.
     */
    get eligibleUpstreamEquipment() {
      const pool = (typeof this.getNodePool === 'function') ? this.getNodePool() : (this.stack || this.allNodes || window.facilityNodes || []);
      const currentDomain = (this.form && this.form.domain) || (this.selectedDomain ? this.selectedDomain.id : '');

      // Primary sources (Utility, Generator, Solar PV) don't have upstream feeders
      if (currentDomain === 'sources') {
        return [];
      }

      // Collect all downstream descendant tags if editing to prevent electrical cycles
      const descendantTags = new Set();
      if (this.form && this.form.tag) {
        const findDescendants = (parentTag) => {
          const pUpper = String(parentTag).trim().toUpperCase();
          pool.forEach(item => {
            if (!item) return;
            const rawAttrs = item.attributes || {};
            const itemSources = [];
            if (item.fed_from) itemSources.push(item.fed_from);
            if (rawAttrs.emergency_source) itemSources.push(rawAttrs.emergency_source);
            if (rawAttrs.upstream_sources && Array.isArray(rawAttrs.upstream_sources)) {
              rawAttrs.upstream_sources.forEach(s => s && itemSources.push(s));
            }
            const isFed = itemSources.some(s => s && String(s).trim().toUpperCase() === pUpper);
            if (isFed && item.tag) {
              if (!descendantTags.has(item.tag)) {
                descendantTags.add(item.tag);
                findDescendants(item.tag);
              }
            }
          });
        };
        findDescendants(this.form.tag);
      }

      return pool.filter(item => {
        if (!item) return false;
        // 1. Exclude self
        if (this.editingId && item.id === this.editingId) return false;
        if (this.form && this.form.tag && item.tag && String(item.tag).trim().toUpperCase() === String(this.form.tag).trim().toUpperCase()) return false;

        // 2. Exclude downstream descendants (cycle prevention)
        if (item.tag && descendantTags.has(item.tag)) return false;

        // 3. Exclude terminal loads and meters - loads can never feed anything upstream
        if (item.domain === 'loads') return false;
        if (item.type_tag === 'METER') return false;

        // 4. Domain-specific physical upstream rules:
        if (currentDomain === 'switches') {
          return ['sources', 'transformers', 'panels', 'power_quality', 'switches'].includes(item.domain);
        }
        if (currentDomain === 'transformers') {
          return ['sources', 'switches', 'panels', 'transformers', 'power_quality'].includes(item.domain);
        }
        if (currentDomain === 'panels') {
          return ['sources', 'switches', 'transformers', 'panels', 'power_quality'].includes(item.domain);
        }
        if (currentDomain === 'power_quality') {
          return ['sources', 'switches', 'transformers', 'panels'].includes(item.domain);
        }
        if (currentDomain === 'loads') {
          return ['panels', 'transformers', 'switches', 'power_quality', 'sources'].includes(item.domain);
        }
        return true;
      });
    },

    /**
     * Computes eligible downstream equipment with back-feeding ancestor exclusion.
     */
    get eligibleDownstreamEquipment() {
      const pool = (typeof this.getNodePool === 'function') ? this.getNodePool() : (this.stack || this.allNodes || window.facilityNodes || []);
      const hostPanelTag = (this.form && this.form.tag) ? String(this.form.tag).trim().toUpperCase() : '';
      const hostPanelId = (this.editingId || (this.form && this.form.id)) || '';

      // Collect all upstream feeding ancestor tags of this panel to prevent back-feeding cycles
      const ancestorTags = new Set();
      let currentParentTag = (this.form && this.form.fed_from) ? this.form.fed_from : null;
      while (currentParentTag) {
        const parentTagUpper = String(currentParentTag).trim().toUpperCase();
        ancestorTags.add(parentTagUpper);
        const parentItem = pool.find(i => i && i.tag && String(i.tag).trim().toUpperCase() === parentTagUpper);
        currentParentTag = (parentItem && parentItem.fed_from) ? parentItem.fed_from : null;
        if (ancestorTags.has(currentParentTag ? String(currentParentTag).trim().toUpperCase() : '')) break; // prevent infinite loop
      }

      return pool.filter(item => {
        if (!item) return false;
        // 1. Exclude self
        if (item.id === hostPanelId) return false;
        if (item.tag && String(item.tag).trim().toUpperCase() === hostPanelTag) return false;

        // 2. Exclude upstream feeding ancestors
        if (item.tag && ancestorTags.has(String(item.tag).trim().toUpperCase())) return false;

        // 3. Exclude primary utility grid entrances and generators
        if (item.domain === 'sources' && (item.type_tag === 'UTIL' || item.type_tag === 'GEN')) return false;

        return true;
      });
    },

    /**
     * Compute list of child items claiming this panel as upstream feed that are not yet placed in a slot.
     */
    get unresolvedLoads() {
      if (!this.form || !this.form.tag) return [];
      const isPanel = (typeof this.isPanelEquipment === 'function') ? this.isPanelEquipment() : (this.form.is_panel || this.form.domain === 'panels');
      if (!isPanel) return [];

      const panelTag = String(this.form.tag || '').trim().toLowerCase();
      const panelId = String(this.editingId || (this.form && this.form.id) || '').trim().toLowerCase();
      const pool = (typeof this.getNodePool === 'function') ? this.getNodePool() : (this.stack || this.allNodes || []);

      const claimedChildren = pool.filter(item => {
        if (!item || !item.tag || item.id === panelId || String(item.tag).toLowerCase() === panelTag) return false;
        const fedFrom = String(item.fed_from || '').trim().toLowerCase();
        const upstreamSources = (item.attributes && item.attributes.upstream_sources)
          ? item.attributes.upstream_sources.map(s => String(s).trim().toLowerCase())
          : [];
        return fedFrom === panelTag || fedFrom === panelId || upstreamSources.includes(panelTag) || upstreamSources.includes(panelId);
      });

      const schedule = this.scheduleRows || [];
      const assignedTags = new Set();

      schedule.forEach(r => {
        if (!r) return;
        const lt = String(r.leftTargetLoad || '').trim().toLowerCase();
        const rt = String(r.rightTargetLoad || '').trim().toLowerCase();
        const ld = String(r.leftDesc || '').trim().toLowerCase();
        const rd = String(r.rightDesc || '').trim().toLowerCase();

        if (lt) assignedTags.add(lt);
        if (rt) assignedTags.add(rt);

        claimedChildren.forEach(child => {
          const cTag = String(child.tag || '').trim().toLowerCase();
          if (cTag && (lt === cTag || rt === cTag || (ld && ld.includes(cTag)) || (rd && rd.includes(cTag)))) {
            assignedTags.add(cTag);
          }
        });
      });

      return claimedChildren.filter(child => {
        const cTag = String(child.tag || '').trim().toLowerCase();
        const cId = String(child.id || '').trim().toLowerCase();
        return !assignedTags.has(cTag) && !assignedTags.has(cId);
      });
    },

    // Searchable FAQs & Field Knowledge Base Dataset
    faqItems: [
      {
        id: 'add_device',
        category: 'assets',
        categoryName: 'Assets & Hierarchy',
        icon: '⚡',
        question: 'How do I add a new electrical device, panel, or transformer?',
        summary: 'Create a physical asset in the facility digital twin and connect it into the power distribution tree.',
        tags: ['add', 'device', 'equipment', 'asset', 'panel', 'transformer', 'switchboard', 'new', 'create'],
        steps: [
          'Click the "+ Add Equipment" button in the table toolbar (Survey) or DOMAINS palette (Diagram), or press hotkey (N).',
          'Select an Equipment Archetype (e.g., Panelboard, Switchboard, Dry-Type Transformer, Generator) or pick a template from the Catalog.',
          'Enter the unique Equipment Tag (e.g., MDP-1, T-1, LP-A), Equipment Name, and physical Location (Floor, Room).',
          'Set the "Fed From / Upstream Source" dropdown to link it to its parent power source.',
          'Click "💾 Save Equipment" to record it into your facility model.'
        ],
        action: { label: '+ Add New Equipment', key: 'new_asset' }
      },
      {
        id: 'add_breaker',
        category: 'breakers',
        categoryName: 'Breakers & Panels',
        icon: '🗄️',
        question: 'How do I add a circuit breaker to a panelboard or switchboard?',
        summary: 'Configure circuit breaker poles, trip ratings, catalog models, and downstream load descriptions in the panel schedule.',
        tags: ['breaker', 'add breaker', 'schedule', 'poles', '1p', '2p', '3p', 'trip rating', 'catalog', 'circuit'],
        steps: [
          'Open the target Panelboard or Switchboard in the equipment editor drawer.',
          'Scroll to the "Panel Schedule & Feeder Configuration" section and click any pole space.',
          'Select the Pole configuration (1-Pole, 2-Pole, or 3-Pole) in the segmented top selector.',
          'Enter the Trip Amperage (e.g., 20A, 100A, 225A) or choose a verified OEM model from the Master Catalog dropdown.',
          'Select the downstream connected asset (or enter a branch circuit description like "HVAC Chiller-1").',
          'Click "Save Breaker" to append it to the panel schedule.'
        ]
      },
      {
        id: 'unresolved_loads',
        category: 'connected_loads',
        categoryName: 'Connected Loads',
        icon: '⚠️',
        question: 'What is an "Unresolved Connected Load" and how do I resolve it?',
        summary: 'Downstream equipment referencing this panel as its upstream feed that has not yet been assigned a specific breaker slot.',
        tags: ['unresolved', 'connected loads', 'uplink', 'downstream', 'resolve', 'fed from', 'assign breaker', 'missing breaker'],
        steps: [
          'When another equipment item lists this panel in its "Fed From" field, JAMES tracks the upstream electrical connection.',
          'If no breaker slot in the panel schedule currently points to that downstream asset, an amber "⚠️ Unresolved Connected Loads" card appears above the schedule.',
          'Click the "Resolve" button next to the unassigned load.',
          'The Breaker Inspector opens with the downstream load pre-selected and recommended 3-Pole / trip ratings pre-filled.',
          'Review and tap "Save Breaker" to permanently link the breaker slot to the downstream equipment.'
        ]
      },
      {
        id: 'upstream_feed',
        category: 'assets',
        categoryName: 'Assets & Hierarchy',
        icon: '🔌',
        question: 'How do I connect equipment upstream (Fed From) to build the power tree?',
        summary: 'Establish digital twin parent-child hierarchy from the utility service entrance down to branch panels.',
        tags: ['fed from', 'upstream', 'parent', 'hierarchy', 'source', 'service entrance', 'utility', 'feed'],
        steps: [
          'In the equipment editor drawer, locate the "Electrical Ratings & Supply" section.',
          'Open the "Fed From / Upstream Source" dropdown list.',
          'Select the feeding panel, switchboard, or transformer that supplies power to this equipment.',
          'For the primary utility connection (e.g. MSB or Utility Service), select "Main Service / Utility Feed".',
          'JAMES automatically draws connected topology lines on the Single-Line Diagram (SLD) based on these feeds.'
        ]
      },
      {
        id: 'system_integrity_audit',
        category: 'assets',
        categoryName: 'System Integrity & Audit',
        icon: '🛡️',
        question: 'How does the System Integrity Audit check voltage, AIC, and capacity headroom?',
        summary: 'Run automated NEC and IEEE engineering rule checks across the entire facility distribution topology and generate PDF/Markdown reports.',
        tags: ['audit', 'integrity', 'health score', 'nec', 'ieee', 'voltage', 'aic', 'capacity', 'overload', 'export', 'pdf', 'print'],
        steps: [
          'Open the Toolbox (🧰) in the top header and click "Run Integrity Audit" on the hero tile.',
          'The engine deterministically checks voltage class continuity (flagging unstepped 480V→208V drops), upstream breaker headroom vs downstream loads, and low-AIC withstand ratings.',
          'View the live Health Score (0-100) and categorized Critical, Warning, and Info findings.',
          'Click "Inspect Asset ↗" on any finding to jump directly into the equipment drawer for instant correction.',
          'Click "🖨️ Print / PDF" to generate a publication-ready PDF report with cover page, health scorecard, and executive findings.',
          'Or download reports as Markdown with Table of Contents, Excel CSV, or companion JSONL.'
        ],
        action: { label: '🛡️ Run Integrity Audit', key: 'open_audit' }
      },
      {
        id: 'inspection_checklists',
        category: 'assets',
        categoryName: 'Checklists & Inspections',
        icon: '📋',
        question: 'How do I perform equipment inspection checklists and record deficiencies?',
        summary: 'Execute domain-specific NEC, NFPA, and IEEE inspection items with one-tap status toggling, auto-revealed deficiency notes, preset defect chips, and field sign-offs.',
        tags: ['checklist', 'inspection', 'deficient', 'deficiency', 'pass', 'signoff', 'notes', 'chips', 'preset', 'nec', 'nfpa'],
        steps: [
          'Open any equipment in the Survey or SLD drawer and navigate to the "Inspection Checklists" tab.',
          'Applicable checklists for the equipment domain and archetype load dynamically (e.g. Visual Inspection, NEC Clearance, Arc Flash, Conductor Torquing).',
          'Tap "Pass", "Deficient", or "N/A" on each item. Marking an item as "Deficient" automatically expands the deficiency notes field.',
          'Tap one-click preset chips (e.g., "+ Label Missing", "+ Torque Unverified", "+ Clearance < 36\"", "+ Missing Filler Plate", "+ Arc Flash Expired") or type custom field observations.',
          'Filter by "All", "Deficient", "Pending", or "Passed" to quickly track remaining work.',
          'Review the live Compliance Percentage meter and enter the Inspector name to sign off the inspection.'
        ]
      },
      {
        id: 'nameplate_photos',
        category: 'photos',
        categoryName: 'Photos & Notes',
        icon: '📷',
        question: 'How do I capture nameplate photos and attach field observation notes?',
        summary: 'Attach high-resolution physical nameplate photos and notes for engineering verification.',
        tags: ['photo', 'camera', 'nameplate', 'notes', 'observation', 'upload', 'ipad', 'lightbox', 'field'],
        steps: [
          'In the equipment editor drawer, select the "Photos & Field Notes" tab.',
          'Tap "📷 Take Photo / Upload" to take a picture with your mobile device or select an existing photo file.',
          'Add field notes in the text box (e.g., "Enclosure rusted at base; nameplate stamped 208Y/120V 3Ph 4W").',
          'Tap "Add Field Note" to save the timestamped entry.',
          'Click any thumbnail image to inspect it in high resolution using the zoomable Lightbox.'
        ]
      },
      {
        id: 'master_catalog',
        category: 'breakers',
        categoryName: 'Breakers & Panels',
        icon: '📚',
        question: 'How do I pick breakers from the Master Catalog?',
        summary: 'Use verified manufacturer catalogs (Square D, Eaton, Siemens) with pre-filled frame sizes, AIC ratings, and mounting types.',
        tags: ['catalog', 'master catalog', 'square d', 'eaton', 'siemens', 'bolt-on', 'plug-in', 'aic', 'frame'],
        steps: [
          'In the Breaker Inspector modal, select the Pole count (1P, 2P, or 3P).',
          'Open the "Master Catalog Breaker" dropdown.',
          'The list dynamically filters to match the selected pole count and manufacturer series.',
          'Selecting an item automatically populates the Brand, Mounting type (Bolt-on/Plug-in), Frame, and Interrupting Capacity (AIC).',
          'You can also customize trip amperage or enter non-catalog custom ratings as needed.'
        ]
      },
      {
        id: 'facility_twin',
        category: 'facility',
        categoryName: 'Facility Twins & SLD',
        icon: '🏢',
        question: 'How do I switch facilities or create a new client digital twin?',
        summary: 'Manage multi-client facility datasets, switch between site projects, or create a clean industrial model.',
        tags: ['facility', 'client', 'switch', 'database', 'new facility', 'model', 'twin', 'workspace', 'seed'],
        steps: [
          'Click the Facility DB Pill in the header (or open Toolbox 🧰 → Files / Finder, or press Cmd+O).',
          'Search through existing facilities across all clients or click "+ New Facility Database".',
          'Enter the Client ID and Facility ID.',
          'Optionally check "Seed with standard industrial hierarchy templates" to pre-load a starter electrical tree.',
          'Click "Create & Switch" to immediately load the new SQLite database model.'
        ],
        action: { label: '📁 Open Facility Finder', key: 'open_finder' }
      },
      {
        id: 'single_line_diagram',
        category: 'facility',
        categoryName: 'Facility Twins & SLD',
        icon: '⚡',
        question: 'How do I generate and view the Single-Line Diagram (SLD)?',
        summary: 'Visualize the full electrical distribution single-line diagram schematic and power flow hierarchy.',
        tags: ['sld', 'single line diagram', 'schematic', 'topology', 'visualizer', 'power flow', 'export', 'svg'],
        steps: [
          'Open the Toolbox (🧰) and click "SLD Diagram" (or navigate to the Diagram view).',
          'JAMES computes the tree topology from Utility Feeds down to branch panels and generates an interactive Graphviz single-line schematic.',
          'Click any equipment box or cluster on the diagram to open the slide-over Inspector and edit ratings in real time.',
          'Use the Zoom & Pan controls or Export buttons to save SVG schematics and documentation.'
        ]
      },
      {
        id: 'arc_flash_safety',
        category: 'safety',
        categoryName: 'Safety & Arc Flash',
        icon: '⚡',
        question: 'How do I reference Arc Flash Labeling & Safety Standards in JAMES?',
        summary: 'Look up NFPA 70E / NEC 110.16 arc flash labeling requirements, boundaries, and safety PDFs.',
        tags: ['arc flash', 'safety', 'nfpa 70e', 'nec 110.16', 'labeling', 'incident energy', 'boundary', 'pdf', 'ppe', 'hazard'],
        steps: [
          'Search "arc flash" in the Help & Knowledge Base search bar to retrieve indexed technical spec PDFs with highlighted passages.',
          'Click "Open PDF (Page X) ↗" to view the Quick Start Guide on Arc Flash Labeling (QSG) in the built-in PDF viewer.',
          'Record the Arc Flash Label Date and custom incident energy attributes directly in the equipment editor drawer.'
        ],
        action: {
          key: 'open_arc_flash_pdf',
          label: '📖 View Arc Flash PDF Guide ↗'
        }
      },
      {
        id: 'offline_mode',
        category: 'field_tips',
        categoryName: 'Field Tips & Offline',
        icon: '📱',
        question: 'How do I work offline in electrical basements or shielded vaults?',
        summary: 'Survey smoothly without cellular reception, with local in-browser caching and instant export backups.',
        tags: ['offline', 'basement', 'vault', 'connectivity', 'cache', 'backup', 'export json', 'safety'],
        steps: [
          'JAMES runs locally in your browser environment; once loaded, the survey ledger and equipment drawer work offline.',
          'Use the Display & Font Scaling tile in the Toolbox (🧰) to adjust contrast (🌙 Dark / ☀️ Light) for low-light switchgear rooms.',
          'Download periodic Markdown (TOC) or Model JSONL backups directly from the Toolbox.',
          'Changes save directly to your facility SQLite database.'
        ]
      },
      {
        id: 'custom_attributes',
        category: 'assets',
        categoryName: 'Assets & Hierarchy',
        icon: '🏷️',
        question: 'What are Custom Attributes and when should I use them?',
        summary: 'Add flexible, project-specific metadata fields to any equipment item.',
        tags: ['custom attributes', 'metadata', 'arc flash', 'nema', 'enclosure', 'lock', 'metering', 'extra fields'],
        steps: [
          'In the equipment editor drawer, scroll to the "Custom / Archetype Specifications" section.',
          'Tap "+ Add Specification" to create an ad-hoc key-value row.',
          'Enter the Attribute Name (e.g., "Arc Flash Hazard Category", "NEMA Enclosure", "Key Lock #") and its Value.',
          'Custom attributes are preserved across all exports, reports, and digital twin models.'
        ]
      }
    ],

    // Help & FAQ Methods
    activeHelpTab: 'faq',
    helpSearch: '',
    helpFaqCategory: 'all',
    helpExpandedFaqs: {},
    kbSearchResults: [],
    kbSearchLoading: false,
    kbDebounceTimer: null,

    toggleFaq(id) {
      if (!this.helpExpandedFaqs) this.helpExpandedFaqs = {};
      this.helpExpandedFaqs[id] = !this.helpExpandedFaqs[id];
    },

    isFaqExpanded(id) {
      if (this.helpSearch && this.helpSearch.trim().length > 0) return true;
      if (!this.helpExpandedFaqs) this.helpExpandedFaqs = {};
      return !!this.helpExpandedFaqs[id];
    },

    onHelpSearchInput() {
      clearTimeout(this.kbDebounceTimer);
      const q = (this.helpSearch || '').trim();
      if (q.length < 2) {
        this.kbSearchResults = [];
        return;
      }

      this.kbDebounceTimer = setTimeout(async () => {
        try {
          this.kbSearchLoading = true;
          const catParam = (this.helpFaqCategory && this.helpFaqCategory !== 'all') ? `&category=${encodeURIComponent(this.helpFaqCategory)}` : '';
          const res = await fetch(`/api/kb/search?q=${encodeURIComponent(q)}${catParam}&limit=8`);
          if (res.ok) {
            const data = await res.json();
            this.kbSearchResults = data.results || [];
          }
        } catch (err) {
          console.error('KB FTS Search failed:', err);
        } finally {
          this.kbSearchLoading = false;
        }
      }, 200);
    },

    openDocumentViewer(filename, page = 1, title = '', section = '') {
      if (!filename) return;
      const cleanFilename = (filename || '').trim().split('/').pop();
      const ext = (cleanFilename || '').split('.').pop().toLowerCase();
      const pageNum = parseInt(page, 10) || 1;
      const targetName = 'kb_doc_' + cleanFilename.replace(/[^a-zA-Z0-9_]/g, '_');
      const url = ext === 'pdf'
        ? `/kb/viewer/${encodeURIComponent(cleanFilename)}?page=${pageNum}&title=${encodeURIComponent(title || '')}&section=${encodeURIComponent(section || '')}`
        : `/api/kb/view/${encodeURIComponent(cleanFilename)}`;

      try {
        const bc = new BroadcastChannel('build_aware_kb_channel');
        bc.postMessage({
          filename: cleanFilename,
          page: pageNum,
          title: title || cleanFilename,
          section: section || ''
        });
        setTimeout(() => { try { bc.close(); } catch(e) {} }, 1000);
      } catch (e) {
        console.warn('BroadcastChannel not supported', e);
      }

      const win = window.open(url, targetName);
      if (win) {
        try { win.focus(); } catch (e) {}
      }
    },

    get filteredFaqs() {
      const list = this.faqItems || [];
      const cat = this.helpFaqCategory || 'all';
      const q = (this.helpSearch || '').toLowerCase().trim();

      return list.filter(item => {
        const matchesCategory = cat === 'all' || item.category === cat;
        if (!matchesCategory) return false;
        if (!q) return true;

        const inQuestion = (item.question || '').toLowerCase().includes(q);
        const inSummary = (item.summary || '').toLowerCase().includes(q);
        const inCategory = (item.categoryName || '').toLowerCase().includes(q);
        const inTags = (item.tags || []).some(t => t.toLowerCase().includes(q));
        const inSteps = (item.steps || []).some(s => s.toLowerCase().includes(q));

        return inQuestion || inSummary || inCategory || inTags || inSteps;
      });
    },

    runFaqAction(key) {
      if (key === 'new_asset' && typeof this.openEquipmentPicker === 'function') {
        this.openEquipmentPicker();
      } else if (key === 'open_finder' && typeof this.openFinderModal === 'function') {
        this.openFinderModal();
      } else if (key === 'open_audit' && typeof this.openSystemAudit === 'function') {
        this.openSystemAudit();
      } else if (key === 'open_feeders' && typeof this.openFeederSchedule === 'function') {
        this.openFeederSchedule();
      } else if (key === 'open_arc_flash_pdf') {
        this.openDocumentViewer('QSG-Arc Flash Labeling.pdf', 1, 'Arc Flash Labeling Guide', 'Quick Start Guide');
      }
    },

    // ==========================================
    // CABLE & FEEDER MANAGEMENT ENGINE
    // ==========================================
    showCableDrawer: false,
    showFeederScheduleModal: false,
    isSavingFeeder: false,
    feederScheduleSearch: '',
    feederComplianceFilter: 'all',
    feederSortCol: 'from_tag',
    feederSortAsc: true,
    feederScheduleList: [],

    activeFeeder: {
      id: '',
      from_node: '',
      from_tag: '',
      to_node: '',
      to_tag: '',
      sets: 1,
      conductor: '4/0',
      conductor_material: 'Cu',
      insulation: 'THHN/THWN-2',
      neutral: 'Full (100%)',
      egc: '#4 AWG Cu',
      conduit: 'Steel',
      conduit_size: 'Auto',
      length_ft: 100,
      current_amps: 100,
      voltage: '480V 3Ø',
      breaker_trip: null,
      breaker_poles: null
    },

    cablePhysics: {
      v_drop_pct: 0.0,
      v_drop_volts: 0.0,
      total_ampacity: 230,
      impedance_z: 0.062,
      suggested_egc: '#4 AWG Cu',
      status: 'ok',
      compliance_message: '✅ Meets NEC 3% feeder limit'
    },

    async loadFacilityFeeders() {
      const c = this.client || this.client_id || 'zoetis';
      const f = this.facility || this.facility_id || 'b4';
      try {
        const res = await fetch(`/api/feeders?client_id=${encodeURIComponent(c)}&facility_id=${encodeURIComponent(f)}&_t=${Date.now()}`);
        if (res.ok) {
          const data = await res.json();
          this.feederScheduleList = Array.isArray(data) ? data : (data.feeders || []);
        }
      } catch (err) {
        console.error('Failed to load facility feeders:', err);
      }
    },

    async openFeederSchedule() {
      await this.loadFacilityFeeders();
      this.showFeederScheduleModal = true;
    },

    async openCableDrawer(feederOrId) {
      // Ensure feeders list is current
      if (!this.feederScheduleList || this.feederScheduleList.length === 0) {
        await this.loadFacilityFeeders();
      }

      let feeder = null;
      if (typeof feederOrId === 'object' && feederOrId !== null) {
        feeder = { ...feederOrId };
      } else if (typeof feederOrId === 'string') {
        const rawQuery = feederOrId.trim();
        const norm = (s) => (s || '').toLowerCase().replace(/[^a-z0-9]/g, '');
        const qNorm = norm(rawQuery);

        // 1. Direct match in feederScheduleList
        feeder = this.feederScheduleList.find(f => 
          f.id === rawQuery || 
          f.edge_id === rawQuery ||
          `edge_${f.from_node}_${f.to_node}`.toLowerCase() === rawQuery.toLowerCase() ||
          `edge_${f.from_tag}_${f.to_tag}`.toLowerCase() === rawQuery.toLowerCase() ||
          norm(`edge_${f.from_node}_${f.to_node}`) === qNorm ||
          norm(`edge_${f.from_tag}_${f.to_tag}`) === qNorm
        );

        // 2. Parse Arrow syntax (e.g. "UTIL_1->MSB" or "MSB:s->TX_1:n" or "Feeder: GEN -> ATS")
        if (!feeder && (rawQuery.includes('->') || rawQuery.includes('➔') || rawQuery.includes('-->') || rawQuery.includes('&#45;&gt;'))) {
          const arrowParts = rawQuery.replace(/^.*Feeder:\s*/i, '').replace(/&#45;&gt;/g, '->').split(/(?:->|➔|-->)/);
          if (arrowParts.length >= 2) {
            const cleanFrom = norm(arrowParts[0].split(':')[0]);
            const cleanTo = norm(arrowParts[1].split(':')[0]);
            feeder = this.feederScheduleList.find(f => 
              (norm(f.from_node) === cleanFrom || norm(f.from_tag) === cleanFrom) &&
              (norm(f.to_node) === cleanTo || norm(f.to_tag) === cleanTo)
            );
          }
        }

        // 3. Parse edge_From_To syntax (e.g. "edge_util_1_msb" or "edge_msb_tx_1")
        if (!feeder && rawQuery.startsWith('edge_')) {
          const stripped = rawQuery.replace(/^edge_/, '');
          const pool = (typeof this.getNodePool === 'function') ? this.getNodePool() : (this.stack || this.allNodes || window.facilityNodes || []);
          
          for (const fromN of pool) {
            const fromNorm = norm(fromN.tag || fromN.id);
            if (stripped.toLowerCase().startsWith(fromNorm)) {
              const remainder = stripped.substring(fromNorm.length).replace(/^_/, '');
              for (const toN of pool) {
                const toNorm = norm(toN.tag || toN.id);
                if (remainder.toLowerCase().startsWith(toNorm)) {
                  feeder = this.feederScheduleList.find(f => 
                    (norm(f.from_node) === fromNorm || norm(f.from_tag) === fromNorm) &&
                    (norm(f.to_node) === toNorm || norm(f.to_tag) === toNorm)
                  );
                  if (!feeder) {
                    feeder = {
                      id: `edge_${fromN.tag || fromN.id}_${toN.tag || toN.id}`,
                      from_node: fromN.tag || fromN.id,
                      from_tag: fromN.tag || fromN.id,
                      to_node: toN.tag || toN.id,
                      to_tag: toN.tag || toN.id,
                      voltage: toN.voltage || '480V 3Ø',
                      current_amps: Number(toN.amps) || 100
                    };
                  }
                  break;
                }
              }
              if (feeder) break;
            }
          }
        }

        // 4. Fuzzy fallback search against feeder schedule list
        if (!feeder && this.feederScheduleList.length > 0) {
          feeder = this.feederScheduleList.find(f => 
            qNorm.includes(norm(f.from_tag || f.from_node)) && 
            qNorm.includes(norm(f.to_tag || f.to_node))
          );
        }
      }

      if (!feeder) {
        // Construct fallback feeder placeholder
        feeder = {
          id: typeof feederOrId === 'string' ? feederOrId : 'feeder_temp',
          from_node: 'Source',
          from_tag: 'Source',
          to_node: 'Load',
          to_tag: 'Load',
          sets: 1,
          conductor: '4/0',
          conductor_material: 'Cu',
          insulation: 'THHN/THWN-2',
          neutral: 'Full (100%)',
          egc: '#4 AWG Cu',
          conduit: 'Steel',
          conduit_size: 'Auto',
          length_ft: 100,
          current_amps: 100,
          voltage: '480V 3Ø',
          breaker_trip: null
        };
      }

      // Populate activeFeeder
      this.activeFeeder = {
        id: feeder.id || `edge_${feeder.from_node}_${feeder.to_node}`,
        is_new: Boolean(feeder.is_new),
        from_node: feeder.from_node || '',
        from_tag: feeder.from_tag || feeder.from_node || '',
        to_node: feeder.to_node || '',
        to_tag: feeder.to_tag || feeder.to_node || '',
        sets: Number(feeder.sets) || 1,
        conductor: feeder.conductor || '4/0',
        conductor_material: feeder.conductor_material || 'Cu',
        insulation: feeder.insulation || 'THHN/THWN-2',
        neutral: feeder.neutral || 'Full (100%)',
        egc: feeder.egc || '#4 AWG Cu',
        conduit: feeder.conduit || 'Steel',
        conduit_size: feeder.conduit_size || 'Auto',
        length_ft: Number(feeder.length_ft) || 100,
        current_amps: Number(feeder.current_amps) || Number(feeder.breaker_trip) || 100,
        voltage: feeder.voltage || '480V 3Ø',
        breaker_trip: feeder.breaker_trip || null,
        breaker_poles: feeder.breaker_poles || null
      };

      // Realtime voltage drop calculation
      await this.calcCableVoltageDropRealtime();

      this.showCableDrawer = true;
    },

    async openNewFeederDrawer(fromNode = '', toNode = '') {
      this.showFeederScheduleModal = false;
      this.showEquipmentPicker = false;

      // Ensure nodes and feeders are current
      const pool = (typeof this.getNodePool === 'function') ? this.getNodePool() : (this.stack || this.allNodes || window.facilityNodes || []);
      
      const defaultFrom = fromNode || (pool.length > 0 ? (pool.find(n => n.domain === 'sources' || n.domain === 'panels')?.tag || pool[0].tag) : '');
      const defaultTo = toNode || (pool.length > 1 ? (pool.find(n => n.tag !== defaultFrom && n.domain !== 'sources')?.tag || pool[1].tag) : '');

      const targetToObj = pool.find(n => n.tag === defaultTo || n.id === defaultTo);
      const toVolts = targetToObj ? (targetToObj.voltage || '480V 3Ø') : '480V 3Ø';
      const toAmps = targetToObj ? (Number(targetToObj.amps) || 100) : 100;

      this.activeFeeder = {
        id: `edge_${Date.now()}`,
        is_new: true,
        from_node: defaultFrom,
        from_tag: defaultFrom,
        to_node: defaultTo,
        to_tag: defaultTo,
        sets: 1,
        conductor: '4/0',
        conductor_material: 'Cu',
        insulation: 'THHN/THWN-2',
        neutral: 'Full (100%)',
        egc: '#4 AWG Cu',
        conduit: 'Steel',
        conduit_size: 'Auto',
        length_ft: 100,
        current_amps: toAmps,
        voltage: toVolts,
        breaker_trip: null,
        breaker_poles: null
      };

      await this.calcCableVoltageDropRealtime();
      this.showCableDrawer = true;
    },

    onFeederEndpointChange() {
      const pool = (typeof this.getNodePool === 'function') ? this.getNodePool() : (this.stack || this.allNodes || window.facilityNodes || []);
      const toObj = pool.find(n => n.tag === this.activeFeeder.to_node || n.id === this.activeFeeder.to_node);
      if (toObj) {
        if (toObj.voltage) this.activeFeeder.voltage = toObj.voltage;
        if (toObj.amps) this.activeFeeder.current_amps = Number(toObj.amps) || 100;
      }
      this.calcCableVoltageDropRealtime();
    },

    closeCableDrawer() {
      this.showCableDrawer = false;
      if (typeof window.clearEdgeSelection === 'function') {
        window.clearEdgeSelection();
      }
    },

    jumpToEquipment(nodeIdOrTag) {
      this.showCableDrawer = false;
      this.showFeederScheduleModal = false;
      if (typeof window.clearEdgeSelection === 'function') {
        window.clearEdgeSelection();
      }
      if (typeof this.openEditDrawer === 'function') {
        this.openEditDrawer(nodeIdOrTag);
      } else if (typeof window.openEquipmentDrawer === 'function') {
        window.openEquipmentDrawer(nodeIdOrTag);
      }
    },

    async calcCableVoltageDropRealtime() {
      const f = this.activeFeeder;
      const payload = {
        conductor: f.conductor || '4/0',
        material: f.conductor_material || 'Cu',
        conduit: f.conduit || 'Steel',
        length_ft: Number(f.length_ft) || 100,
        current_amps: Number(f.current_amps) || 100,
        sets: Number(f.sets) || 1,
        system_voltage: String(f.voltage || '480V').includes('208') ? 208 : (String(f.voltage).includes('240') ? 240 : (String(f.voltage).includes('120') ? 120 : 480)),
        is_three_phase: !String(f.voltage || '').includes('1Ø') && !String(f.voltage || '').includes('120/240'),
        power_factor: 0.85
      };

      try {
        const res = await fetch('/api/feeders/calc-voltage-drop', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (res.ok) {
          const result = await res.json();
          this.cablePhysics = {
            v_drop_pct: result.voltage_drop_pct || 0.0,
            v_drop_volts: result.voltage_drop_volts || 0.0,
            total_ampacity: result.total_ampacity || 230,
            impedance_z: result.effective_impedance_z || 0.062,
            suggested_egc: result.suggested_egc || '#4 AWG Cu',
            status: result.status || 'ok',
            compliance_message: result.compliance_message || 'Compliant'
          };
          if (!f.egc || f.egc.includes('Auto')) {
            this.activeFeeder.egc = result.suggested_egc || '#4 AWG Cu';
          }
        }
      } catch (err) {
        console.warn('Realtime voltage drop API failed, using fallback:', err);
      }
    },

    async autoSizeFeeder() {
      const f = this.activeFeeder;
      const targetAmps = Number(f.current_amps) || 100;
      const targetLen = Number(f.length_ft) || 100;
      const mat = f.conductor_material || 'Cu';
      const cond = f.conduit || 'Steel';
      const is3p = !String(f.voltage || '').includes('1Ø');
      const v = String(f.voltage || '').includes('208') ? 208 : 480;

      const gauges = ['#14 AWG', '#12 AWG', '#10 AWG', '#8 AWG', '#6 AWG', '#4 AWG', '#3 AWG', '#2 AWG', '#1 AWG', '1/0', '2/0', '3/0', '4/0', '250 kcmil', '300 kcmil', '350 kcmil', '400 kcmil', '500 kcmil', '600 kcmil', '750 kcmil'];
      
      for (const g of gauges) {
        const res = await fetch('/api/feeders/calc-voltage-drop', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            conductor: g,
            material: mat,
            conduit: cond,
            length_ft: targetLen,
            current_amps: targetAmps,
            sets: 1,
            system_voltage: v,
            is_three_phase: is3p
          })
        });
        if (res.ok) {
          const r = await res.json();
          if (r.voltage_drop_pct <= 2.9 && r.total_ampacity >= targetAmps) {
            this.activeFeeder.conductor = g;
            this.activeFeeder.sets = 1;
            await this.calcCableVoltageDropRealtime();
            this.toast(`🪄 Auto-sized to 1x (${g} ${mat}) for ${r.voltage_drop_pct.toFixed(2)}% ΔV!`);
            return;
          }
        }
      }

      // If single run exceeds gauge, try 2x sets
      this.activeFeeder.sets = 2;
      this.activeFeeder.conductor = '4/0';
      await this.calcCableVoltageDropRealtime();
      this.toast(`🪄 Auto-sized to 2x (4/0 ${mat}) parallel feeder!`);
    },

    async saveCableSpecs() {
      const c = this.client || this.client_id || 'zoetis';
      const f = this.facility || this.facility_id || 'b4';
      const af = this.activeFeeder;

      this.isSavingFeeder = true;
      try {
        const payload = {
          client_id: c,
          facility_id: f,
          from_node: af.from_node,
          to_node: af.to_node,
          conductor: af.conductor,
          conductor_material: af.conductor_material,
          insulation: af.insulation,
          sets: Number(af.sets) || 1,
          neutral: af.neutral,
          egc: af.egc,
          conduit: af.conduit,
          conduit_size: af.conduit_size,
          length_ft: Number(af.length_ft) || 100,
          current_amps: Number(af.current_amps) || 100,
          voltage_drop_pct: this.cablePhysics.v_drop_pct || 0.0,
          voltage: af.voltage
        };

        const res = await fetch('/api/feeders/update', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (!res.ok) {
          throw new Error('Failed to save cable attributes');
        }

        const updatedFeeder = await res.json();

        // If newly created feeder run, also ensure destination node upstream sources include from_node
        if (af.is_new) {
          try {
            const pool = (typeof this.getNodePool === 'function') ? this.getNodePool() : (this.stack || this.allNodes || window.facilityNodes || []);
            const targetNode = pool.find(n => n.tag === af.to_node || n.id === af.to_node);
            if (targetNode) {
              const upList = Array.isArray(targetNode.upstream_sources) ? [...targetNode.upstream_sources] : (targetNode.fed_from ? [targetNode.fed_from] : []);
              if (!upList.includes(af.from_node)) {
                upList.push(af.from_node);
              }
              targetNode.fed_from = upList[0] || af.from_node;
              targetNode.upstream_sources = upList;
              
              await fetch(`/api/clients/${c}/facilities/${f}/nodes`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(targetNode)
              });
            }
          } catch (syncErr) {
            console.warn('Could not sync node upstream fed_from link:', syncErr);
          }
        }

        this.toast(`🔌 Saved feeder: ${af.from_tag || af.from_node} ➔ ${af.to_tag || af.to_node}!`);
        this.showCableDrawer = false;
        if (typeof window.clearEdgeSelection === 'function') {
          window.clearEdgeSelection();
        }

        // Reload feeders list
        await this.loadFacilityFeeders();

        // Refresh diagram if in SLD view
        if (typeof window.refreshDiagram === 'function') {
          window.refreshDiagram();
        } else if (typeof refreshDiagram === 'function') {
          refreshDiagram();
        }
      } catch (err) {
        console.error('Error saving cable specs:', err);
        this.toast(`⚠️ Error saving cable specs: ${err.message}`);
      } finally {
        this.isSavingFeeder = false;
      }
    },

    get filteredFeederScheduleList() {
      const list = this.feederScheduleList || [];
      const q = (this.feederScheduleSearch || '').toLowerCase().trim();
      const comp = this.feederComplianceFilter || 'all';

      const filtered = list.filter(item => {
        // Compliance filter
        const vdrop = item.voltage_drop_pct || 0;
        if (comp === 'ok' && vdrop > 3.0) return false;
        if (comp === 'warning' && (vdrop <= 3.0 || vdrop > 5.0)) return false;
        if (comp === 'critical' && vdrop <= 5.0) return false;

        if (!q) return true;
        const fromTag = (item.from_tag || item.from_node || '').toLowerCase();
        const toTag = (item.to_tag || item.to_node || '').toLowerCase();
        const cond = (item.conductor || '').toLowerCase();
        const conduit = (item.conduit || '').toLowerCase();
        const trip = String(item.breaker_trip || '');

        return fromTag.includes(q) || toTag.includes(q) || cond.includes(q) || conduit.includes(q) || trip.includes(q);
      });

      const col = this.feederSortCol || 'from_tag';
      const asc = this.feederSortAsc !== false;

      const gaugeRank = (g) => {
        const order = ['#14', '#12', '#10', '#8', '#6', '#4', '#3', '#2', '#1', '1/0', '2/0', '3/0', '4/0', '250', '300', '350', '400', '500', '600', '750'];
        const str = String(g || '');
        const idx = order.findIndex(o => str.includes(o));
        return idx >= 0 ? idx : 999;
      };

      return filtered.sort((a, b) => {
        let valA, valB;
        if (col === 'length_ft') {
          valA = Number(a.length_ft) || 0;
          valB = Number(b.length_ft) || 0;
        } else if (col === 'voltage_drop_pct') {
          valA = Number(a.voltage_drop_pct) || 0;
          valB = Number(b.voltage_drop_pct) || 0;
        } else if (col === 'breaker_trip') {
          valA = Number(a.breaker_trip) || 0;
          valB = Number(b.breaker_trip) || 0;
        } else if (col === 'conductor') {
          valA = gaugeRank(a.conductor);
          valB = gaugeRank(b.conductor);
        } else if (col === 'conductor_material') {
          valA = (a.conductor_material || '').toLowerCase();
          valB = (b.conductor_material || '').toLowerCase();
        } else if (col === 'conduit') {
          valA = (a.conduit || '').toLowerCase();
          valB = (b.conduit || '').toLowerCase();
        } else if (col === 'to_tag') {
          valA = (a.to_tag || a.to_node || '').toLowerCase();
          valB = (b.to_tag || b.to_node || '').toLowerCase();
        } else {
          // default from_tag
          valA = (a.from_tag || a.from_node || '').toLowerCase();
          valB = (b.from_tag || b.from_node || '').toLowerCase();
        }

        if (valA < valB) return asc ? -1 : 1;
        if (valA > valB) return asc ? 1 : -1;
        return 0;
      });
    },

    toggleFeederSort(col) {
      if (this.feederSortCol === col) {
        this.feederSortAsc = !this.feederSortAsc;
      } else {
        this.feederSortCol = col;
        this.feederSortAsc = true;
      }
    },

    get totalFeederRouteLength() {
      const list = this.feederScheduleList || [];
      return list.reduce((acc, f) => acc + (Number(f.length_ft) || 0), 0);
    },

    get compliantFeederCount() {
      const list = this.feederScheduleList || [];
      return list.filter(f => (f.voltage_drop_pct || 0) <= 3.0).length;
    },

    get warningFeederCount() {
      const list = this.feederScheduleList || [];
      return list.filter(f => (f.voltage_drop_pct || 0) > 3.0).length;
    },

    exportFeederScheduleCSV() {
      const list = this.filteredFeederScheduleList || [];
      if (list.length === 0) {
        this.toast('⚠️ No feeders to export');
        return;
      }

      const headers = ['From Equipment', 'To Equipment', 'Breaker / OCPD (A)', 'Sets', 'Conductor Gauge', 'Material', 'Insulation', 'Neutral', 'EGC Ground', 'Conduit', 'Length (ft)', 'Operating Amps', 'Voltage Drop %', 'Status'];
      const rows = list.map(f => [
        `"${f.from_tag || f.from_node}"`,
        `"${f.to_tag || f.to_node}"`,
        f.breaker_trip || '',
        f.sets || 1,
        `"${f.conductor || '4/0'}"`,
        f.conductor_material || 'Cu',
        `"${f.insulation || 'THHN/THWN-2'}"`,
        `"${f.neutral || 'Full'}"`,
        `"${f.egc || '#4 Cu'}"`,
        `"${(f.conduit_size || '') + ' ' + (f.conduit || 'Steel')}"`.trim(),
        f.length_ft || 100,
        f.current_amps || '',
        (f.voltage_drop_pct ? f.voltage_drop_pct.toFixed(2) : '0.00'),
        (f.voltage_drop_pct || 0) <= 3.0 ? 'Compliant (<3%)' : ((f.voltage_drop_pct || 0) <= 5.0 ? 'Warning (3-5%)' : 'Critical (>5%)')
      ]);

      const csvContent = [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `feeder_schedule_${this.client || 'zoetis'}_${this.facility || 'b4'}.csv`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      this.toast('📥 Feeder schedule exported to CSV!');
    },

    copyFeederScheduleMD() {
      const list = this.filteredFeederScheduleList || [];
      if (list.length === 0) {
        this.toast('⚠️ No feeders to copy');
        return;
      }

      let md = `# Feeder & Conductor Schedule • ${(this.client || 'facility').toUpperCase()} / ${(this.facility || '').toUpperCase()}\n\n`;
      md += `| Status | From | To | Breaker | Conductors | Neutral & Ground | Conduit | Length | ΔV % |\n`;
      md += `|:---|:---|:---|:---|:---|:---|:---|---:|---:|\n`;

      list.forEach(f => {
        const status = (f.voltage_drop_pct || 0) <= 3.0 ? '✅ OK' : ((f.voltage_drop_pct || 0) <= 5.0 ? '⚠️ WARN' : '🚨 CRIT');
        const condStr = `${f.sets > 1 ? f.sets + 'x ' : ''}(${f.conductor || '4/0'} ${f.conductor_material || 'Cu'})`;
        const ngStr = `${f.neutral || 'Full N'} / ${f.egc || 'Auto EGC'}`;
        const conduitStr = `${f.conduit_size && f.conduit_size !== 'Auto' ? f.conduit_size + ' ' : ''}${f.conduit || 'Steel'}`;
        const vdropStr = `${(f.voltage_drop_pct || 0).toFixed(2)}%`;
        const tripStr = f.breaker_trip ? `${f.breaker_trip}A` : '--';

        md += `| ${status} | **${f.from_tag || f.from_node}** | **${f.to_tag || f.to_node}** | ${tripStr} | ${condStr} | ${ngStr} | ${conduitStr} | ${f.length_ft || 100} ft | ${vdropStr} |\n`;
      });

      navigator.clipboard.writeText(md).then(() => {
        this.toast('📋 Feeder schedule copied to clipboard as Markdown table!');
      }).catch(() => {
        this.toast('⚠️ Failed to copy to clipboard');
      });
    },

    /**
     * Safely attaches shared getters and methods to an Alpine.js component instance.
     */
    attachTo(target) {
      const descriptors = Object.getOwnPropertyDescriptors(this);
      delete descriptors.attachTo;
      Object.defineProperties(target, descriptors);
      return target;
    }
  };
})();

