import re, sys
import struct
from base64 import b64encode
from hashlib import sha1

if sys.version_info[0] < 3 :
	from SocketServer import ThreadingMixIn, TCPServer, StreamRequestHandler
else:
	from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler




'''
+-+-+-+-+-------+-+-------------+-------------------------------+
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
|N|V|V|V|       |S|             |   (if payload len==126/127)   |
| |1|2|3|       |K|             |                               |
+-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
|     Extended payload length continued, if payload len == 127  |
+ - - - - - - - - - - - - - - - +-------------------------------+
|                     Payload Data continued ...                |
+---------------------------------------------------------------+
'''

FIN    = 0x80
OPCODE = 0x0f
MASKED = 0x80
PAYLOAD_LEN = 0x7f
PAYLOAD_LEN_EXT16 = 0x7e
PAYLOAD_LEN_EXT64 = 0x7f

OPCODE_TEXT = 0x01
CLOSE_CONN  = 0x8



# -------------------------------- API ---------------------------------

class API():
	def run_forever(self):
		try:
			print("Listening on port %d for clients.." % self.port)
			self.serve_forever()
		except KeyboardInterrupt:
			self.server_close()
			print("Server terminated.")
		except Exception as e:
			print("ERROR: WebSocketsServer: "+str(e))
			exit(1)
	def new_client(self, client, server):
		pass
	def client_left(self, client, server):
		pass
	def message_received(self, client, server, message):
		pass
	def set_fn_new_client(self, fn):
		self.new_client=fn
	def set_fn_client_left(self, fn):
		self.client_left=fn
	def set_fn_message_received(self, fn):
		self.message_received=fn
	def send_message(self, client, msg):
		self._unicast_(client, msg)
	def send_message_to_all(self, msg):
		self._multicast_(msg)



# ------------------------- Implementation -----------------------------

class WebsocketServer(ThreadingMixIn, TCPServer, API):

	allow_reuse_address = True
	daemon_threads = True # comment to keep threads alive until finished

	'''
	clients is a list of dict:
	    {
	     'id'      : id,
	     'handler' : handler,
	     'address' : (addr, port)
	    }
	'''
	clients=[]
	id_counter=0

	def __init__(self, port, host='127.0.0.1'):
		self.port=port
		TCPServer.__init__(self, (host, port), WebSocketHandler)

	def _message_received_(self, handler, msg):
		self.message_received(self.handler_to_client(handler), self, msg)

	def _new_client_(self, handler):
		self.id_counter += 1
		client={
			'id'      : self.id_counter,
			'handler' : handler,
			'address' : handler.client_address
		}
		self.clients.append(client)
		self.new_client(client, self)

	def _client_left_(self, handler):
		client=self.handler_to_client(handler)
		self.client_left(client, self)
		if client in self.clients:
			self.clients.remove(client)
	
	def _unicast_(self, to_client, msg):
		to_client["handler"].send_message(msg)

	def _multicast_(self, msg):
		for client in self.clients:
			self._unicast_(client, msg)
	def handler_to_client(self, handler):
		for client in self.clients:
			if client['handler'] == handler:
				return client



class WebSocketHandler(StreamRequestHandler):

	def __init__(self, socket, addr, server):
		self.server=server
		StreamRequestHandler.__init__(self, socket, addr, server)

	def setup(self):
		StreamRequestHandler.setup(self)
		self.keep_alive = True
		self.handshake_done = False
		self.valid_client = False

	def handle(self):
		while self.keep_alive:
			if not self.handshake_done:
				self.handshake()
			elif self.valid_client:
				self.read_next_message()

	def read_bytes(self, num):
		# python3 gives ordinal of byte directly
		bytes = self.rfile.read(num)
		if sys.version_info[0] < 3:
			return map(ord, bytes)
		else:
			return bytes

	def read_next_message(self):

		b1, b2 = self.read_bytes(2)

		fin    = b1 & FIN
		opcode = b1 & OPCODE
		masked = b2 & MASKED
		payload_length = b2 & PAYLOAD_LEN

		if not b1:
			print("Client closed connection.")
			self.keep_alive = 0
			return
		if opcode == CLOSE_CONN:
			print("Client asked to close connection.")
			self.keep_alive = 0
			return
		if not masked:
			print("Client must always be masked.")
			self.keep_alive = 0
			return

		if payload_length == 126:
			payload_length = struct.unpack(">H", self.rfile.read(2))[0]
		elif payload_length == 127:
			payload_length = struct.unpack(">Q", self.rfile.read(8))[0]

		masks = self.read_bytes(4)
		decoded = ""
		for char in self.read_bytes(payload_length):
			char ^= masks[len(decoded) % 4]
			decoded += chr(char)
		self.server._message_received_(self, decoded)

	def send_message(self, message):
		self.send_text(message)

	def send_text(self, message):
		'''
		NOTES
		Fragmented(=continuation) messages are not being used since their usage
		is needed in very limited cases - when we don't know the payload length.
		'''
	
		# Validate message
		try:
		
			if isinstance(message, bytes):
				message = try_decode_UTF8(message) # this is slower but assures we have UTF-8
				if not message:
					print("Can\'t send message, message is not valid UTF-8")
					return False
			elif isinstance(message, str) or isinstance(message, unicode):
				pass
			else:
				print('Can\'t send message, message has to be a string or bytes. Given type is %s' % type(message))
				return False
		except NameError:
			pass
		header  = bytearray()
		payload = encode_to_UTF8(message)
		payload_length = len(payload)

		# Normal payload
		if payload_length <= 125:
			header.append(FIN | OPCODE_TEXT)
			header.append(payload_length)

		# Extended payload
		elif payload_length >= 126 and payload_length <= 65535:
			header.append(FIN | OPCODE_TEXT)
			header.append(PAYLOAD_LEN_EXT16)
			header.extend(struct.pack(">H", payload_length))

		# Huge extended payload
		elif payload_length < 18446744073709551616:
			header.append(FIN | OPCODE_TEXT)
			header.append(PAYLOAD_LEN_EXT64)
			header.extend(struct.pack(">Q", payload_length))
			
		else:
			raise Exception("Message is too big. Consider breaking it into chunks.")
			return

		self.request.send(header + payload)

	def handshake(self):
		message = self.request.recv(1024).decode().strip()
		upgrade = re.search('\nupgrade[\s]*:[\s]*websocket', message.lower())
		if not upgrade:
			self.keep_alive = False
			return
		key = re.search('\n[sS]ec-[wW]eb[sS]ocket-[kK]ey[\s]*:[\s]*(.*)\r\n', message)
		if key:
			key = key.group(1)
		else:
			print("Client tried to connect but was missing a key")
			self.keep_alive = False
			return
		response = self.make_handshake_response(key)
		self.handshake_done = self.request.send(response.encode())
		self.valid_client = True
		self.server._new_client_(self)
		
	def make_handshake_response(self, key):
		return \
		  'HTTP/1.1 101 Switching Protocols\r\n'\
		  'Upgrade: websocket\r\n'              \
		  'Connection: Upgrade\r\n'             \
		  'Sec-WebSocket-Accept: %s\r\n'        \
		  '\r\n' % self.calculate_response_key(key)
		
	def calculate_response_key(self, key):
		GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
		hash = sha1(key.encode() + GUID.encode())
		response_key = b64encode(hash.digest()).strip()
		return response_key.decode('ASCII')

	def finish(self):
		self.server._client_left_(self)



def encode_to_UTF8(data):
	try:
		return data.encode('UTF-8')
	except UnicodeEncodeError as e:
		print("Could not encode data to UTF-8 -- %s" % e)
		return False
	except Exception as e:
		raise(e)
		return False
	except AttributeError:
		return False



def try_decode_UTF8(data):
	try:
		return data.decode('utf-8')
	except UnicodeDecodeError:
		return False
	except Exception as e:
		raise(e)
		


# This is only for testing purposes
class DummyWebsocketHandler(WebSocketHandler):
    def __init__(self, *_):
        pass

#######################################################################
from random import randint
import json
players = {}
online = []
games = {}
countgames = 0
class player(object):
	connected = False 
	idclient = None #integeer
	onlinem = None #integer
	game = None #integer
class game(object):
	id1cord = 0 #integer
	id1 = None
	id2cord = 0 #integer
	id2 = None
	Finish = False
	statusid1 = False
	statusid2 = False
	napr1 = None
	napr2 = None
		
# Called for every client connecting (after handshake)
def new_client(client, server):
	global games
	global countgames
	global id_counter
	global players
	print("New client connected and was given id %d" % client['id'])
	print(server.clients)
	players[client['id']] = player()                   #записываем id одключившегося игрока в class player();
	players[client['id']].idclient = client['id']      #олучаем id клиента
	players[client['id']].connected = True
	online.insert(len(online), client['id'])
	players[client['id']].onlinem = len(online)
	print(online)
	if len(online) >= 2:                                #если в игре уже 2 игрока 
		id1 = online.pop(0)                             #даляет в списке онлайн
		id2 = online.pop(0)
		countgames = countgames + 1
		players[id1].game = countgames                  #количество игр
		players[id2].game = countgames
		games[int(countgames)] = game()                 #номер игры записываем в класс игры
		games[int(countgames)].id1 = id1
		games[int(countgames)].id2 = id2
		games[int(countgames)].id1cord = 0
		games[int(countgames)].id2cord = 0
		print(games[countgames].id1)
		print(games[countgames].id2)
		print(games)
		players[id1].onlinem = None
		players[id2].onlinem = None
		# server._multicast_(countgames)
		print(server.clients)
		i = 0
		while i != len(server.clients):                                  #ищет в списке серверклиентов определенного клиента
			if server.clients[i]['id'] == games[countgames].id1:
				server._unicast_(server.clients[i], str(countgames))
			i = i + 1
		i = 0
		while i != len(server.clients):
			if server.clients[i]['id'] == games[countgames].id2:
				server._unicast_(server.clients[i], str(countgames))
			i = i + 1


# Called for every client disconnecting
def client_left(client, server):
	global online
	global id_counter
	# print("Client(%d) disconnected" % client['id'])
	# players[client['id']].connected = False
	# print(players[client['id']].onlinem)
	# if players[client['id']].onlinem == None:
	# 	pass
	# else:
	# 	online.pop(players[client['id']].onlinem - 1)
	# print(online)


# Called when a client sends a message
def message_received(client, server, messag): 
	global players
	global games
	message = str(messag)
	if len(message) > 200:                     #проверка буфера
		message = message[:200]+'..'
	# print(message)
	# print(server.clients) 
	# print(int(message[0]))
	# # print(games[int(message[0])].id1)
	# print(games[1].id1cord)
	# print(games[1].id2cord)
	# print(games[1].id1)
	# print(games[int(message[0])].id1)
	# print(client['id'])
	# print(games[int(message[0])].id1 == client['id'])
	# print(games[1].id2)
	# print(games[1].Finish)
	# print(str("ВАЖНО:  ") + str(games[1].id2cord))
	# message = array(massege)
	print(message)
	print(json.loads(message))
	message = json.loads(message)
	gamecol = message["game"]
	# print(json.loads(message))
	# print(json.loads(message)["status"])
	try:
		i = 0
		while i != len(server.clients):
			if server.clients[i]['id'] == client['id'] and int(games[int(gamecol)].id1) == int(client['id']):
				id1c = i
			i = i + 1
		i = 0
		while i != len(server.clients):
			if server.clients[i]['id'] == client['id'] and int(games[int(gamecol)].id2) == int(client['id']):
				id2c = i
			i = i + 1


	 		#тправка информации
		if int(games[int(gamecol)].id1) == int(client['id']):
			games[int(gamecol)].id1cord = message["cord"]
			games[int(gamecol)].napr1= message["napr"]
			if message['status'] == 'true':
				games[int(gamecol)].id1cord = True
			send = dict(cord = str(games[int(gamecol)].id2cord), status = str(games[int(gamecol)].statusid1), napr = games[int(gamecol)].napr2)
			server._unicast_(server.clients[id1c], json.dumps(send))
		if int(games[int(gamecol)].id2) == int(client['id']):
			games[int(gamecol)].id2cord = message["cord"]
			games[int(gamecol)].napr2= message["napr"]
			if message['status'] == 'true':
				games[int(gamecol)].id2cord = True
			send = dict(cord = str(games[int(gamecol)].id1cord), status = str(games[int(gamecol)].statusid2), napr = games[int(gamecol)].napr1)
			server._unicast_(server.clients[id2c], json.dumps(send))

	except KeyError:
		pass
	except IndexError:
		pass
	except IndexError:
		pass


	# if games[int(message[0])].id1 == client['id']:
	# 	try:
	# 		games[int(message[0])].id1cord = int(message[1:])
	# 		server._unicast_(server.clients[client['id']], str(games[int(message[0])].id2))
	# 	except IndexError:
	# 		pass
	# 	except KeyError:
	# 		pass
		
	# if games[int(message[0])].id2 == client['id']:
	# 	try:
	# 		games[int(message[0])].id2cord = int(message[1:])
	# 		server._unicast_(server.clients[client['id']], str(games[int(message[0])].id1))
	# 	except IndexError:
	# 		pass
	# 	except KeyError:
	# 		pass
		
	
	#server._multicast_(str(cordid[1]))
	#server._multicast_(str(cordid[2]))
	#server.send_message_to_all(str(cordid[client["id"]]))
	print("Client(%d) said: %s" % (client['id'], message))

id_counter = 0


PORT=9001
server = WebsocketServer(PORT, host='0.0.0.0')
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()