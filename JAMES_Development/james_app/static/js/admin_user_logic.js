/**
 * JAMES Admin User & Access Management Shared Logic
 * Provides full user listing, creation, role editing, password resets, and activation toggling.
 */
(function() {
  window.AdminUserModalLogic = {
    attachTo(app) {
      app.showAdminUserModal = false;
      app.adminUsers = [];
      app.adminSearchQuery = '';
      app.adminToast = { message: '', type: 'success' };
      app.adminResetModal = {
        isOpen: false,
        user: null,
        newPassword: '',
        showPassword: true,
        copied: false,
        loading: false
      };
      app.adminUserModal = {
        isOpen: false,
        isEdit: false,
        loading: false,
        form: {
          email: '',
          name: '',
          role: 'engineer',
          password: '',
          is_active: true
        }
      };

      app.openAdminUserModal = async function() {
        this.showAdminUserModal = true;
        await this.fetchAdminUsers();
      };

      app.closeAdminUserModal = function() {
        this.showAdminUserModal = false;
        if (this.adminResetModal) this.adminResetModal.isOpen = false;
        if (this.adminUserModal) this.adminUserModal.isOpen = false;
      };

      app.showAdminToast = function(message, type = 'success') {
        this.adminToast = { message, type };
        setTimeout(() => {
          if (this.adminToast.message === message) this.adminToast.message = '';
        }, 5000);
      };

      app.getFilteredAdminUsers = function() {
        if (!this.adminUsers) return [];
        if (!this.adminSearchQuery) return this.adminUsers;
        const q = this.adminSearchQuery.toLowerCase();
        return this.adminUsers.filter(u => 
          (u.name && u.name.toLowerCase().includes(q)) ||
          (u.email && u.email.toLowerCase().includes(q)) ||
          (u.username && u.username.toLowerCase().includes(q)) ||
          (u.role && u.role.toLowerCase().includes(q))
        );
      };

      app.fetchAdminUsers = async function() {
        try {
          const resp = await fetch('/api/admin/users');
          if (!resp.ok) {
            const errData = await resp.json().catch(() => ({}));
            throw new Error(errData.detail || 'Failed to load users');
          }
          const data = await resp.json();
          this.adminUsers = data.users || [];
        } catch (err) {
          this.showAdminToast(err.message, 'error');
        }
      };

      app.openAdminResetPassword = function(user) {
        this.adminResetModal = {
          isOpen: true,
          user: user,
          newPassword: '',
          showPassword: true,
          copied: false,
          loading: false
        };
        this.generateAdminPassword();
      };

      app.generateAdminPassword = function() {
        const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789!@#$%';
        let pwd = '';
        for (let i = 0; i < 10; i++) {
          pwd += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        this.adminResetModal.newPassword = pwd;
        this.adminResetModal.copied = false;
      };

      app.copyAdminPassword = function() {
        if (!this.adminResetModal.newPassword) return;
        navigator.clipboard.writeText(this.adminResetModal.newPassword);
        this.adminResetModal.copied = true;
        setTimeout(() => { 
          if (this.adminResetModal) this.adminResetModal.copied = false; 
        }, 2500);
      };

      app.submitAdminPasswordReset = async function() {
        if (!this.adminResetModal.newPassword || !this.adminResetModal.user) return;
        this.adminResetModal.loading = true;
        try {
          const resp = await fetch('/api/admin/users/reset-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              identifier: this.adminResetModal.user.email,
              new_password: this.adminResetModal.newPassword
            })
          });
          const res = await resp.json();
          if (!resp.ok) throw new Error(res.detail || 'Password reset failed');
          this.showAdminToast(res.message || 'Password successfully updated!', 'success');
          this.adminResetModal.isOpen = false;
        } catch (err) {
          this.showAdminToast(err.message, 'error');
        } finally {
          this.adminResetModal.loading = false;
        }
      };

      app.openAdminAddUser = function() {
        this.adminUserModal = {
          isOpen: true,
          isEdit: false,
          loading: false,
          form: {
            email: '',
            name: '',
            role: 'engineer',
            password: '',
            is_active: true
          }
        };
      };

      app.openAdminEditUser = function(user) {
        this.adminUserModal = {
          isOpen: true,
          isEdit: true,
          loading: false,
          form: {
            email: user.email,
            name: user.name,
            role: user.role,
            password: '',
            is_active: user.is_active
          }
        };
      };

      app.submitAdminUserForm = async function() {
        if (!this.adminUserModal.form.email) return;
        this.adminUserModal.loading = true;
        try {
          const resp = await fetch('/api/admin/users/upsert', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.adminUserModal.form)
          });
          const res = await resp.json();
          if (!resp.ok) throw new Error(res.detail || 'Failed to save user');
          this.showAdminToast(res.message || 'User saved successfully!', 'success');
          this.adminUserModal.isOpen = false;
          await this.fetchAdminUsers();
        } catch (err) {
          this.showAdminToast(err.message, 'error');
        } finally {
          this.adminUserModal.loading = false;
        }
      };

      app.toggleAdminUserActive = async function(user) {
        const newStatus = !user.is_active;
        try {
          const resp = await fetch('/api/admin/users/toggle-active', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              identifier: user.email,
              is_active: newStatus
            })
          });
          const res = await resp.json();
          if (!resp.ok) throw new Error(res.detail || 'Failed to toggle user status');
          user.is_active = newStatus;
          this.showAdminToast(res.message, 'success');
        } catch (err) {
          this.showAdminToast(err.message, 'error');
        }
      };

      app.deleteAdminUser = async function(user) {
        if (!confirm(`Are you sure you want to permanently remove user account ${user.name} (${user.email})?`)) {
          return;
        }
        try {
          const resp = await fetch('/api/admin/users/delete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ identifier: user.email })
          });
          const res = await resp.json();
          if (!resp.ok) throw new Error(res.detail || 'Failed to delete user');
          this.showAdminToast(res.message, 'success');
          await this.fetchAdminUsers();
        } catch (err) {
          this.showAdminToast(err.message, 'error');
        }
      };
    }
  };

  // Global helper functions callable from onclick or anywhere in the document
  window.openAdminUserModal = function() {
    const appInstance = window.alpineApp || window.__sldAppInstance || window.__surveyAppInstance || window.__catalogAppInstance;
    if (appInstance && typeof appInstance.openAdminUserModal === 'function') {
      appInstance.openAdminUserModal();
    } else if (appInstance) {
      appInstance.showAdminUserModal = true;
      if (typeof appInstance.fetchAdminUsers === 'function') {
        appInstance.fetchAdminUsers();
      }
    }
  };

  window.closeAdminUserModal = function() {
    const appInstance = window.alpineApp || window.__sldAppInstance || window.__surveyAppInstance || window.__catalogAppInstance;
    if (appInstance && typeof appInstance.closeAdminUserModal === 'function') {
      appInstance.closeAdminUserModal();
    } else if (appInstance) {
      appInstance.showAdminUserModal = false;
    }
  };
})();
