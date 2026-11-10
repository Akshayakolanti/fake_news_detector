document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const navButtons = document.querySelectorAll('.nav-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    const modeTextBtn = document.getElementById('mode-text-btn');
    const modeUrlBtn = document.getElementById('mode-url-btn');
    const textSection = document.getElementById('text-input-section');
    const urlSection = document.getElementById('url-input-section');
    const textInput = document.getElementById('news-text-input');
    const urlInput = document.getElementById('news-url-input');
    const presetChips = document.querySelectorAll('.preset-chip');
    const clearBtn = document.getElementById('clear-input-btn');
    const analyzeBtn = document.getElementById('analyze-news-btn');
    const loader = document.getElementById('analysis-loader');
    const resultsDashboard = document.getElementById('results-dashboard');

    // Result elements
    const verdictBadge = document.getElementById('verdict-badge-tag');
    const confidenceBadge = document.getElementById('confidence-badge');
    const truthGauge = document.getElementById('truth-gauge');
    const truthScoreDisplay = document.getElementById('truth-score-display');
    const realPercentVal = document.getElementById('real-percent-val');
    const fakePercentVal = document.getElementById('fake-percent-val');
    const sensationScoreVal = document.getElementById('sensation-score-val');
    const relatedArticlesGrid = document.getElementById('related-articles-grid');
    const highlightedTextContent = document.getElementById('highlighted-text-content');
    const riskChecklist = document.getElementById('risk-checklist');

    let currentMode = 'text';

    // Tab Switching
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            navButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(targetTab).classList.add('active');

            if (targetTab === 'trending-tab') {
                loadTrendingNews();
            }
        });
    });

    // Mode Switching (Text vs URL)
    modeTextBtn.addEventListener('click', () => {
        currentMode = 'text';
        modeTextBtn.classList.add('active');
        modeUrlBtn.classList.remove('active');
        textSection.classList.remove('hidden');
        urlSection.classList.add('hidden');
    });

    modeUrlBtn.addEventListener('click', () => {
        currentMode = 'url';
        modeUrlBtn.classList.add('active');
        modeTextBtn.classList.remove('active');
        urlSection.classList.remove('hidden');
        textSection.classList.add('hidden');
    });

    // Quick Presets
    presetChips.forEach(chip => {
        chip.addEventListener('click', () => {
            const sampleText = chip.getAttribute('data-sample');
            currentMode = 'text';
            modeTextBtn.click();
            textInput.value = sampleText;
            analyzeNews();
        });
    });

    clearBtn.addEventListener('click', () => {
        textInput.value = '';
        urlInput.value = '';
        resultsDashboard.classList.add('hidden');
    });

    // Analyze Click Handler
    analyzeBtn.addEventListener('click', analyzeNews);

    async function analyzeNews() {
        let payload = {};
        let endpoint = '/api/predict';

        if (currentMode === 'text') {
            const text = textInput.value.strip ? textInput.value.strip() : textInput.value.trim();
            if (!text) {
                alert('Please enter or paste news text to analyze!');
                return;
            }
            payload = { text };
        } else {
            const url = urlInput.value.trim();
            if (!url) {
                alert('Please enter a news article URL!');
                return;
            }
            payload = { url };
            endpoint = '/api/analyze-url';
        }

        // Show loader
        resultsDashboard.classList.add('hidden');
        loader.classList.remove('hidden');
        analyzeBtn.disabled = true;

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            loader.classList.add('hidden');
            analyzeBtn.disabled = false;

            if (response.ok) {
                renderResults(data);
            } else {
                alert(data.error || 'Failed to analyze news.');
            }
        } catch (err) {
            console.error(err);
            loader.classList.add('hidden');
            analyzeBtn.disabled = false;
            alert('Server connection error. Make sure Python Flask app is running!');
        }
    }

    function renderResults(data) {
        resultsDashboard.classList.remove('hidden');

        // Verdict Badge
        verdictBadge.textContent = data.verdict_code === 'REAL' ? 'AUTHENTIC REAL NEWS' : (data.verdict_code === 'UNCERTAIN' ? 'SUSPICIOUS / UNVERIFIED' : 'LIKELY FAKE NEWS');
        verdictBadge.style.color = data.status_color;
        verdictBadge.style.borderColor = data.status_color;
        verdictBadge.style.backgroundColor = `${data.status_color}25`;

        confidenceBadge.textContent = data.confidence_badge;

        // Animate Gauge
        const realPercent = data.real_percentage;
        truthScoreDisplay.textContent = `${realPercent}%`;
        truthGauge.style.background = `conic-gradient(${data.status_color} ${realPercent * 3.6}deg, rgba(255, 255, 255, 0.05) 0deg)`;

        // Score metrics
        realPercentVal.textContent = `${data.real_percentage}%`;
        fakePercentVal.textContent = `${data.fake_percentage}%`;
        sensationScoreVal.textContent = `${data.sensationalism_score}/100`;

        // Render Highlighted Text
        highlightedTextContent.innerHTML = data.highlighted_text || textInput.value;

        // Render Related Real News Articles Grid
        renderRelatedNews(data.related_real_news || []);

        // Render Risk Checklist
        renderRiskChecklist(data);

        // Scroll smoothly to results
        resultsDashboard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function renderRelatedNews(articles) {
        relatedArticlesGrid.innerHTML = '';
        
        if (!articles || articles.length === 0) {
            relatedArticlesGrid.innerHTML = '<p style="color: var(--text-muted);">No related verified articles found.</p>';
            return;
        }

        articles.forEach(art => {
            const card = document.createElement('div');
            card.className = 'news-article-card';
            card.innerHTML = `
                <div>
                    <div class="news-meta">
                        <span><i class="fa-solid fa-building-columns"></i> ${art.source}</span>
                        <span><i class="fa-regular fa-clock"></i> ${art.published}</span>
                    </div>
                    <a href="${art.link}" target="_blank" class="news-title-link">
                        ${art.title}
                    </a>
                </div>
                <a href="${art.link}" target="_blank" class="read-btn">
                    Read Verified Coverage <i class="fa-solid fa-arrow-up-right-from-square"></i>
                </a>
            `;
            relatedArticlesGrid.appendChild(card);
        });
    }

    function renderRiskChecklist(data) {
        riskChecklist.innerHTML = '';

        const checks = [
            {
                condition: data.real_percentage >= 70,
                text: `Machine Learning Confidence: ${data.real_percentage}% Real News pattern match.`,
                isGood: true
            },
            {
                condition: data.sensationalism_score < 30,
                text: `Low Clickbait Index (${data.sensationalism_score}/100) - Tone is objective and factual.`,
                isGood: true
            },
            {
                condition: data.sensational_details.flagged_words.length > 0,
                text: `Sensational keywords found: ${data.sensational_details.flagged_words.join(', ')}`,
                isGood: false
            },
            {
                condition: data.sensational_details.caps_percentage > 15,
                text: `High ALL-CAPS ratio (${data.sensational_details.caps_percentage}%) detected.`,
                isGood: false
            },
            {
                condition: data.related_real_news && data.related_real_news.length > 0,
                text: `Cross-referenced with ${data.related_real_news.length} verified news sources on Google News.`,
                isGood: true
            }
        ];

        checks.forEach(chk => {
            const li = document.createElement('li');
            li.className = `risk-item ${chk.isGood ? 'success' : 'danger'}`;
            li.innerHTML = `
                <i class="fa-solid ${chk.isGood ? 'fa-circle-check' : 'fa-triangle-exclamation'}"></i>
                <span>${chk.text}</span>
            `;
            riskChecklist.appendChild(li);
        });
    }

    async function loadTrendingNews() {
        const grid = document.getElementById('trending-news-grid');
        grid.innerHTML = '<p class="loader-text">Loading trending news feed...</p>';

        try {
            const res = await fetch('/api/trending');
            const newsList = await res.json();
            grid.innerHTML = '';

            newsList.forEach(item => {
                const card = document.createElement('div');
                card.className = 'trending-card glass-panel';
                card.innerHTML = `
                    <div>
                        <div class="trending-card-header">
                            <span class="category-tag">${item.category}</span>
                            <span class="verdict-badge" style="font-size: 11px; padding: 2px 10px; color: ${item.status_color}; border-color: ${item.status_color}; background: ${item.status_color}20">
                                ${item.verdict_code} (${item.real_percentage}% Real)
                            </span>
                        </div>
                        <h4 class="trending-title">${item.title}</h4>
                        <p class="trending-summary">${item.summary}</p>
                    </div>
                    <button class="preset-chip" style="align-self: flex-start;" onclick="testTrendingSample('${encodeURIComponent(item.title)}')">
                        <i class="fa-solid fa-magnifying-glass"></i> Deep Analyze
                    </button>
                `;
                grid.appendChild(card);
            });
        } catch (e) {
            grid.innerHTML = '<p class="loader-text">Failed to load trending news.</p>';
        }
    }

    window.testTrendingSample = function(encodedTitle) {
        const title = decodeURIComponent(encodedTitle);
        document.querySelector('[data-tab="detector-tab"]').click();
        modeTextBtn.click();
        textInput.value = title;
        analyzeNews();
    };
});
