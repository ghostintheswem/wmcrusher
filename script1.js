const swiper = new Swiper('.mySwiper', {
    // Optional parameters
    direction: 'horizontal',
    loop: true, // Seamless looping

    // Enable Touch/Swipe control
    // This is enabled by default, but it's good to know the option exists.
    allowTouchMove: true,

    // If we need pagination (dots)
    pagination: {
        el: '.swiper-pagination',
        clickable: true, // Makes the dots clickable
    },

    // Navigation arrows
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },

    // Keyboard controls for desktop accessibility
    keyboard: {
        enabled: true,
        onlyInViewport: false,
    },
});