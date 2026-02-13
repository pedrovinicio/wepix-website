(function () {
    var ua = navigator.userAgent || navigator.vendor || window.opera;
    var isIOS = /iPad|iPhone|iPod/.test(ua) && !window.MSStream;
    var isAndroid = /android/i.test(ua);

    var appStoreButtons = document.querySelectorAll('.app-store-btn');
    var playStoreButtons = document.querySelectorAll('.play-store-btn');

    if (isIOS) {
        playStoreButtons.forEach(function (btn) { btn.style.display = 'none'; });
    } else if (isAndroid) {
        appStoreButtons.forEach(function (btn) { btn.style.display = 'none'; });
    }
})();
