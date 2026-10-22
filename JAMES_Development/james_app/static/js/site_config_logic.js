/**
 * Building Aware (JAMES) - Site Configuration Logic Mixin
 * Provides interactive management of facility profile, incoming service voltage (e.g. 208Y/120V vs 480Y/277V),
 * utility company parameters, physical site address, and primary facility contact personnel.
 */
(function() {
  window.SiteConfigModalLogic = {
    attachTo(app) {
      app.showSiteConfigModal = false;
      app.siteConfigLoading = false;
      app.siteConfigSaving = false;
      app.siteConfigTab = 'identity';
      app.siteConfigSuccessMsg = '';
      app.siteConfigErrorMsg = '';

      app.siteConfig = {
        client_id: '',
        facility_id: '',
        facility_name: '',
        street_address: '',
        city: '',
        state: '',
        postal_code: '',
        country: 'USA',
        full_address: '',
        service_voltage: '480Y/277V 3Ø 4W',
        service_amperage: 2000,
        service_phase: 3,
        service_wires: 4,
        service_frequency: '60 Hz',
        service_type: 'Underground Pad-Mounted',
        main_disconnect_type: 'Main Circuit Breaker (MCB)',
        available_fault_current_ka: 65,
        utility_name: '',
        utility_account_number: '',
        utility_meter_number: '',
        utility_transformer_id: '',
        primary_contact_name: '',
        primary_contact_title: '',
        primary_contact_email: '',
        primary_contact_phone: '',
        emergency_contact_name: '',
        emergency_contact_phone: '',
        facility_operating_hours: '24/7 Operations',
        nec_edition: 'NEC 2023',
        arc_flash_study_date: '',
        arc_flash_status: 'Verified / Compliant',
        notes: '',
        attributes: {}
      };

      app.openSiteConfigModal = async function() {
        this.showSiteConfigModal = true;
        this.siteConfigSuccessMsg = '';
        this.siteConfigErrorMsg = '';
        this.siteConfigTab = 'identity';
        await this.loadSiteConfig();
      };

      app.closeSiteConfigModal = function() {
        this.showSiteConfigModal = false;
        this.siteConfigSuccessMsg = '';
        this.siteConfigErrorMsg = '';
      };

      app.loadSiteConfig = async function() {
        const c = this.client || 'zoetis';
        const f = this.facility || 'b4';
        this.siteConfigLoading = true;
        this.siteConfigErrorMsg = '';

        try {
          const resp = await fetch(`/api/clients/${encodeURIComponent(c)}/facilities/${encodeURIComponent(f)}/config`);
          if (!resp.ok) {
            throw new Error(`Failed to load site configuration (HTTP ${resp.status})`);
          }
          const data = await resp.json();
          this.siteConfig = Object.assign({}, this.siteConfig, data);
        } catch (err) {
          console.error('[SiteConfig] Error loading configuration:', err);
          this.siteConfigErrorMsg = err.message || 'Error loading site configuration';
        } finally {
          this.siteConfigLoading = false;
        }
      };

      app.saveSiteConfig = async function() {
        const c = this.client || 'zoetis';
        const f = this.facility || 'b4';
        this.siteConfigSaving = true;
        this.siteConfigSuccessMsg = '';
        this.siteConfigErrorMsg = '';

        try {
          const resp = await fetch(`/api/clients/${encodeURIComponent(c)}/facilities/${encodeURIComponent(f)}/config`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.siteConfig)
          });

          if (!resp.ok) {
            const errData = await resp.json().catch(() => ({}));
            throw new Error(errData.detail || `Save failed with HTTP ${resp.status}`);
          }

          const res = await resp.json();
          if (res.config) {
            this.siteConfig = Object.assign({}, this.siteConfig, res.config);
          }

          this.siteConfigSuccessMsg = 'Site configuration saved successfully ✓';

          // If CAD SLD modal is currently active, refresh preview to show updated title block
          if (this.showCadModal && typeof this.fetchCadSvg === 'function') {
            this.fetchCadSvg();
          }

          // Auto-clear success message after 4 seconds
          setTimeout(() => {
            if (this.siteConfigSuccessMsg) {
              this.siteConfigSuccessMsg = '';
            }
          }, 4000);

        } catch (err) {
          console.error('[SiteConfig] Error saving configuration:', err);
          this.siteConfigErrorMsg = err.message || 'Error saving site configuration';
        } finally {
          this.siteConfigSaving = false;
        }
      };

      app.applyVoltagePreset = function(v) {
        if (!v) return;
        this.siteConfig.service_voltage = v;
        if (v.includes('208')) {
          if (!this.siteConfig.service_amperage || this.siteConfig.service_amperage > 2000) {
            this.siteConfig.service_amperage = 800;
          }
          this.siteConfig.service_phase = 3;
          this.siteConfig.service_wires = 4;
        } else if (v.includes('480')) {
          if (!this.siteConfig.service_amperage || this.siteConfig.service_amperage < 1200) {
            this.siteConfig.service_amperage = 2500;
          }
          this.siteConfig.service_phase = 3;
          this.siteConfig.service_wires = 4;
        } else if (v.includes('240')) {
          this.siteConfig.service_phase = 1;
          this.siteConfig.service_wires = 3;
          if (!this.siteConfig.service_amperage || this.siteConfig.service_amperage > 600) {
            this.siteConfig.service_amperage = 400;
          }
        }
      };

      app.is208vOnlySite = function() {
        const v = String(this.siteConfig.service_voltage || '');
        return v.includes('208') || v.includes('120/208');
      };
    }
  };
})();
