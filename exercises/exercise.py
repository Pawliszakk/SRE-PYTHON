"""
Stwórz plik servers.txt (ręcznie, w edytorze) z 5 liniami — każda linia to nazwa serwera i jego status oddzielone spacją, np. jedna nazwa i jeden status na linię.
W skrypcie Pythona otwórz ten plik do odczytu i wczytaj wszystkie linie.
Dla każdej linii: rozbij ją na dwie części (nazwa i status).
Wypisz wynik w formacie własnego wyboru, np. Serwer X ma status Y.
Policz ile linii ma status "Running", a ile "Stopped".
"""
with open('servers.txt', 'r') as f:
    running_counter = 0
    stopped_counter = 0
    
    for line in f:
      servers, status = line.strip().split()
      print(f'Server {servers} has status {status}')
      
      if status.lower() == "running":
         running_counter += 1
      elif status.lower() == "stopped":
         stopped_counter += 1
      
    print(f'Running Servers: {running_counter}')
    print(f'Stopped Servers: {stopped_counter}')
        
