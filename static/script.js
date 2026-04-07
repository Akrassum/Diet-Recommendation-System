/**
 * script.js — DietAI Frontend Logic
 *
 * Features:
 *  1. Live BMI preview on the form page as the user types.
 *  2. Client-side form validation with friendly error messages.
 *  3. Loading spinner on form submission.
 */

// ── Live BMI Preview ──────────────────────────────────────────────────────────
(function initBMIPreview() {
  const weightInput = document.getElementById("weight");
  const heightInput = document.getElementById("height");
  const bmiPreview = document.getElementById("bmiPreview");
  const bmiValue = document.getElementById("bmiValue");
  const bmiLabel = document.getElementById("bmiLabel");

  if (!weightInput || !heightInput) return;

  function calcBMI() {
    const w = parseFloat(weightInput.value);
    const h = parseFloat(heightInput.value) / 100;

    if (w > 0 && h > 0) {
      const bmi = (w / (h * h)).toFixed(1);
      bmiValue.textContent = bmi;
      bmiLabel.textContent = getBMICategory(parseFloat(bmi));
      bmiPreview.classList.remove("hidden");
    } else {
      bmiPreview.classList.add("hidden");
    }
  }

  function getBMICategory(bmi) {
    if (bmi < 18.5) return "Underweight";
    if (bmi < 25)   return "Normal weight";
    if (bmi < 30)   return "Overweight";
    return "Obese";
  }

  weightInput.addEventListener("input", calcBMI);
  heightInput.addEventListener("input", calcBMI);
})();


// ── Form Validation ───────────────────────────────────────────────────────────
(function initFormValidation() {
  const form = document.getElementById("dietForm");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    const age = parseInt(document.getElementById("age").value, 10);
    const weight = parseFloat(document.getElementById("weight").value);
    const height = parseFloat(document.getElementById("height").value);

    let error = "";

    if (!age || age < 1 || age > 120) {
      error = "Please enter a valid age between 1 and 120.";
    } else if (!weight || weight < 10 || weight > 300) {
      error = "Please enter a valid weight between 10 and 300 kg.";
    } else if (!height || height < 50 || height > 250) {
      error = "Please enter a valid height between 50 and 250 cm.";
    }

    if (error) {
      e.preventDefault();
      showAlert(error);
      return;
    }

    // Show loading state
    const btn = document.getElementById("submitBtn");
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing…';
    }
  });

  function showAlert(message) {
    let alertEl = document.querySelector(".alert-error");
    if (!alertEl) {
      alertEl = document.createElement("div");
      alertEl.className = "alert alert-error";
      form.insertBefore(alertEl, form.firstChild);
    }
    alertEl.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    alertEl.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
})();


// ── Scroll-reveal animation for feature cards ─────────────────────────────────
(function initScrollReveal() {
  const cards = document.querySelectorAll(".feature-card, .step, .meal-card, .stat-card");
  if (!cards.length) return;

  const observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.style.opacity = "1";
          entry.target.style.transform = "translateY(0)";
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );

  cards.forEach(function (card) {
    card.style.opacity = "0";
    card.style.transform = "translateY(20px)";
    card.style.transition = "opacity 0.4s ease, transform 0.4s ease";
    observer.observe(card);
  });
})();
