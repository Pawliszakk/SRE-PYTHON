"""
Napisz funkcję, która przyjmuje listę (polecenie + argumenty) i:

łapie wyjątek, gdy polecenie nie istnieje,
sprawdza returncode, gdy polecenie istnieje, ale zwraca błąd (wypisz wtedy stderr),
wypisuje stdout, gdy wszystko się powiodło.

Przetestuj funkcję na trzech poleceniach: jednym poprawnym, jednym nieistniejącym, i jednym które istnieje ale zwróci błąd (np. sprawdzenie statusu nieistniejącej usługi systemd albo próba odczytu nieistniejącego pliku)."""
import subprocess


command1 = ["ls"]
command2 = ["testo_commando"]
command3 = ["systemctl","status","noon_service"]


def run_command(command):
    try:
        result = subprocess.run(command,capture_output=True, text=True)
        if result.returncode != 0:
            print("Command exited with following errors: ")
            print(result.stderr.strip())
            print(f'Return code: {result.returncode}')
        else:
            print(result.stdout)
    except FileNotFoundError as e:
        print("The command probably does not exist.")
        print(e)
    except Exception as e:
        print(e)

print("FIRST-----")
run_command(command1)
print("SECOND-----")
run_command(command2)
print("THIRD-----")
run_command(command3)

