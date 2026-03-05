/**
 * CipherLab — Core Application JS
 * Shared utilities and global behavior.
 */
(function () {
    'use strict';

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
        const toast = document.createElement('div');
        toast.className = `fixed bottom-4 sm:bottom-6 right-4 sm:right-6 z-[9999] px-4 py-2.5 rounded-lg text-sm font-medium shadow-lg animate-slide-up max-w-xs`;
        toast.style.background = type === 'error' ? '#991B1B' : type === 'success' ? '#065F46' : '#0F1729';
        toast.style.color = type === 'error' ? '#FCA5A5' : type === 'success' ? '#86EFAC' : '#E2E8F0';
        toast.style.border = `1px solid ${type === 'error' ? 'rgba(239,68,68,0.2)' : type === 'success' ? 'rgba(34,197,94,0.2)' : 'rgba(99,102,241,0.15)'}`;
        toast.style.backdropFilter = 'blur(12px)';
        toast.style.wordWrap = 'break-word';
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity 0.3s';
            setTimeout(() => toast.remove(), 300);
        }, 2500);
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

})();
