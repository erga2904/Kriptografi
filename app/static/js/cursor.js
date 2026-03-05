/**
 * CipherLab — Custom Cursor with Glow + Trailing Blur
 * Smooth lerp-based follow with a secondary trail element.
 * Performance-optimized via requestAnimationFrame + will-change.
 */
(function () {
    // Bail on touch devices
    if ('ontouchstart' in window) return;

    const glow = document.getElementById('cursor-glow');
    const trail = document.getElementById('cursor-trail');
    if (!glow || !trail) return;

    // Enable hardware acceleration
    glow.style.willChange = 'transform, opacity';
    trail.style.willChange = 'transform, opacity';

    let mouseX = 0, mouseY = 0;
    let glowX = 0, glowY = 0;
    let trailX = 0, trailY = 0;
    let visible = false;

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        if (!visible) {
            visible = true;
            glow.style.opacity = '0.85';
            trail.style.opacity = '0.6';
        }
    });

    document.addEventListener('mouseleave', () => {
        visible = false;
        glow.style.opacity = '0';
        trail.style.opacity = '0';
    });

    // Lerp constants — glow follows faster, trail lags behind
    const GLOW_SPEED = 0.18;
    const TRAIL_SPEED = 0.08;

    function animate() {
        glowX += (mouseX - glowX) * GLOW_SPEED;
        glowY += (mouseY - glowY) * GLOW_SPEED;
        trailX += (mouseX - trailX) * TRAIL_SPEED;
        trailY += (mouseY - trailY) * TRAIL_SPEED;

        glow.style.left = glowX + 'px';
        glow.style.top = glowY + 'px';
        trail.style.left = trailX + 'px';
        trail.style.top = trailY + 'px';

        requestAnimationFrame(animate);
    }
    animate();

    // Scale effect on interactive elements
    const interactiveSelectors = 'a, button, input, textarea, select, [role="button"], .btn-primary, .btn-ghost, .card-hover';

    document.addEventListener('mouseenter', (e) => {
        if (e.target.matches && e.target.matches(interactiveSelectors)) {
            glow.style.width = '26px';
            glow.style.height = '26px';
            glow.style.filter = 'blur(2px)';
            trail.style.width = '48px';
            trail.style.height = '48px';
            trail.style.filter = 'blur(10px)';
        }
    }, true);

    document.addEventListener('mouseleave', (e) => {
        if (e.target.matches && e.target.matches(interactiveSelectors)) {
            glow.style.width = '18px';
            glow.style.height = '18px';
            glow.style.filter = 'blur(1px)';
            trail.style.width = '36px';
            trail.style.height = '36px';
            trail.style.filter = 'blur(6px)';
        }
    }, true);
})();
