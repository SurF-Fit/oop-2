const slider = document.querySelector('.slider');
    const prevButton = document.querySelector('.prev-button');
    const nextButton = document.querySelector('.next-button');
    const slides = Array.from(document.querySelectorAll('.slide'));
    let slideIndex = 0;

    const updateSlider = () => {
        const imageWidth = slider.clientWidth;
        const slideOffset = -slideIndex * imageWidth / 4;
        slider.style.transform = `translateX(${slideOffset}px)`;
    };

    prevButton.addEventListener('click', () => {
        slideIndex = (slideIndex - 1 + slides.length) % slides.length;
        updateSlider();
    });

    nextButton.addEventListener('click', () => {
        slideIndex = (slideIndex + 1) % slides.length;
        updateSlider();
    });

    window.addEventListener('load', updateSlider);