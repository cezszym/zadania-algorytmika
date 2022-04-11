
def read_from_file(filename):
  data = {}
  with open(file=filename, encoding="utf-8") as f:
    graph_info = next(f).split(' ')
    data['num_of_vertex'] = int(graph_info[0])
    data['num_of_edges'] = int(graph_info[1])
    graph = [ [] for i in range(data['num_of_vertex']) ]
    colors = [ '' for i in range(data['num_of_vertex']) ]
    for  line in f:
      edge = int(line[0])
      neighbour = int(line[2])
      graph[edge - 1].append(neighbour)
    data['graph'] = graph
    data['colors'] = colors
  return data

def search_graph(data, arr_type, remove_method):

  graph = data['graph']
  colors = data['colors']
  iterations = 1
  result_message = 'Graf jest dwudzielny'

  # Pierwszy krok
  visited_indexes = [1]
  arr = [ n for n in graph[0] ]
  colors[0] = 'czerwony'
  print("Krok: 1")
  for neighbour in arr:
    colors[neighbour - 1] = 'niebieski'
    print("ustawiam kolor wierzchołka %s na niebieski" % (neighbour))
  print("Odwiedzone: ", visited_indexes)
  print(arr_type + ": ", arr)
  print('\n')
  
  while len(arr) > 0:
    iterations += 1
    current_vertex = remove_method(arr)
    current_vertex_neighbours = graph[current_vertex - 1]
    visited_indexes.append(current_vertex)
    print("Krok: ", iterations)
    print("Odwiedzany wierchołek: ", current_vertex)
    print("sasiedzi wierzchołek: ", current_vertex_neighbours)
    for vertex in current_vertex_neighbours:
      if colors[current_vertex - 1] == colors[vertex - 1] and colors[current_vertex - 1] != '':
        result_message = "Graf nie jest dwudzielny"
        print("brak dwudzielności dla wierzchołeka %s jego kolor to %s" % (vertex, colors[vertex - 1]))
      if vertex not in visited_indexes and vertex not in arr:
        arr.append(vertex)
        if colors[current_vertex - 1] == 'niebieski':
          print('ustawiam kolor wierzchołka %s na czerwony' % (vertex))
          colors[vertex - 1] = 'czerwony'
        else:
          print('ustawiam kolor wierzchołka %s na niebieski' % (vertex))
          colors[vertex - 1] = 'niebieski'
    
    print("Odwiedzone: ", visited_indexes)
    print(arr_type + ": ", arr)
    print('-' * 100, '\n')
  for index, vertex in enumerate(colors):
    print("wierzchołek %s ma kolor %s" % (index + 1, vertex))
  print('\n', 'Wynik sprawdzania: ' + result_message)

def bfs(data):
  def pop_first(arr):
    return arr.pop(0)

  for neighbours in  data['graph']:
    neighbours.sort()

  print_header(data, 'BFS_dwudzielnosc')
  search_graph(data, "kolejka", pop_first)

def dfs(data):
  def pop_last(arr):
    return arr.pop(-1)

  for neighbours in  data['graph']:
    neighbours.sort(reverse=True)

  print_header(data, 'DFS_dwudzielnosc')
  search_graph(data, "stos", pop_last)

def print_header(data, method_name):
  print('//// %s /////'  % (method_name))
  for index, v in enumerate(data['graph']):
    print('wierzchołek: ', index+1, ' sasiedzi: ', v)
  print('\n')
  
def tryb_a(data):
  bfs(data)
  dfs(data)

data = read_from_file('data.txt')
tryb_a(data)
