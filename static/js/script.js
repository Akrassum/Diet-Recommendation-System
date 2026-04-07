// =============================================================================
// script.js — AI Diet Recommendation System
// =============================================================================
// This file handles all client-side interactivity:
//   - Live BMI calculation and preview
//   - Activity card selection highlighting
//   - Form validation before submission
//   - Animated BMI pointer on result page
//   - General page enhancements
// =============================================================================

document.addEventListener("DOMContentLoaded", function () {

  // ---------------------------------------------------------------------------
  // 1. LIVE BMI PREVIEW (Form Page)
  // Calculates and displays BMI live as the user types weight/height
  // ---------------------------------------------------------------------------
  const weightInput = document.getElementById("weight");
  const heightInput = document.getElementById("height");
  const bmiPreview = document.getElementById("bmiPreview");
  const bmiValueEl = document.getElementById("bmiValue");
  const bmiCategoryEl = document.getElementById("bmiCategory");
  const bmiBarEl = document.getElementById("bmiBar");

  function calculateBMI(weight, height) {
    // BMI = weight(kg) / (height(m))^2
    const heightM = height / 100;
    return weight / (heightM * heightM);
  }

  function getBMICategory(bmi) {
    if (bmi < 18.5) return { label: "Underweight", color: "#3b82f6" };
    if (bmi < 25)   return { label: "Normal weight", color: "#10b981" };
    if (bmi < 30)   return { label: "Overweight", color: "#f97316" };
    return              { label: "Obese", color: "#ef4444" };
  }

  // BMI scale boundaries for position mapping on the visual bar
  const BMI_SCALE_MIN = 10;
  const BMI_SCALE_MAX = 40;

  /**
   * Maps a BMI value to a percentage position for the bar (0–100%).
   * Scale: BMI_SCALE_MIN (0%) → BMI_SCALE_MAX (100%)
   */
  function bmiToPercent(bmi) {
    const range = BMI_SCALE_MAX - BMI_SCALE_MIN;
    const clamped = Math.max(BMI_SCALE_MIN, Math.min(BMI_SCALE_MAX, bmi));
    return ((clamped - BMI_SCALE_MIN) / range) * 100;
  }

  function updateBMIPreview() {
    if (!weightInput || !heightInput || !bmiPreview) return;
    const weight = parseFloat(weightInput.value);
    const height = parseFloat(heightInput.value);

    if (weight > 0 && height > 0) {
      const bmi = calculateBMI(weight, height);
      const { label, color } = getBMICategory(bmi);
      const pct = bmiToPercent(bmi);

      bmiPreview.style.display = "block";
      bmiValueEl.textContent = bmi.toFixed(1);
      bmiValueEl.style.color = color;
      bmiCategoryEl.textContent = label;
      bmiCategoryEl.style.color = color;
      bmiBarEl.style.width = pct + "%";
      bmiBarEl.style.background = color;
    } else {
      bmiPreview.style.display = "none";
    }
  }

  if (weightInput) weightInput.addEventListener("input", updateBMIPreview);
  if (heightInput) heightInput.addEventListener("input", updateBMIPreview);

  // ---------------------------------------------------------------------------
  // 2. ACTIVITY CARD SELECTION (Form Page)
  // Adds visual feedback when an activity level card is selected
  // ---------------------------------------------------------------------------
  const activityOptions = document.querySelectorAll(".activity-option");
  activityOptions.forEach(function (option) {
    const radio = option.querySelector("input[type='radio']");
    if (radio && radio.checked) {
      option.querySelector(".activity-card").classList.add("selected");
    }
    radio && radio.addEventListener("change", function () {
      activityOptions.forEach(function (o) {
        o.querySelector(".activity-card").classList.remove("selected");
      });
      if (this.checked) {
        option.querySelector(".activity-card").classList.add("selected");
      }
    });
  });

  // ---------------------------------------------------------------------------
  // 3. FORM VALIDATION (Form Page)
  // Validates inputs before submitting, shows friendly error messages
  // ---------------------------------------------------------------------------
  const dietForm = document.getElementById("dietForm");
  const submitBtn = document.getElementById("submitBtn");

  if (dietForm) {
    dietForm.addEventListener("submit", function (e) {
      const age = parseFloat(document.getElementById("age").value);
      const weight = parseFloat(document.getElementById("weight").value);
      const height = parseFloat(document.getElementById("height").value);
      const gender = document.getElementById("gender").value;

      let errors = [];

      if (!gender) errors.push("Please select your gender.");
      if (!age || age < 1 || age > 120) errors.push("Age must be between 1 and 120.");
      if (!weight || weight < 20 || weight > 300) errors.push("Weight must be between 20 and 300 kg.");
      if (!height || height < 100 || height > 250) errors.push("Height must be between 100 and 250 cm.");

      if (errors.length > 0) {
        e.preventDefault();
        showFormError(errors.join(" "));
        return;
      }

      // Show loading state on button
      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analysing...';
      submitBtn.disabled = true;
    });
  }

  function showFormError(message) {
    // Remove any existing alert
    const existing = document.querySelector(".alert-js");
    if (existing) existing.remove();

    const alert = document.createElement("div");
    alert.className = "alert alert-error alert-js";
    alert.style.margin = "1rem 2rem";
    alert.innerHTML = '<i class="fas fa-exclamation-circle"></i> ' + message;

    const form = document.querySelector(".diet-form");
    if (form) form.insertBefore(alert, form.firstChild);

    // Scroll to error
    alert.scrollIntoView({ behavior: "smooth", block: "center" });

    // Auto-dismiss after 5 seconds
    setTimeout(function () { alert.remove(); }, 5000);
  }

  // ---------------------------------------------------------------------------
  // 4. BMI POINTER ANIMATION (Result Page)
  // Positions the BMI pointer arrow on the visual bar
  // ---------------------------------------------------------------------------
  const bmiPointer = document.getElementById("bmiPointer");
  if (bmiPointer) {
    const bmiVal = parseFloat(bmiPointer.getAttribute("data-bmi"));
    if (!isNaN(bmiVal)) {
      // Map BMI to percentage using the same scale as the visual bar
      const pct = Math.max(0, Math.min(100,
        ((bmiVal - BMI_SCALE_MIN) / (BMI_SCALE_MAX - BMI_SCALE_MIN)) * 100
      ));
      // Animate pointer into position
      setTimeout(function () {
        bmiPointer.style.left = pct + "%";
        bmiPointer.style.transition = "left 1s ease";
      }, 300);
      bmiPointer.style.left = "0%";
    }
  }

  // ---------------------------------------------------------------------------
  // 5. ANIMATED BMI COUNTER (Result Page)
  // Counts up the BMI number for a nice entrance effect
  // ---------------------------------------------------------------------------
  const bmiDisplay = document.getElementById("bmiDisplay");
  if (bmiDisplay) {
    const target = parseFloat(bmiDisplay.textContent);
    if (!isNaN(target)) {
      let current = 0;
      const duration = 1000; // ms
      const steps = 50;
      const increment = target / steps;
      const interval = duration / steps;

      bmiDisplay.textContent = "0.0";
      const timer = setInterval(function () {
        current += increment;
        if (current >= target) {
          current = target;
          clearInterval(timer);
        }
        bmiDisplay.textContent = current.toFixed(1);
      }, interval);
    }
  }

  // ---------------------------------------------------------------------------
  // 6. SMOOTH SCROLL for anchor links (Home Page)
  // ---------------------------------------------------------------------------
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener("click", function (e) {
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  // ---------------------------------------------------------------------------
  // 7. SCROLL-IN ANIMATIONS
  // Fade in cards as they scroll into the viewport
  // ---------------------------------------------------------------------------
  const animatedEls = document.querySelectorAll(
    ".feature-card, .step, .diet-card, .summary-card, .meal-item, .tip-card, .stat-item"
  );

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  animatedEls.forEach(function (el) {
    el.style.opacity = "0";
    el.style.transform = "translateY(20px)";
    el.style.transition = "opacity 0.5s ease, transform 0.5s ease";
    observer.observe(el);
  });

});
