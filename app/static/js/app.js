/**
 * CipherLab — Core Application JS
 * Shared utilities and global behavior.
 */
(function () {
    'use strict';

    function ensureToastContainer() {
        let container = document.getElementById('app-toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'app-toast-container';
            container.className = 'app-toast-container';
            container.setAttribute('aria-live', 'polite');
            container.setAttribute('aria-atomic', 'true');
            document.body.appendChild(container);
        }
        return container;
    }

    function getToastIcon(type) {
        if (type === 'success') return 'M5 13l4 4L19 7';
        if (type === 'error') return 'M12 9v2m0 4h.01m-.01-12a9 9 0 100 18 9 9 0 000-18z';
        if (type === 'warn') return 'M12 9v3.75m0 3.75h.007v.008H12v-.008zM10.29 3.86L1.82 18a2 2 0 001.72 3h16.92a2 2 0 001.72-3L13.71 3.86a2 2 0 00-3.42 0z';
        return 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z';
    }

    function initAnimatedInputBorders() {
        const fields = document.querySelectorAll('input.input-field, textarea.input-field, select.input-field');
        fields.forEach((field) => {
            if (!field.parentElement || field.parentElement.classList.contains('input-glow-wrap')) {
                return;
            }

            const wrapper = document.createElement('div');
            wrapper.className = 'input-glow-wrap';
            field.parentElement.insertBefore(wrapper, field);
            wrapper.appendChild(field);
        });
    }

    // ═══════════════ MOBILE SIDEBAR TOGGLE ═══════════════
    function initSidebarToggle() {
        const sidebarToggle = document.getElementById('sidebar-toggle');
        const sidebar = document.getElementById('sidebar');
        const sidebarOverlay = document.getElementById('sidebar-overlay');
        
        if (!sidebarToggle || !sidebar) return;
        
        const toggleSidebar = (e) => {
            e?.stopPropagation?.();
            const isOpen = sidebar.classList.contains('active');
            
            if (isOpen) {
                sidebar.classList.remove('active');
                sidebarOverlay?.classList.remove('active');
            } else {
                sidebar.classList.add('active');
                sidebarOverlay?.classList.add('active');
            }
        };
        
        const closeSidebar = () => {
            sidebar.classList.remove('active');
            sidebarOverlay?.classList.remove('active');
        };
        
        // Toggle on button click
        sidebarToggle.addEventListener('click', toggleSidebar);
        
        // Close on overlay click
        sidebarOverlay?.addEventListener('click', closeSidebar);
        
        // Close when clicking nav links (mobile)
        const navLinks = sidebar.querySelectorAll('a[href]');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 1024) {
                    closeSidebar();
                }
            });
        });
        
        // Close sidebar when window resizes to desktop
        window.addEventListener('resize', () => {
            if (window.innerWidth >= 1024) {
                closeSidebar();
            }
        });
        
        // Prevent sidebar from closing when clicking inside it
        sidebar.addEventListener('click', (e) => {
            e.stopPropagation?.();
        });
    }
    
    // Initialize after DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSidebarToggle);
    } else {
        initSidebarToggle();
    }

    // ═══════════════ KEYBOARD SHORTCUTS ═══════════════
    document.addEventListener('keydown', (e) => {
        const sidebar = document.getElementById('sidebar');
        
        // Ctrl+K / Cmd+K → focus first input on page
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const input = document.querySelector('input.input-field, input[type="text"]:first-of-type');
            if (input) input.focus();
        }
        
        // Escape → close sidebar on mobile
        if (e.key === 'Escape' && sidebar?.classList.contains('active')) {
            sidebar.classList.remove('active');
            document.getElementById('sidebar-overlay')?.classList.remove('active');
        }
    });

    // ═══════════════ COPY TO CLIPBOARD ═══════════════
    window.copyToClipboard = async function (text) {
        try {
            await navigator.clipboard.writeText(text);
            showToast('Copied to clipboard');
        } catch {
            // Fallback
            const ta = document.createElement('textarea');
            ta.value = text;
            ta.style.position = 'fixed';
            ta.style.opacity = '0';
            document.body.appendChild(ta);
            ta.select();
            document.execCommand('copy');
            ta.remove();
            showToast('Copied');
        }
    };

    // ═══════════════ TOAST NOTIFICATIONS ═══════════════
    window.showToast = function (message, type = 'info') {
        const normalizedType = ['info', 'success', 'error', 'warn'].includes(type) ? type : 'info';
        const container = ensureToastContainer();
        const toast = document.createElement('div');
        toast.className = `app-toast ${normalizedType}`;
        toast.innerHTML = `
            <div class="app-toast-icon" aria-hidden="true">
                <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="${getToastIcon(normalizedType)}"/>
                </svg>
            </div>
            <div class="app-toast-message">${message}</div>
        `;
        container.appendChild(toast);
        requestAnimationFrame(() => toast.classList.add('show'));

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 240);
        }, 2600);
    };

    window.showWarn = function (message) {
        window.showToast(message, 'warn');
    };

    // ═══════════════ GLOBAL FETCH ERROR HANDLER ═══════════════
    window.addEventListener('unhandledrejection', (e) => {
        console.error('Unhandled promise rejection:', e.reason);
    });

    // ═══════════════ GUIDE PANEL TOGGLE ═══════════════
    window.toggleGuide = function (id) {
        const panel = document.getElementById(id || 'guide-panel');
        if (panel) {
            panel.classList.toggle('open');
            // Scroll panel into view on mobile
            if (window.innerWidth < 768) {
                setTimeout(() => {
                    panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 100);
            }
        }
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAnimatedInputBorders);
    } else {
        initAnimatedInputBorders();
    }

})();
