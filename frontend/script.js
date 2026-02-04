document.getElementById('generateForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const grade = document.getElementById('grade').value;
    const topic = document.getElementById('topic').value;

    if (!grade || !topic) return;

    // UI Reset
    document.getElementById('results').classList.add('hidden');
    document.getElementById('refinedSection').classList.add('hidden');
    document.getElementById('loading').classList.remove('hidden');

    try {
        console.log("Sending request to /generate...");
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                grade: parseInt(grade),
                topic: topic
            }),
        });

        if (!response.ok) {
            throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        // Prepare request payload for display
        const requestPayload = {
            grade: parseInt(grade),
            topic: topic
        };

        renderResults(data, requestPayload);

    } catch (error) {
        console.error("GENERATE ERROR:", error);
        let msg = "Failed to generate content. ";

        if (error.message.includes("Failed to fetch")) {
            msg += "\n\nCould not connect to the backend server (http://localhost:8000). \nPlease check:\n1. Is the backend running? (python -m backend.main)\n2. Is it blocked by a firewall?";
        } else {
            msg += error.message;
        }
        alert(msg);
    } finally {
        document.getElementById('loading').classList.add('hidden');
    }
});

// Debug Toggle
// Debug Toggle
document.getElementById('toggleDebug').addEventListener('click', () => {
    const debugPanel = document.getElementById('debugPanel');
    const btn = document.getElementById('toggleDebug');

    if (debugPanel.classList.contains('hidden')) {
        debugPanel.classList.remove('hidden');
        debugPanel.classList.add('visible');
        btn.classList.add('active');
    } else {
        debugPanel.classList.add('hidden');
        debugPanel.classList.remove('visible');
        btn.classList.remove('active');
    }
});

function renderResults(data, requestPayload) {
    const resultsSection = document.getElementById('results');
    resultsSection.classList.remove('hidden');

    // Debug Info
    document.getElementById('jsonRequest').textContent = JSON.stringify(requestPayload, null, 2);
    document.getElementById('jsonResponse').textContent = JSON.stringify(data, null, 2);

    // 1. Generator Output
    renderContent('generatorContent', data.initial_output);
    document.getElementById('genStatus').textContent = "Completed";
    document.getElementById('genStatus').className = "status-badge status-pass";

    // 2. Reviewer Output
    const reviewStatus = document.getElementById('reviewStatus');
    const reviewerContent = document.getElementById('reviewerContent');
    const reviewData = data.review_output;

    if (reviewData.status === 'pass') {
        reviewStatus.textContent = "Passed";
        reviewStatus.className = "status-badge status-pass";
        reviewerContent.innerHTML = `<p style="color: var(--success)">Content passed validation.</p>`;
    } else {
        reviewStatus.textContent = "Failed";
        reviewStatus.className = "status-badge status-fail";
        let feedbackHtml = '<p><strong>Feedback:</strong></p><ul class="feedback-list">';
        reviewData.feedback.forEach(item => {
            feedbackHtml += `<li>${item}</li>`;
        });
        feedbackHtml += '</ul>';
        reviewerContent.innerHTML = feedbackHtml;
    }

    // 3. Refined Output (if exists)
    const refinedSection = document.getElementById('refinedSection');
    if (data.refined_output) {
        refinedSection.classList.remove('hidden');
        renderContent('refinedContent', data.refined_output);
    } else {
        refinedSection.classList.add('hidden');
    }
}

function renderContent(containerId, content) {
    const container = document.getElementById(containerId);
    if (!content) {
        container.innerHTML = '<p class="error">No content available</p>';
        return;
    }

    let html = `<p><strong>Explanation:</strong> ${content.explanation}</p>`;

    if (content.mcqs && content.mcqs.length > 0) {
        html += `<h3>Multiple Choice Questions</h3>`;
        content.mcqs.forEach((mcq, index) => {
            html += `
            <div class="mcq-item">
                <p><strong>Q${index + 1}: ${mcq.question}</strong></p>
                <ul class="mcq-options">
                    ${mcq.options.map(opt => `<li>${opt}</li>`).join('')}
                </ul>
                <p style="margin-top:0.5rem; font-size:0.9em; color:var(--text-light)">Answer: ${mcq.answer}</p>
            </div>
            `;
        });
    }

    container.innerHTML = html;
}
