const map = L.map('map').setView([-22.9456, -42.1805], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

dangerZones.forEach(z => {
    L.circle([z.latitude, z.longitude], { radius: 200 })
        .addTo(map)
        .bindPopup(z.name);
});

let points = [];
const markers = [];
map.on('click', function(e) {
    const { lat, lng } = e.latlng;
    points.push({ latitude: lat, longitude: lng });
    const m = L.marker([lat, lng]).addTo(map);
    markers.push(m);
});

document.getElementById('calc-route').onclick = async () => {
    const resp = await fetch('/api/route/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ points })
    });
    const data = await resp.json();
    const latlngs = data.path.map(p => [p[0], p[1]]);
    L.polyline(latlngs).addTo(map);
};