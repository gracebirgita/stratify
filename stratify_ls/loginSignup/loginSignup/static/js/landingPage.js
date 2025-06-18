console.log("landingPage.js loaded");

document.addEventListener('DOMContentLoaded', () =>{
    const totalBusinessEl = document.querySelector('.tB');
    const totalTransactionEl = document.querySelector('.tT');
    const totalInvestorEl = document.querySelector('.tI');

   // Parse integers 
    const totalBusiness = parseInt(totalBusinessEl.textContent.replace('+', ''));
    const totalTransaction = parseInt(totalTransactionEl.textContent.replace('+', ''));
    const totalInvestor = parseInt(totalInvestorEl.textContent.replace('+', ''));

    function animateCounter(element,target){
        let current = 0;
        const increment = Math.ceil(target / 100);
            const interval = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(interval);
            }
            element.textContent = `${current}+`;
            },20 ); //ms
        };

        animateCounter(totalBusinessEl, totalBusiness);
        animateCounter(totalTransactionEl, totalTransaction);
        animateCounter(totalInvestorEl, totalInvestor);
        console.log('test123')
});

document.addEventListener('DOMContentLoaded', () =>{
    const images = document.querySelectorAll(".slider-image");
    const descriptions = document.querySelectorAll(".desc-header, .desc-header-hidden");
    const rightItems = document.querySelectorAll(".right-bot > div");
    const indicator = document.querySelector(".left-bot h1");
    const btnLeft = document.querySelector(".fa-arrow-left");
    const btnRight = document.querySelector(".fa-arrow-right");
    
    let currentIndex = 0;
    const totalSlides = images.length;

    function updateSlider(index) {
        images.forEach((img, i) => {
            img.classList.toggle("active", i === index);
            img.classList.toggle("hidden", i !== index);
        });

        descriptions.forEach((desc, i) => {
            desc.style.display = i === index ? "block" : "none";
        });

        rightItems.forEach((item, i) => {
            item.style.opacity = (totalSlides - 1 - i === index) ? "1" : "0.4";
        });

        indicator.textContent = `${index + 1}/${totalSlides}`;
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % totalSlides;
        updateSlider(currentIndex);
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        updateSlider(currentIndex);
    }

    // Auto-slide every 5 seconds
    let autoSlide = setInterval(nextSlide, 5000);

    btnRight.addEventListener("click", () => {
        nextSlide();
        resetAutoSlide();
    });

    btnLeft.addEventListener("click", () => {
        prevSlide();
        resetAutoSlide();
    });

    function resetAutoSlide() {
        clearInterval(autoSlide);
        autoSlide = setInterval(nextSlide, 5000);
    }

    // Initial display
    updateSlider(currentIndex);

});

