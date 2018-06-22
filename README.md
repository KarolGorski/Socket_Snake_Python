# Socket_Snake_Python
Sockets programming classes' project.
[PL]

Sposób uruchomienia:
	Na komputerze należy mieć zainstalowanego Pythona 3.6 oraz moduł pygame. Po ściągnięciu plików należy włączyć
najpierw server.py, a następnie dowolną ilość client.py.


Dokumentacja:

Program składa się z 2 głównych programów - client i server.
Niemniej tym dwóm towarzyszą inne pliki/klasy, które zawierają content wspomagający:

-game.py - Klasa, która zarządza pojedynczym pokojem gry - oblicza ruchy, przyjmuje input od graczy, generuje kolizje, itp. Odpala się ją w wątku na serwerze.

-render.py - Klasa, która zarządza wyświetlaniem danych otrzymanych przez serwer (od game) po stronie clienta

-protocol_commands.py - Plik, w którym zadeklarowane są typy wiadomości protokołu - zarówno ich składanie - przygotowanie do przesłania, jak i rozparsowywanie

-keys.py - Plik z zadeklarowanymi stałymi stringami

-logger.py - Klasa, która przyjmuje informacje od serwera, a następnie loguje je do plików.

Typy wiadomości protokołu:

ID, 		Nazwa, 			Typy danych, 		            Składnia

0.			OK			    string 					        "0."
1.			JOIN_REQUEST	string					        "1."
2.			JOIN_REPLY		string					        "2.WAIT"/"2.PLAY"
3.			INIT_INFO		int[][], int[][],int,int,int	"3.;1,9;2,21;1,0.;1,4;1,9;2,21;1.1313.1331.134314"
4.			FRAME_INFO		int[][], int[][], int[]			"3.;1,9;2,21;1,0.;1,4;1,9;2,21;1.5,7"
5.
6.
7.
8.
9.


