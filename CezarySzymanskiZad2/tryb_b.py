from random import randrange
import plotly.graph_objects as go

def check_bipart(data):

  graph = data['graph']
  colors = data['colors']
  iterations = 1

  # Pierwszy krok
  visited_indexes = [1]
  queue = [ n for n in graph[0] ]
  colors[0] = 'czerwony'
  for neighbour in queue:
    colors[neighbour - 1] = 'niebieski'
 
  while len(queue) > 0:
    iterations += 1
    current_vertex = queue.pop(0)
    current_vertex_neighbours = graph[current_vertex - 1]
    visited_indexes.append(current_vertex)

    for vertex in current_vertex_neighbours:
      if colors[current_vertex - 1] == colors[vertex - 1] and colors[current_vertex - 1] != '':
        return False
      if vertex not in visited_indexes and vertex not in queue:
        queue.append(vertex)
        if colors[current_vertex - 1] == 'niebieski':
          colors[vertex - 1] = 'czerwony'
        else:
          colors[vertex - 1] = 'niebieski'
    
  return True

def check_random_graf_of_edges(num_of_vertex, additional_edges):
  data = {}
  data['num_of_vertex'] = num_of_vertex
  data['num_of_edges'] = num_of_vertex - 1
  graph = [ [] for i in range(data['num_of_vertex']) ]
  colors = [ '' for i in range(data['num_of_vertex']) ]
  data['graph'] = graph
  data['colors'] = colors
  # Stworzenie losowego minimalnego grafu spójnego
  for i in range(num_of_vertex - 1):
    random_vertex = randrange(1, num_of_vertex + 1)
    while random_vertex == i + 1:
      random_vertex = randrange(1, num_of_vertex + 1)
    graph[random_vertex - 1].append(i + 1)

  # Stworzenie dodatkowych krawedzi
  for i in range(additional_edges):
    random_vertex = randrange(1, num_of_vertex + 1)
    # Sprawdzenie czy wybrany wierzchołek nie ma już wszystkich połączeń
    while len(graph[random_vertex - 1]) == len(graph) - 1:
      random_vertex = randrange(1, num_of_vertex + 1)
    random_edge = randrange(1, num_of_vertex + 1)
    while random_edge in graph[random_vertex - 1] or random_edge == random_vertex:
      random_edge = randrange(1, num_of_vertex + 1)
    graph[random_vertex - 1].append(random_edge)
    data['num_of_edges'] +=1
  return check_bipart(data)

def check_graph_of_every_density(num_of_vertex):
  edges = []
  densities = []
  results = []

  max_edges = num_of_vertex * (num_of_vertex - 1) 
  min_edges = num_of_vertex - 1
  additional_edges = 0
  # Sprawdza dwudzielność losowo generowanego grafu o n dodatkowych krawędziach
  # Każdy graf jest generowany osobno
  while max_edges != min_edges + additional_edges:
    edges.append(additional_edges + min_edges)
    densities.append(round((additional_edges + min_edges) / max_edges * 100, 2))
    results.append(check_random_graf_of_edges(num_of_vertex, additional_edges)) 
    additional_edges += 1
  return edges, densities, results


def tryb_b():
  edges, densities, results = check_graph_of_every_density(33)
  fig = go.Figure(data=[go.Table(header=dict(values=['Liczba krawędzi', 'Gęstość [%]', 'Dwudzielność']),
                  cells=dict(
  values=[edges, densities, results]))
                      ])
  fig.write_html('tryb_b_wyniki.html', auto_open=True)

tryb_b()

# Wnioski z wyników:
# Można zauważyć, że dwudzielność spełniają głównie grafy o niskich gęstościach
# W próbie, którą ja przeprowadziłem najgętszym dwudzielnym grafem miał gęstość 11.36%
# Zdarza się, że grafy o dużych gęstościach są dwudzielne, ale z tego co zaobserwowałem jest to rzadkie
