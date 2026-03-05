/**
 * CipherLab — Core Application JS
 * Shared utilities and global behavior.
 */
(function () {
    'use strict';

    // ═══════════════ KEYBOARD SHORTCUTS ═══════════════
    document.addEventListener('keydown', (e) => {
        // Ctrl+K → focus first input on page
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const input = document.querySelector('.input-field');
            if (input) input.focus();
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
        toast.className = `fixed bottom-6 right-6 z-[9999] px-4 py-2.5 rounded-lg text-sm font-medium shadow-lg animate-slide-up`;
        toast.style.background = type === 'error' ? '#991B1B' : '#0F1729';
        toast.style.color = type === 'error' ? '#FCA5A5' : '#E2E8F0';
        toast.style.border = `1px solid ${type === 'error' ? 'rgba(239,68,68,0.2)' : 'rgba(99,102,241,0.15)'}`;
        toast.style.backdropFilter = 'blur(12px)';
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
        if (panel) panel.classList.toggle('open');
    };

})();
