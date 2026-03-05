document.querySelectorAll('.app-store-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
        gtag('event', 'cta_click', {
            platform: 'ios',
            location: btn.closest('.hero') ? 'hero' : 'cta_section'
        });
    });
});

document.querySelectorAll('.play-store-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
        gtag('event', 'cta_click', {
            platform: 'android',
            location: btn.closest('.hero') ? 'hero' : 'cta_section'
        });
    });
});
