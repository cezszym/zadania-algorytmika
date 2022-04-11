
from typing import Counter


def read_data (filename):
  data = {}
  with open(file=filename, encoding="utf-8") as f:
    for id, line in enumerate(f):
      # wprowadzenie danych z liń od 0-7 do słownika
      if id < 7:
        line_arr = line.strip().split(': ')
        data[line_arr[0]] = line_arr[1]

      # zapisanie instrukcji w postaci słownika stanów
      elif id == 7: 
        data['instrukcje'] = {}
      else:
        if not line.startswith(' '):
          data['instrukcje'][line.strip().strip(':')] = {}
        else:
          instruction = line.split(';')
          triggering_state = instruction[0].strip()
          states = list(data['instrukcje'].keys())
          data['instrukcje'][states[-1]][triggering_state] = instruction[1]

  return data

def move_head (head_index, action):
  if action == 'l':
    return head_index - 1
  
  if action == 'r':
    return head_index + 1

  if action == 's':
    return head_index
  
  else:
    raise ValueError('Zły znak przejścia: ' + action + ' - dozwolone tylko: l, r, s')
  

def run_program (filename):
  
  # wczytanie danych
  data = read_data(filename)
  # dodanie dotatkowych pól pustych na końcach słowa
  data['słowo'] = '__' + data['słowo'] + '__'
  # stworzenie taśmy w postaci listy i sprawdzenie czy nie występują znaki z poza alfabetu
  tape = [ char for char in  data['słowo'] ]
  if not all([ char in data['alfabet'] for char in tape]):
    raise ValueError("Słowo początkowe zawiera znaki z poza alfabetu")
  # ustawienie głowicy na pierwszym niepustym znaku
  head_index = [ index for  index, char in enumerate(tape) if char != '_'][0]
  state = data['stan początkowy']
  # stworzenie listy stanów końcowych - w razie jakby było ich więcej niż 1
  final_states = data['stan końcowy'].split(',')
  # licznik iteracji aby wykryć zapętlenie oraz historia stanów żeby w przypadku zapętlenia znaleźć stan, który zawiesił program
  iterations = 0
  states_history = ''

  print('Wykonuje program: ' + data['Opis'])

  # pętla wykonywania programu - kończy się gdy stan będzie równy stanowi końcowemu lub zostanie osiągnięty limit iteracji
  while True:

    # dodanie pustego znaku, gdy głowica dojdzie do któregoś z końców taśmy - w ten sposób zapewniony jest warunek nieskończoności taśmy
    if head_index == 0:
      tape = ['_'] + tape
      head_index = 1
    if head_index == len(tape):
      tape.append('_')

    print('\n','Stan: ' + state)
    print(' ' * head_index + '|')
    print(' ' * head_index + 'V')
    print(''.join(tape), '\n')

  # warunek stopu i przerwanie z powodu nieskończonej pętli
    if state in final_states :
      print('Koniec programu w stanie ' + state)
      break
    if iterations > 1000:
      c = Counter(states_history)
      print('Błąd - Program przekroczył limit iteracji')
      print('Najprawdopodobniej błędna instrukcja w stanie: ' + c.most_common(1)[0][0])
      break

    # przypisanie obecnej wartości obserwowanej oraz instrukcji zgodnie ze stanem i obserowaną wartością
    observed_value = tape[head_index]
    current_instruction = data['instrukcje'][state][observed_value].split(',')
    # zmiana stanu, obserwowanej wartości oraz przesunięcie głowicy
    state = current_instruction[0]
    tape[head_index] = current_instruction[1]
    head_index = move_head(head_index, current_instruction[2])
    iterations += 1
    states_history += state

  f = open(data['Opis'].strip("\"") + "-wynik.txt", "w", encoding="utf-8")
  f.write(''' 
  Początkowe słowo: %s
  Nazwa instrukcji: %s
  Wynik końcowy: %s
  Stan końcowy: %s
  ''' 
  % (data['słowo'], data['Opis'], ''.join(tape), state))

run_program('test-data1.txt')
run_program('test-data2.txt')
run_program('test-data3.txt')