import json
import networkx as nx
from django.shortcuts import render
from django.http import JsonResponse
from .models import DangerZone
from .serializers import PointSerializer, RouteSerializer

def map_view(request):
    zones = DangerZone.objects.all().values('name', 'latitude', 'longitude')
    return render(request, 'petpaths/map.html', {'zones': list(zones)})


def route_api(request):
    data = json.loads(request.body)
    points = data.get('points', [])


    G = nx.Graph()
    for i, p in enumerate(points):
        G.add_node(i, pos=(p['latitude'], p['longitude']))
    for i in G.nodes():
        for j in G.nodes():
            if i < j:
                xi, yi = G.nodes[i]['pos']
                xj, yj = G.nodes[j]['pos']
                dist = ((xi-xj)**2 + (yi-yj)**2)**0.5
                G.add_edge(i, j, weight=dist)

    try:
        path = nx.shortest_path(G, source=0, target=len(points)-1, weight='weight')
        coords = [G.nodes[n]['pos'] for n in path]
    except Exception as e:
        coords = []

    serializer = RouteSerializer({'path': coords})
    return JsonResponse(serializer.data)


def home_view(request):
    return render(request, 'petpaths/home.html')