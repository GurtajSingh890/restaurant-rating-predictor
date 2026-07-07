/**
 * Bengaluru Restaurant Rating Predictor
 * Main JavaScript File
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // ─── Navbar Mobile Toggle ──────────────────────────────────────────
    const navToggle = document.getElementById('nav-toggle');
    const navLinks = document.getElementById('nav-links');
    const hamburger = document.querySelector('.hamburger');
    
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            if (hamburger) {
                hamburger.classList.toggle('active');
            }
        });
    }

    // ─── Sticky Navbar Effect ──────────────────────────────────────────
    const navbar = document.getElementById('main-navbar');
    
    const handleScroll = () => {
        if (window.scrollY > 20) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    };
    
    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Init on load


    // ─── Scroll Animations (Intersection Observer) ─────────────────────
    const fadeElements = document.querySelectorAll('.fade-in, .fade-in-right');
    
    const fadeOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };
    
    const fadeObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('appear');
                observer.unobserve(entry.target);
            }
        });
    }, fadeOptions);
    
    fadeElements.forEach(el => fadeObserver.observe(el));


    // ─── Form Submission Loader ────────────────────────────────────────
    const predictForm = document.getElementById('predict-form');
    const btnPredict = document.getElementById('btn-predict');
    
    if (predictForm && btnPredict) {
        predictForm.addEventListener('submit', (e) => {
            const btnText = btnPredict.querySelector('.btn-text');
            const btnLoader = btnPredict.querySelector('.btn-loader');
            
            // Basic HTML5 validation check before showing loader
            if (predictForm.checkValidity()) {
                if (btnText && btnLoader) {
                    btnText.style.display = 'none';
                    btnLoader.style.display = 'inline-block';
                }
                btnPredict.disabled = true;
                btnPredict.style.opacity = '0.8';
                btnPredict.style.cursor = 'not-allowed';
            }
        });
    }

    // ─── Auto-hide Flash Messages ──────────────────────────────────────
    const flashContainer = document.getElementById('flash-container');
    if (flashContainer) {
        const flashes = flashContainer.querySelectorAll('.flash-message');
        flashes.forEach(flash => {
            setTimeout(() => {
                flash.style.opacity = '0';
                flash.style.transform = 'translateX(100%)';
                flash.style.transition = 'all 0.4s ease-in-out';
                setTimeout(() => flash.remove(), 400);
            }, 6000);
        });
    }

});
