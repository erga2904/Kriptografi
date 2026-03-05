/**
 * CipherLab — Microinteractions
 * Liquid ripple clicks, circular light burst on submit,
 * SVG icon hover animations, sidebar, card entrance.
 */
(function () {
    'use strict';

    // ═══════════════ LIQUID RIPPLE CLICK ═══════════════
    // Mimics a water drop on glass — soft, expanding ring
    document.addEventListener('click', (e) => {
        const ripple = document.createElement('div');
        ripple.className = 'liquid-ripple';
        ripple.style.left = (e.clientX - 80) + 'px';
        ripple.style.top = (e.clientY - 80) + 'px';
        document.body.appendChild(ripple);
        setTimeout(() => ripple.remove(), 650);
    });

    // ═══════════════ CIRCULAR LIGHT BURST ON SUBMIT ═══════════════
    // Fires on .btn-primary clicks — elegant, fast, low opacity, 300-600ms
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.btn-primary');
        if (!btn) return;

        const burst = document.createElement('div');
        burst.className = 'light-burst';
        burst.style.left = e.clientX + 'px';
        burst.style.top = e.clientY + 'px';
        document.body.appendChild(burst);
        setTimeout(() => burst.remove(), 500);
    });

    // ═══════════════ SVG ICON HOVER ANIMATIONS ═══════════════
    // Already handled via CSS (.nav-icon transitions in main.css)
    // This adds subtle stroke-dashoffset animation for drawing effect
    document.querySelectorAll('.nav-link').forEach(link => {
        const icon = link.querySelector('.nav-icon');
        if (!icon) return;

        const paths = icon.querySelectorAll('path');
        paths.forEach(path => {
            // Store original stroke-dasharray
            const length = path.getTotalLength ? path.getTotalLength() : 100;
            path.style.strokeDasharray = length;
            path.style.strokeDashoffset = '0';
            path.style.transition = 'stroke-dashoffset 0.3s ease, stroke 0.3s ease, filter 0.3s ease';
        });

        link.addEventListener('mouseenter', () => {
            paths.forEach(path => {
                const length = path.getTotalLength ? path.getTotalLength() : 100;
                path.style.strokeDashoffset = length * 0.05 + '';
            });
        });

        link.addEventListener('mouseleave', () => {
            paths.forEach(path => {
                path.style.strokeDashoffset = '0';
            });
        });
    });

    // ═══════════════ SIDEBAR TOGGLE ═══════════════
    const sidebar = document.getElementById('sidebar');
    const toggle = document.getElementById('sidebar-toggle');
    const mainContent = document.getElementById('main-content');

    if (toggle && sidebar) {
        toggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });

        // Close sidebar on content click (mobile)
        if (mainContent) {
            mainContent.addEventListener('click', () => {
                if (sidebar.classList.contains('open')) {
                    sidebar.classList.remove('open');
                }
            });
        }
    }

    // ═══════════════ ACTIVE NAV HIGHLIGHT ═══════════════
    const path = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (path === href || (href !== '/' && path.startsWith(href))) {
            link.classList.add('active');
            link.setAttribute('aria-current', 'page');
        }
    });

    // ═══════════════ CARD ENTRANCE ANIMATION ═══════════════
    const cards = document.querySelectorAll('.card-base');
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!prefersReducedMotion) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    // Stagger based on index in DOM
                    const siblings = Array.from(entry.target.parentElement.children);
                    const idx = siblings.indexOf(entry.target);
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, idx * 60);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.05 });

        cards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(10px)';
            card.style.transition = 'opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1), transform 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
            observer.observe(card);
        });
    }
})();
