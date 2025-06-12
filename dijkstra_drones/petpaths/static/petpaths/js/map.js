const map = L.map('map').setView([-22.9456, -42.1805], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Adiciona zonas de perigo
dangerZones.forEach(z => {
    L.circle([z.latitude, z.longitude], {
        radius: 200,
        color: 'red',
        fillOpacity: 0.4
    }).addTo(map).bindPopup(z.name);
});

let points = [];
const markers = [];

map.on('click', function(e) {
    const { lat, lng } = e.latlng;
    const point = { latitude: lat, longitude: lng };
    points.push(point);

    const marker = L.marker([lat, lng]).addTo(map);
    markers.push(marker);

    // Atualiza coordenadas na tela
    const coordDisplay = document.getElementById('clicked-coords');
    if (coordDisplay) {
        coordDisplay.innerText = `Último ponto clicado: Latitude ${lat.toFixed(5)}, Longitude ${lng.toFixed(5)}`;
    } else {
        console.warn('Elemento #clicked-coords não encontrado!');
    }

    // Remover marcador ao clicar nele
    marker.on('click', function() {
        map.removeLayer(marker);

        const markerIndex = markers.indexOf(marker);
        if (markerIndex !== -1) {
            markers.splice(markerIndex, 1);
            points.splice(markerIndex, 1);
        }
    });
});

document.getElementById('calc-route').onclick = async () => {
    const resp = await fetch('/api/route/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ points })
    });

    const data = await resp.json();
    const latlngs = data.path.map(p => [p[0], p[1]]);
    L.polyline(latlngs, { color: 'blue' }).addTo(map);
};