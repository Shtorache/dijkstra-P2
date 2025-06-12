Este projeto implementa os algoritmos Dijkstra e A* para encontrar a rota mais eficiente e segura para drones, evitando:

Áreas de risco (como obstáculos, zonas restritas ou perigosas)
Regiões com baixo sinal, que podem comprometer a comunicação com o drone

Objetivo
Fornecer uma solução de planejamento de caminho ideal para drones, considerando fatores ambientais como obstáculos e qualidade de sinal. O algoritmo determina a melhor rota possível entre dois pontos, minimizando o custo e maximizando a segurança.

Durante a execução, o sistema solicitará:

Ponto inicial (x, y)

Ponto final (x, y)


Lógica do Algoritmo
Dijkstra: calcula a rota mais curta expandindo uniformemente os caminhos.

 usa heurística (distância estimada ao destino) para otimizar o tempo de busca.

As áreas com baixo sinal ou risco têm custo mais alto, fazendo o algoritmo evitá-las quando possível.



Observações

Zonas de risco são pré-definidas no código como obstáculos ou regiões com custo aumentado.
