import json
import networkx as nx
from django.shortcuts import render
from django.http import JsonResponse
from .models import DangerZone


def map_view(request):
    zones = DangerZone.objects.all().values('name', 'latitude', 'longitude')
    return render(request, 'petpaths/map.html', {'zones': list(zones)})


def route_api(request):
    """
    Calcula a rota euclidiana mais curta entre dois pontos evitando zonas de perigo.
    Espera JSON: { points: [ { latitude, longitude }, { latitude, longitude } ] }
    Retorna JSON: { path: [[lat, lon], ...] }
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'path': []}, status=400)

    points = data.get('points', [])
    if len(points) != 2:
        return JsonResponse({'path': []}, status=400)

    a, b = points

    # Define limites da grid em volta de A e B
    latitudes = [a['latitude'], b['latitude']]
    longitudes = [a['longitude'], b['longitude']]
    lat_min, lat_max = min(latitudes) - 0.01, max(latitudes) + 0.01
    lon_min, lon_max = min(longitudes) - 0.01, max(longitudes) + 0.01
    step = 0.005         # espaçamento da grade (~500m)
    danger_radius = 0.0025  # raio de perigo (~250m)

    # Carrega zonas de perigo
    danger_zones = list(DangerZone.objects.all())

    def in_danger(lat, lon):
        for z in danger_zones:
            if ((lat - z.latitude)**2 + (lon - z.longitude)**2)**0.5 < danger_radius:
                return True
        return False

    # Monta grafo
    G = nx.Graph()
    G.add_node(0, pos=(a['latitude'], a['longitude']))
    G.add_node(1, pos=(b['latitude'], b['longitude']))

    idx = 2
    lat = lat_min
    while lat <= lat_max:
        lon = lon_min
        while lon <= lon_max:
            if not in_danger(lat, lon):
                G.add_node(idx, pos=(lat, lon))
            idx += 1
            lon += step
        lat += step

    # Conecta nós próximos
    nodes = list(G.nodes(data='pos'))
    for i, pos_i in nodes:
        for j, pos_j in nodes:
            if i < j:
                yi, xi = pos_i
                yj, xj = pos_j
                dist = ((yi - yj)**2 + (xi - xj)**2)**0.5
                if dist <= step * 1.5:
                    G.add_edge(i, j, weight=dist)

    # Calcula menor caminho
    try:
        path_nodes = nx.shortest_path(G, source=0, target=1, weight='weight')
        coords = [list(G.nodes[n]['pos']) for n in path_nodes]
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        coords = []

    return JsonResponse({'path': coords})


def home_view(request):
    return render(request, 'petpaths/home.html')
