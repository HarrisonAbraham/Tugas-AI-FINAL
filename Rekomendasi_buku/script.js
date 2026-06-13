document.getElementById('searchForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const userInput = document.getElementById('description').value;
    const loading = document.getElementById('loading');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContainer = document.getElementById('resultsContainer');

    // 1. Tampilkan Loading, Sembunyikan Hasil Lama
    loading.classList.remove('hidden');
    resultsSection.classList.add('hidden');
    resultsContainer.innerHTML = '';

    try {
        // 2. Kirim data ke API Backend Python (FastAPI)
        const response = await fetch('http://127.0.0.1:8000/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: userInput })
        });

        const data = await response.json();

        // 3. Matikan Loading & Tampilkan Section Hasil
        loading.classList.add('hidden');
        resultsSection.classList.remove('hidden');

        // 4. Render data asli dari Python ke dalam HTML
        data.results.forEach(book => {
            const card = `
                <div class="book-card">
                    <div class="book-icon">📖</div>
                    <div class="book-details">
                        <div class="book-header">
                            <h3 class="book-title">${book.title}</h3>
                            <span class="badge-match">${book.match} Match</span>
                        </div>
                        <p class="book-author">Oleh ${book.author}</p>
                        <p class="book-desc">${book.desc}</p>
                    </div>
                </div>
            `;
            resultsContainer.innerHTML += card;
        });

    } catch (error) {
        // Handle jika server Python mati atau ada kendala jaringan
        loading.classList.add('hidden');
        alert('Gagal terhubung ke server AI Python. Pastikan server sudah dijalankan!');
        console.error(error);
    }
});