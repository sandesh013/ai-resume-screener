document.addEventListener("DOMContentLoaded", function () {
    const rootStyles = getComputedStyle(document.documentElement);
    const theme = {
        primary: readVar(rootStyles, "--accent-primary", "#6366f1"),
        success: readVar(rootStyles, "--accent-success", "#10b981"),
        warning: readVar(rootStyles, "--accent-highlight", "#f59e0b"),
        danger: readVar(rootStyles, "--accent-danger", "#ef4444"),
        text: readVar(rootStyles, "--text-primary", "#1e1b4b"),
        muted: readVar(rootStyles, "--text-muted", "#6b7280"),
        line: readVar(rootStyles, "--border-color", "rgba(99, 102, 241, 0.12)")
    };

    if (window.Chart) {
        window.Chart.defaults.font.family = '"Plus Jakarta Sans", sans-serif';
        window.Chart.defaults.color = theme.muted;
    }

    setupResumeUpload();
    setupRegisterValidation();
    setupScoreCircles();
    setupScoreBars();
    setupSkillCopy();
    setupTrendChart(theme);
    setupAtsChart(theme);
    setupAlerts();
    setupSmoothScroll();
    setupPrinting();
    setupScrollReveal();
});

function readVar(styles, name, fallback) {
    const value = styles.getPropertyValue(name).trim();
    return value || fallback;
}

function setupResumeUpload() {
    const resumeInput = document.getElementById("resumeFile");
    const uploadForm = document.getElementById("uploadForm");
    const submitBtn = document.getElementById("submitBtn");
    const fileInfo = document.getElementById("fileInfo");
    const uploadZone = document.querySelector(".upload-zone");

    if (resumeInput) {
        resumeInput.addEventListener("change", function () {
            updateResumePreview(resumeInput, fileInfo);
        });
    }

    if (uploadZone && resumeInput) {
        ["dragenter", "dragover"].forEach(function (eventName) {
            uploadZone.addEventListener(eventName, function (event) {
                event.preventDefault();
                uploadZone.classList.add("drag-over");
            });
        });

        ["dragleave", "dragend"].forEach(function (eventName) {
            uploadZone.addEventListener(eventName, function () {
                uploadZone.classList.remove("drag-over");
            });
        });

        uploadZone.addEventListener("drop", function (event) {
            event.preventDefault();
            uploadZone.classList.remove("drag-over");

            if (!event.dataTransfer || !event.dataTransfer.files.length) {
                return;
            }

            resumeInput.files = event.dataTransfer.files;
            resumeInput.dispatchEvent(new Event("change"));
        });
    }

    if (uploadForm) {
        uploadForm.addEventListener("submit", function (event) {
            const jdText = document.getElementById("jdText");
            const jdFile = document.getElementById("jdFile");

            if (!resumeInput || !resumeInput.files[0]) {
                event.preventDefault();
                showAlert("danger", "Please upload a resume file.");
                return;
            }

            const hasJdText = jdText && jdText.value.trim().length > 0;
            const hasJdFile = jdFile && jdFile.files[0];

            if (!hasJdText && !hasJdFile) {
                event.preventDefault();
                showAlert("danger", "Please provide a job description as text or file.");
                return;
            }

            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Analyzing...';
            }

            showProgressOverlay();
        });
    }
}

function updateResumePreview(input, target) {
    if (!target) {
        return;
    }

    const file = input.files && input.files[0];
    if (!file) {
        target.innerHTML = "";
        return;
    }

    const extension = file.name.split(".").pop().toLowerCase();
    const allowed = ["pdf", "doc", "docx"];
    const sizeMb = (file.size / (1024 * 1024)).toFixed(2);

    if (!allowed.includes(extension)) {
        showAlert("danger", "Invalid file type. Please upload PDF, DOC, or DOCX.");
        input.value = "";
        target.innerHTML = "";
        return;
    }

    if (file.size > 16 * 1024 * 1024) {
        showAlert("danger", "File too large. Maximum size is 16 MB.");
        input.value = "";
        target.innerHTML = "";
        return;
    }

    target.innerHTML = `
        <div class="file-preview">
            <i class="bi bi-file-earmark-check-fill"></i>
            <div>
                <strong>${escapeHtml(file.name)}</strong>
                <div class="table-subtext">${sizeMb} MB ready for analysis</div>
            </div>
        </div>
    `;
}

function setupRegisterValidation() {
    const registerForm = document.getElementById("registerForm");
    if (!registerForm) {
        return;
    }

    registerForm.addEventListener("submit", function (event) {
        const password = document.getElementById("password");
        const confirm = document.getElementById("confirm_password");

        if (!password || !confirm) {
            return;
        }

        if (password.value.length < 6) {
            event.preventDefault();
            showAlert("danger", "Password must be at least 6 characters long.");
            return;
        }

        if (password.value !== confirm.value) {
            event.preventDefault();
            showAlert("danger", "Passwords do not match.");
        }
    });
}

function setupScoreCircles() {
    document.querySelectorAll(".score-circle").forEach(function (circle) {
        const score = parseFloat(circle.dataset.score || "0");
        const radius = 54;
        const circumference = 2 * Math.PI * radius;
        const offset = circumference - (score / 100) * circumference;
        const progressRing = circle.querySelector(".progress-ring-circle");
        const scoreText = circle.querySelector(".score-text");

        if (progressRing) {
            progressRing.style.strokeDasharray = circumference;
            progressRing.style.strokeDashoffset = circumference;

            setTimeout(function () {
                progressRing.style.transition = "stroke-dashoffset 1.4s ease";
                progressRing.style.strokeDashoffset = offset;
            }, 220);
        }

        if (scoreText) {
            animateNumber(scoreText, 0, score, 1400);
        }
    });
}

function setupScoreBars() {
    const scoreBars = document.querySelectorAll(".score-bar-fill");
    if (!scoreBars.length || typeof IntersectionObserver === "undefined") {
        scoreBars.forEach(function (bar) {
            bar.style.width = `${bar.dataset.width || 0}%`;
        });
        return;
    }

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (!entry.isIntersecting) {
                return;
            }

            const bar = entry.target;
            bar.style.transition = "width 1.2s ease";
            bar.style.width = `${bar.dataset.width || 0}%`;
            observer.unobserve(bar);
        });
    }, { threshold: 0.15 });

    scoreBars.forEach(function (bar) {
        observer.observe(bar);
    });
}

function setupSkillCopy() {
    document.querySelectorAll(".skill-tag").forEach(function (tag) {
        tag.title = "Click to copy";
        tag.style.cursor = "pointer";

        tag.addEventListener("click", function () {
            const text = tag.textContent.trim();

            if (!navigator.clipboard || !window.isSecureContext) {
                showToast(`Skill: ${text}`);
                return;
            }

            navigator.clipboard.writeText(text).then(function () {
                showToast(`Copied: ${text}`);
            }).catch(function () {
                showToast(`Skill: ${text}`);
            });
        });
    });
}

function setupTrendChart(theme) {
    const trendCanvas = document.getElementById("trendChart");
    if (!trendCanvas || !window.Chart) {
        return;
    }

    const labels = JSON.parse(trendCanvas.dataset.labels || "[]");
    const scores = JSON.parse(trendCanvas.dataset.scores || "[]");
    const context = trendCanvas.getContext("2d");
    const fill = context.createLinearGradient(0, 0, 0, 320);

    fill.addColorStop(0, "rgba(99, 102, 241, 0.2)");
    fill.addColorStop(1, "rgba(99, 102, 241, 0.01)");

    new Chart(trendCanvas, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Compatibility",
                data: scores,
                borderColor: theme.primary,
                backgroundColor: fill,
                borderWidth: 3,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: theme.primary,
                pointBorderColor: "#fff",
                pointBorderWidth: 2,
                tension: 0.38,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: theme.text,
                        usePointStyle: true,
                        boxWidth: 10
                    }
                },
                tooltip: {
                    backgroundColor: "rgba(255, 255, 255, 0.96)",
                    titleColor: theme.text,
                    bodyColor: theme.text,
                    borderColor: theme.line,
                    borderWidth: 1,
                    displayColors: false,
                    callbacks: {
                        label: function (context) {
                            return `${context.parsed.y}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    min: 0,
                    max: 100,
                    ticks: {
                        color: theme.muted,
                        callback: function (value) {
                            return `${value}%`;
                        }
                    },
                    grid: {
                        color: "rgba(99, 102, 241, 0.07)"
                    }
                },
                x: {
                    ticks: {
                        color: theme.muted
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function setupAtsChart(theme) {
    const atsCanvas = document.getElementById("atsChart");
    if (!atsCanvas || !window.Chart) {
        return;
    }

    const score = parseFloat(atsCanvas.dataset.score || "0");
    let activeColor = theme.danger;

    if (score >= 70) {
        activeColor = theme.success;
    } else if (score >= 40) {
        activeColor = theme.warning;
    }

    new Chart(atsCanvas, {
        type: "doughnut",
        data: {
            labels: ["Score", "Remaining"],
            datasets: [{
                data: [score, 100 - score],
                backgroundColor: [activeColor, "rgba(99, 102, 241, 0.08)"],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "78%",
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        }
    });
}

function setupAlerts() {
    document.querySelectorAll(".alert-dismissible").forEach(function (alert) {
        setTimeout(function () {
            const instance = bootstrap.Alert.getOrCreateInstance(alert);
            instance.close();
        }, 5000);
    });
}

function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener("click", function (event) {
            const target = document.querySelector(anchor.getAttribute("href"));
            if (!target) {
                return;
            }

            event.preventDefault();
            target.scrollIntoView({ behavior: "smooth", block: "start" });
        });
    });
}

function setupPrinting() {
    const printButton = document.getElementById("printResults");
    if (!printButton) {
        return;
    }

    printButton.addEventListener("click", function () {
        window.print();
    });
}

function animateNumber(element, start, end, duration) {
    const range = end - start;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = start + range * eased;
        element.textContent = `${Math.round(current * 10) / 10}%`;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

function showAlert(type, message) {
    const container = document.querySelector(".alert-container") || document.querySelector(".page-content .container");
    if (!container) {
        return;
    }

    const alert = document.createElement("div");
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        <div class="d-flex align-items-start gap-2">
            <i class="bi bi-info-circle-fill"></i>
            <span>${escapeHtml(message)}</span>
        </div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    container.prepend(alert);

    setTimeout(function () {
        if (alert.parentNode) {
            bootstrap.Alert.getOrCreateInstance(alert).close();
        }
    }, 5000);
}

function showToast(message) {
    const toast = document.createElement("div");
    toast.className = "toast-notification";
    toast.textContent = message;
    document.body.appendChild(toast);

    requestAnimationFrame(function () {
        toast.classList.add("show");
    });

    setTimeout(function () {
        toast.classList.remove("show");
        setTimeout(function () {
            toast.remove();
        }, 250);
    }, 1800);
}

function showProgressOverlay() {
    const overlay = document.createElement("div");
    overlay.id = "progressOverlay";
    overlay.innerHTML = `
        <div class="progress-content">
            <div class="spinner-grow text-success mb-3" role="status" aria-hidden="true"></div>
            <h5>Analyzing your resume</h5>
            <p class="text-muted mt-2 mb-3">Extracting text, comparing role fit, and preparing recommendations.</p>
            <div class="progress mt-3" style="height: 8px;">
            <div class="progress-bar progress-bar-striped progress-bar-animated" id="analysisProgress" style="width: 0%; background: linear-gradient(135deg, #6366f1, #06b6d4);"></div>
            </div>
            <p class="text-muted mt-3 small" id="progressStatus">Preparing files...</p>
        </div>
    `;

    document.body.appendChild(overlay);

    const steps = [
        { pct: 18, text: "Extracting text from the resume..." },
        { pct: 38, text: "Reading the target role..." },
        { pct: 58, text: "Calculating compatibility and skill overlap..." },
        { pct: 78, text: "Running ATS checks..." },
        { pct: 92, text: "Generating recommendations..." }
    ];

    steps.forEach(function (step, index) {
        setTimeout(function () {
            const progress = document.getElementById("analysisProgress");
            const status = document.getElementById("progressStatus");

            if (progress) {
                progress.style.width = `${step.pct}%`;
            }

            if (status) {
                status.textContent = step.text;
            }
        }, (index + 1) * 950);
    });
}

function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, function (char) {
        return {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#039;"
        }[char];
    });
}

function setupScrollReveal() {
    var targets = document.querySelectorAll(
        ".panel-card, .feature-card, .stat-card, .metric-card, .snapshot-card, " +
        ".rec-card, .auth-shell, .editorial-panel, .cta-band, .section-heading, " +
        ".page-hero, .hero-showcase, .fade-up"
    );

    if (!targets.length || typeof IntersectionObserver === "undefined") {
        return;
    }

    targets.forEach(function (el) {
        if (!el.classList.contains("fade-up")) {
            el.classList.add("fade-up");
        }
    });

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.08, rootMargin: "0px 0px -40px 0px" });

    targets.forEach(function (el) {
        observer.observe(el);
    });
}
