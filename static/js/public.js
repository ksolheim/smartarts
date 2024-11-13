document.addEventListener('DOMContentLoaded', function() {
    let lastResponse = null;
    let lastWinnersList = null;
    
    updateContent();
    setInterval(updateContent, 5000);

    function updateContent() {
        // Update main content
        fetch('/api/latest_winner')
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('latest-winner-container');
                if (!container) return;
                
                const newDataStr = JSON.stringify(data);
                const lastDataStr = JSON.stringify(lastResponse);
                
                if (newDataStr !== lastDataStr) {
                    if (Object.keys(data).length === 0) {
                        container.innerHTML = `
                            <div class="d-flex flex-column align-items-center w-100">
                                <p class="text-muted fs-1 text-center"><br><br>We are waiting to start ... <br>Please enjoy your drinks and snacks!<br></p>
                                <div class="ratio ratio-16x9 mt-4 rounded overflow-hidden shadow-lg" style="width: 90%; max-width: 1200px;">
                                    <video loop autoplay muted class="VideoMain">
                                        <source src="/static/video/Champ_720P60.mp4" type="video/mp4">
                                    </video>
                                </div>
                                <p class="text-muted fs-6 text-center"><br><br><br><br><img src="/static/images/logos/github-mark.png" alt="GitHub" style="width: 30px; height: 30px;"><br><a class="text-muted" href="https://github.com/ksolheim/smartarts" target="_blank" style="color: black; text-decoration: none;">ksolheim/smartarts</a></p>
                                <p class="text-muted fs-6 text-center">Developed by Altera IT with ❤️</p>
                            </div>`;
                    } else {
                        const html = `
                            <div class="artwork-display">
                                <img src="/static/images/art/${data.art_id}.jpg" 
                                     alt="Artwork" 
                                     class="artwork-image shadow-sm mb-4">
                                <div class="card">
                                    <div class="card-body">
                                        <h5 class="card-title">Winner: ${data.winner_name}</h5>
                                        <p class="card-text">
                                            <strong>Artist:</strong> ${data.artist}<br>
                                            <strong>Title:</strong> ${data.art_title}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        `;
                        container.innerHTML = html;
                    }
                    lastResponse = data;
                }
            })
            .catch(error => console.error('Error:', error));

        // Update sidebar
        fetch('/api/recent_winners')
            .then(response => response.json())
            .then(winners => {
                const sidebar = document.querySelector('.sidebar ul');
                if (!sidebar) return;

                const newWinnersStr = JSON.stringify(winners);
                const lastWinnersStr = JSON.stringify(lastWinnersList);

                if (newWinnersStr !== lastWinnersStr) {
                    const html = winners.length === 0 
                        ? '<li class="py-2"><small class="text-muted">No winners yet...</small></li>'
                        : winners.map(winner => `
                            <li class="border-bottom py-2">
                                <div class="fw-bold">${winner.winner_name}</div>
                                <small class="text-muted">
                                    Won "${winner.art_title}" by ${winner.artist}
                                </small>
                            </li>
                        `).join('');
                    
                    sidebar.innerHTML = html;
                    lastWinnersList = winners;
                }
            })
            .catch(error => console.error('Error updating sidebar:', error));
    }
});
