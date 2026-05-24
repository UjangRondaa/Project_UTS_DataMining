/* =====================================================
   ObesityScan — Frontend Logic
   Handle form submission via fetch dan render hasil prediksi
   ===================================================== */

document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('prediction-form');
    const submitBtn = document.getElementById('submit-btn');
    const resultSection = document.getElementById('result-section');
    const errorSection = document.getElementById('error-section');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        // UI feedback saat loading
        submitBtn.disabled = true;
        submitBtn.querySelector('.btn-text').textContent = 'Menganalisis...';
        errorSection.style.display = 'none';

        // Kumpulkan data form
        const formData = new FormData(form);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Terjadi kesalahan pada server');
            }

            renderHasil(data);
            resultSection.style.display = 'block';
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

        } catch (err) {
            document.getElementById('error-message').textContent = err.message;
            errorSection.style.display = 'flex';
            resultSection.style.display = 'none';
            errorSection.scrollIntoView({ behavior: 'smooth' });
        } finally {
            submitBtn.disabled = false;
            submitBtn.querySelector('.btn-text').textContent = 'Analisis sekarang';
        }
    });

    form.addEventListener('reset', function () {
        resultSection.style.display = 'none';
        errorSection.style.display = 'none';
    });


    function renderHasil(data) {

        // === Prediction Badge ===
        const badge = document.getElementById('prediction-badge');
        const prediksiValue = document.getElementById('prediction-value');
        const prediksiConfidence = document.getElementById('prediction-confidence');

        prediksiValue.textContent = data.prediksi;

        // Reset class lalu tambah class sesuai prediksi
        badge.className = 'prediction-badge';
        badge.classList.add(data.prediksi.toLowerCase());

        const confidenceValue = data.probabilitas[data.prediksi];
        prediksiConfidence.textContent = `Tingkat keyakinan model ${confidenceValue} persen`;

        // === BMI ===
        document.getElementById('bmi-value').textContent = data.bmi;
        document.getElementById('bmi-category').textContent = `Kategori BMI ${data.kategori_bmi}`;

        // === Probability Bars ===
        const probContainer = document.getElementById('probability-bars');
        probContainer.innerHTML = '';

        const urutan = ['Kurus', 'Normal', 'Obesitas'];
        urutan.forEach(function (kelas) {
            const prob = data.probabilitas[kelas] || 0;
            const cls = kelas.toLowerCase();

            const bar = document.createElement('div');
            bar.className = 'prob-bar';
            bar.innerHTML = `
                <span class="prob-label">${kelas}</span>
                <div class="prob-track">
                    <div class="prob-fill ${cls}" style="width: 0%"></div>
                </div>
                <span class="prob-value">${prob.toFixed(1)} %</span>
            `;
            probContainer.appendChild(bar);

            // Animasi width
            requestAnimationFrame(() => {
                setTimeout(() => {
                    bar.querySelector('.prob-fill').style.width = prob + '%';
                }, 100);
            });
        });

        // === Rekomendasi ===
        const rek = data.rekomendasi;
        document.getElementById('berat-ideal').textContent =
            `${rek.berat_ideal_min} sampai ${rek.berat_ideal_max} kg`;

        const targetEmphasis = document.getElementById('target-emphasis');
        const arahLabel = document.getElementById('arah-label');
        const targetSelisih = document.getElementById('target-selisih');

        // Reset class
        targetEmphasis.className = 'target-block emphasis';

        if (rek.arah === 'naikkan') {
            arahLabel.textContent = 'Naikkan berat badan';
            targetSelisih.textContent = `${rek.selisih} kg`;
            targetEmphasis.classList.add('naik');
        } else if (rek.arah === 'turunkan') {
            arahLabel.textContent = 'Turunkan berat badan';
            targetSelisih.textContent = `${rek.selisih} kg`;
            targetEmphasis.classList.add('turun');
        } else {
            arahLabel.textContent = 'Pertahankan berat badan';
            targetSelisih.textContent = 'Sudah ideal';
            targetEmphasis.classList.add('stabil');
        }

        // === Lifestyle list ===
        const ul = document.getElementById('lifestyle-list');
        ul.innerHTML = '';
        rek.lifestyle.forEach(function (tip) {
            const li = document.createElement('li');
            li.textContent = tip;
            ul.appendChild(li);
        });
    }
});
