const API_BASE = window.location.origin;

class ReleaseNotesApp {
    constructor() {
        this.currentJobId = null;
        this.wsConnection = null;
    }

    init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }

    setup() {
        this.bindEvents();
        this.loadRecentJobs();
        this.loadRepositories();
    }

    bindEvents() {
        const generateBtn = document.getElementById('generateBtn');
        const inputType = document.getElementById('inputType');

        if (generateBtn) {
            generateBtn.addEventListener('click', () => this.generateReleaseNotes());
        }

        if (inputType) {
            inputType.addEventListener('change', () => this.toggleInputType());
        }

        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                this.switchTab(tab.dataset.tab);
            });
        });
    }

    toggleInputType() {
        const inputType = document.getElementById('inputType').value;
        const jqlEditor = document.getElementById('jqlEditor');
        const taskInput = document.getElementById('jiraInput');
        const taskInputGroup = document.getElementById('jiraInput').parentElement;
        const jqlEditorGroup = document.getElementById('jqlEditor');

        if (inputType === 'jql') {
            taskInputGroup.style.display = 'none';
            jqlEditorGroup.style.display = 'block';
        } else if (inputType === 'multiple') {
            taskInputGroup.style.display = 'block';
            jqlEditorGroup.style.display = 'none';
            taskInput.placeholder = 'Enter multiple task numbers (comma-separated, e.g., PRND-1234, PRND-1235)';
        } else {
            taskInputGroup.style.display = 'block';
            jqlEditorGroup.style.display = 'none';
            taskInput.placeholder = 'Enter Jira task number (e.g., PRND-1234)';
        }
    }

    switchTab(tabName) {
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
            if (tab.dataset.tab === tabName) {
                tab.classList.add('active');
            }
        });

        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
            if (content.id === `${tabName}Content`) {
                content.classList.add('active');
            }
        });
    }

    async generateReleaseNotes() {
        const inputType = document.getElementById('inputType').value;
        let jiraInput = '';
        
        if (inputType === 'jql') {
            jiraInput = document.getElementById('jqlQuery').value.trim();
            if (!jiraInput) {
                this.showAlert('Please enter a JQL query', 'error');
                return;
            }
        } else {
            jiraInput = document.getElementById('jiraInput').value.trim();
            if (!jiraInput) {
                this.showAlert('Please enter a Jira task number', 'error');
                return;
            }
        }

        const version = document.getElementById('version').value.trim();
        const releaseDate = document.getElementById('releaseDate').value;
        const author = document.getElementById('author').value.trim();
        const releaseName = document.getElementById('releaseName').value.trim();

        const request = {
            jira_input: jiraInput,
            input_type: inputType === 'multiple' ? 'task' : inputType
        };

        if (version) request.version = version;
        if (releaseDate) request.release_date = releaseDate;
        if (author) request.author = author;
        if (releaseName) request.release_name = releaseName;

        try {
            const response = await fetch(`${API_BASE}/api/release-notes/generate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(request)
            });

            const data = await response.json();

            if (data.success) {
                this.currentJobId = data.data.job_id;
                this.connectWebSocket(data.data.job_id);
                this.switchTab('progress');
            } else {
                this.showAlert(data.message, 'error');
            }
        } catch (error) {
            this.showAlert('Failed to start job: ' + error.message, 'error');
        }
    }

    connectWebSocket(jobId) {
        const wsUrl = `${API_BASE.replace('http', 'ws')}/api/jobs/${jobId}`;
        this.wsConnection = new WebSocket(wsUrl);

        this.wsConnection.onmessage = (event) => {
            const job = JSON.parse(event.data);
            this.updateProgress(job);
        };

        this.wsConnection.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.pollJobStatus(jobId);
        };

        this.wsConnection.onclose = () => {
            console.log('WebSocket connection closed');
        };
    }

    pollJobStatus(jobId) {
        const pollInterval = setInterval(async () => {
            try {
                const response = await fetch(`${API_BASE}/api/jobs/${jobId}`);
                const result = await response.json();

                if (result.success) {
                    this.updateProgress(result.data);

                    if (['completed', 'failed', 'cancelled'].includes(result.data.status)) {
                        clearInterval(pollInterval);
                    }
                }
            } catch (error) {
                console.error('Poll error:', error);
            }
        }, 1000);
    }

    updateProgress(job) {
        document.getElementById('progressSection').classList.remove('hidden');
        document.getElementById('noProgressSection').classList.add('hidden');
        document.getElementById('jobIdDisplay').textContent = job.id;

        const progressBar = document.getElementById('progressBar');
        const progressFill = document.getElementById('progressFill');
        const progressPercent = document.getElementById('progressPercent');
        const currentStep = document.getElementById('currentStep');
        const jobStatus = document.getElementById('jobStatus');

        progressFill.style.width = `${job.progress}%`;
        progressPercent.textContent = `${job.progress}%`;
        currentStep.textContent = job.current_step || 'Initializing...';

        jobStatus.className = `status-badge status-${job.status}`;
        jobStatus.textContent = job.status.charAt(0).toUpperCase() + job.status.slice(1);

        if (job.status === 'completed' && job.result) {
            this.displayResults(job.result);
        } else if (job.status === 'failed') {
            this.showAlert(`Job failed: ${job.error}`, 'error');
        } else if (job.status === 'cancelled') {
            this.showAlert('Job was cancelled', 'warning');
        }
    }

    displayResults(results) {
        this.switchTab('results');
        const resultsContainer = document.getElementById('resultsContainer');
        resultsContainer.innerHTML = '';

        Object.entries(results).forEach(([serviceName, data]) => {
            const card = document.createElement('div');
            card.className = 'release-note';
            card.innerHTML = `
                <div class="release-note-title">
                    <span>${data.service_name} v${data.version}</span>
                    <div class="release-note-actions">
                        <button class="btn btn-secondary btn-sm" onclick="app.copyToClipboard('${serviceName}')">
                            Copy
                        </button>
                        <button class="btn btn-secondary btn-sm" onclick="app.exportMarkdown('${serviceName}')">
                            Download MD
                        </button>
                        <button class="btn btn-secondary btn-sm" onclick="app.exportHTML('${serviceName}')">
                            Export HTML
                        </button>
                    </div>
                </div>
                <div class="release-note-content" id="content-${serviceName}">${this.escapeHtml(data.content)}</div>
            `;
            resultsContainer.appendChild(card);
        });
    }

    async loadAllResults() {
        try {
            const response = await fetch(`${API_BASE}/api/jobs?limit=100`);
            const result = await response.json();

            if (result.success && result.data.length > 0) {
                const completedJobs = result.data.filter(job => job.status === 'completed' && job.result);

                if (completedJobs.length === 0) {
                    this.showAlert('No completed jobs with results found', 'warning');
                    return;
                }

                this.switchTab('results');
                const resultsContainer = document.getElementById('resultsContainer');
                resultsContainer.innerHTML = '';

                let allResults = {};
                let jobCount = 0;

                for (const job of completedJobs) {
                    const jobResult = job.result;
                    const jobIdShort = job.id.substring(0, 8);
                    const inputInfo = job.input ? `(${job.input.input_type}: ${job.input.jira_input?.substring(0, 50)}...)` : '';

                    Object.entries(jobResult).forEach(([serviceName, data]) => {
                        const uniqueServiceName = `${serviceName}_${jobIdShort}`;
                        allResults[uniqueServiceName] = {
                            ...data,
                            service_name: `${data.service_name} [Job ${jobIdShort}]`,
                            job_id: job.id
                        };
                    });

                    jobCount++;
                }

                Object.entries(allResults).forEach(([uniqueServiceName, data]) => {
                    const card = document.createElement('div');
                    card.className = 'release-note';
                    card.innerHTML = `
                        <div class="release-note-title">
                            <span>${data.service_name} v${data.version}</span>
                            <div class="release-note-actions">
                                <button class="btn btn-secondary btn-sm" onclick="app.copyToClipboard('${uniqueServiceName}')">
                                    Copy
                                </button>
                                <button class="btn btn-secondary btn-sm" onclick="app.exportMarkdown('${uniqueServiceName}')">
                                    Download MD
                                </button>
                                <button class="btn btn-secondary btn-sm" onclick="app.exportHTML('${uniqueServiceName}')">
                                    Export HTML
                                </button>
                            </div>
                        </div>
                        <div class="release-note-content" id="content-${uniqueServiceName}">${this.escapeHtml(data.content)}</div>
                    `;
                    resultsContainer.appendChild(card);
                });

                this.showAlert(`Loaded ${jobCount} completed jobs with results!`, 'success');
            } else {
                this.showAlert('No jobs found', 'warning');
            }
        } catch (error) {
            console.error('Failed to load all results:', error);
            this.showAlert('Failed to load all results', 'error');
        }
    }

    clearResults() {
        const resultsContainer = document.getElementById('resultsContainer');
        resultsContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📝</div>
                <div class="empty-state-title">No Results Yet</div>
                <div class="empty-state-text">Generate release notes to see results here</div>
            </div>
        `;
        this.showAlert('Results cleared', 'success');
    }

    async loadRecentJobs() {
        try {
            const response = await fetch(`${API_BASE}/api/jobs?limit=20`);
            const result = await response.json();

            if (result.success && result.data.length > 0) {
                const recentJobsContainer = document.getElementById('recentJobs');
                recentJobsContainer.innerHTML = '';

                result.data.forEach(job => {
                    const jobItem = document.createElement('div');
                    jobItem.className = 'card';
                    
                    let taskList = '';
                    let subtitleInfo = '';
                    
                    if (job.input) {
                        if (job.input.input_type === 'task' && job.input.jira_input) {
                            const tasks = job.input.jira_input.split(',').map(t => t.trim()).filter(t => t);
                            taskList = tasks.join(', ');
                        } else if (job.input.input_type === 'jql' && job.input.jira_input) {
                            taskList = job.input.jira_input.substring(0, 60) + '...';
                            subtitleInfo = 'JQL Query';
                        }
                    }

                    const jobIdShort = job.id.substring(0, 8);
                    const jobTitle = taskList ? `Job ${jobIdShort} - ${taskList}` : `Job ${jobIdShort}`;

                    let actions = '';
                    if (job.status === 'completed' && job.result) {
                        actions = `
                            <button type="button" class="btn btn-secondary btn-sm" onclick="event.stopPropagation(); app.loadJobDetails('${job.id}')">
                                View Results
                            </button>
                        `;
                    }

                    jobItem.innerHTML = `
                        <div class="card-header">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                                <div style="flex: 1; min-width: 0;">
                                    <div class="card-title" style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${jobTitle}">${jobTitle}</div>
                                    <div class="card-subtitle">
                                        <span class="status-badge status-${job.status}">${job.status}</span>
                                        <span style="margin-left: 10px;">${new Date(job.started_at).toLocaleString()}</span>
                                        ${subtitleInfo ? `<span style="margin-left: 10px; font-size: 11px; color: var(--gray-600);">(${subtitleInfo})</span>` : ''}
                                    </div>
                                </div>
                                ${actions ? `<div style="margin-left: 15px;">${actions}</div>` : ''}
                            </div>
                        </div>
                    `;
                    recentJobsContainer.appendChild(jobItem);
                });
            }
        } catch (error) {
            console.error('Failed to load recent jobs:', error);
        }
    }

    async loadJobDetails(jobId) {
        try {
            const response = await fetch(`${API_BASE}/api/jobs/${jobId}`);
            const result = await response.json();

            if (result.success && result.data.status === 'completed' && result.data.result) {
                this.currentJobId = jobId;
                this.displayResults(result.data.result);
            } else {
                this.showAlert('Job not completed or no results available', 'warning');
            }
        } catch (error) {
            this.showAlert('Failed to load job details', 'error');
        }
    }

    copyToClipboard(serviceName) {
        const content = document.getElementById(`content-${serviceName}`).textContent;
        navigator.clipboard.writeText(content).then(() => {
            this.showAlert('Copied to clipboard!', 'success');
        });
    }

    async exportMarkdown(serviceName) {
        const content = document.getElementById(`content-${serviceName}`).textContent;
        const blob = new Blob([content], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${serviceName}_release_notes.md`;
        a.click();
        URL.revokeObjectURL(url);
    }

    async exportHTML(serviceName) {
        try {
            if (this.currentJobId) {
                window.open(`${API_BASE}/api/export/${this.currentJobId}/html`, '_blank');
            }
        } catch (error) {
            this.showAlert('Failed to export HTML', 'error');
        }
    }

    showAlert(message, type = 'success') {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.innerHTML = `<span>${message}</span>`;

        const container = document.querySelector('.container');
        container.insertBefore(alert, container.firstChild);

        setTimeout(() => {
            alert.remove();
        }, 5000);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    insertTemplate(template) {
        const inputType = document.getElementById('inputType').value;
        
        if (inputType === 'jql') {
            const jqlQuery = document.getElementById('jqlQuery');
            jqlQuery.value = template;
        } else {
            const jqlInput = document.getElementById('jiraInput');
            jqlInput.value = template;
        }
        this.toggleInputType();
    }

    async loadRepositories() {
        try {
            const response = await fetch(`${API_BASE}/api/github/repositories`);
            const result = await response.json();

            const container = document.getElementById('repositoriesList');

            if (result.success && result.data.repositories.length > 0) {
                container.innerHTML = `
                    <div style="margin-bottom: 20px;">
                        <strong>Organization:</strong> ${result.data.organization} |
                        <strong>Total Repositories:</strong> ${result.data.count}
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px;">
                        ${result.data.repositories.map(repo => `
                            <div style="padding: 15px; background: var(--gray-50); border-radius: var(--radius); border: 1px solid var(--gray-200);">
                                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                                    <svg width="20" height="20" viewBox="0 0 16 16" fill="currentColor" style="color: var(--primary-blue);">
                                        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
                                    </svg>
                                    <a href="${repo.url}" target="_blank" style="text-decoration: none; color: var(--primary-blue); font-weight: 600; font-size: 14px;">${repo.name}</a>
                                </div>
                                ${repo.description ? `<div style="font-size: 13px; color: var(--gray-600); margin-bottom: 8px; height: 40px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">${repo.description}</div>` : ''}
                                <div style="display: flex; gap: 15px; font-size: 12px; color: var(--gray-600);">
                                    ${repo.language ? `<span>🔹 ${repo.language}</span>` : ''}
                                    <span>⭐ ${repo.stars}</span>
                                    <span>🕐 ${new Date(repo.updated_at).toLocaleDateString()}</span>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                `;
            } else {
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">📦</div>
                        <div class="empty-state-title">No repositories found</div>
                        <div class="empty-state-text">${result.message || 'Unable to load repositories'}</div>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Failed to load repositories:', error);
            const container = document.getElementById('repositoriesList');
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">❌</div>
                    <div class="empty-state-title">Failed to load repositories</div>
                    <div class="empty-state-text">${error.message}</div>
                </div>
            `;
        }
    }

    cancelJob() {
        if (this.currentJobId) {
            fetch(`${API_BASE}/api/jobs/${this.currentJobId}/cancel`, {
                method: 'POST'
            }).then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.showAlert('Job cancelled', 'warning');
                    }
                })
                .catch(error => {
                    this.showAlert('Failed to cancel job', 'error');
                });
        }
    }
}

const app = new ReleaseNotesApp();
app.init();
