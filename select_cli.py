import argparse
from enum import IntEnum

from serial import Serial
from serial.tools.list_ports import comports


TIMEOUT = 1
BAUDRATE = 1000000
devices_found = comports()
PORT = None
try:
	## default use the last port on the list
	PORT = devices_found[-1].device
except:
	pass


def enumerate_ports():
	# 查看可用端口
	print("All serial ports:")
	for item in devices_found:
		print(item)

def serial_xx(gui, mSerial):
	global data_bytes
	print(f"mSerial: {mSerial}")
	while True:
		count = mSerial.inWaiting()
		if count:
			rec_str = mSerial.read(count)
			data_bytes = data_bytes + rec_str
			data_len = len(data_bytes)
			k = 0
			while k + 14 <= data_len:
				# 收到主机目前正在搜索的蓝牙名称
				if data_bytes[k] == 0XEE and data_bytes[k + 1] == 0X88 and data_bytes[k + 12] == 0XEE and data_bytes[k + 13] == 0X77:
					name_buffer = ""
					for k5 in range(10):
						if data_bytes[k + 2 + k5] != 0xEE:
							name_buffer = name_buffer + chr(data_bytes[k + 2 + k5])
					gui.acupoint_name_select.setText("搜索目标：" + name_buffer)
					k = k + 14
				else:
					k = k + 1
			data_bytes[0:k] = b''


class BLE_CMD(IntEnum):
	RECONNECT = 0
	NAME = 1
	CONNECT = 2
	NAMEFILTER = 3
	PROTOCOL = 4


class BLE_PROTOCOL(IntEnum):
	SIMPLE = 0
	SECURE = 1


class BLEController:

	PREFIX = "Presenab"
	TOTAL = 2

	## protocol
	HEAD = 0xEB
	TAIL = 0xED
	ESCAPE = 0xEC
	ESCAPE_ESCAPE = 0x00
	ESCAPE_HEAD = 0x01
	ESCAPE_TAIL = 0x02

	def __init__(self, port, baudrate, timeout=None):
		self.isOpen = False
		self.my_serial = Serial(port, baudrate, timeout=timeout)
		self.isOpen = True
		print(self.my_serial)

		self.cur_idx = 0
		# self.protocol = 1  ## 0 for simple, 1 for secure
		self.protocol = BLE_PROTOCOL.SECURE
		self.namefilter = 0

	def __del__(self):
		self.close()

	def close(self):
		if self.isOpen:
			self.my_serial.close()
			print("Serial port closed.")

	def udpate_idx(self):
		self.cur_idx += 1
		if self.cur_idx == self.TOTAL:
			self.cur_idx = 0

	def send_frame(self, content):
		frame = bytearray()
		frame.append(self.HEAD)
		try:
			## 是一个字节/数字的数组
			for ch in content:
				if ch == self.HEAD:
					frame.append(self.ESCAPE)
					frame.append(self.ESCAPE_HEAD)
				elif ch == self.TAIL:
					frame.append(self.ESCAPE)
					frame.append(self.ESCAPE_TAIL)
				elif ch == self.ESCAPE:
					frame.append(self.ESCAPE)
					frame.append(self.ESCAPE_ESCAPE)
				else:
					frame.append(ch)
		except:
			## 是一个数字
			frame.append(content)
		frame.append(self.TAIL)
		self.my_serial.write(frame)

	def read_byte(self):
		recv = self.my_serial.read()
		if len(recv) != 1:
			raise Exception("Serial timeout!!!")
		return recv[0]

	def recv_frame(self):
		frame = bytearray()
		begin = False
		while True:
			recv = self.read_byte()
			if begin:
				if recv == self.ESCAPE:
					## escape bytes
					recv = self.read_byte()
					if recv == self.ESCAPE_ESCAPE:
						frame.append(self.ESCAPE)
					elif recv == self.ESCAPE_HEAD:
						frame.append(self.HEAD)
					elif recv == self.ESCAPE_TAIL:
						frame.append(self.TAIL)
					else:
						print(f"Wrong ESCAPE byte: {recv}")
				elif recv == self.TAIL:
					## end a frame
					break
				else:
					frame.append(recv)
			elif recv == self.HEAD:
				## begin a frame
				begin = True

		return frame

	def interactive_cli(self):
		while True:
			cmd = input(">> ").strip()
			## exit the command line interface
			if cmd and "quit".startswith(cmd) or cmd == "exit":
				break

			try:
				paras = cmd.split()
				try:
					cmd_type = BLE_CMD(int(paras[0]))
				except Exception:
					cmd_type = BLE_CMD[paras[0].upper()]

				if cmd_type == BLE_CMD.RECONNECT:
					## reconnect
					self.send_frame(BLE_CMD.RECONNECT)
					print("Reconnect")
				elif cmd_type == BLE_CMD.NAME:
					## get name
					self.send_frame(BLE_CMD.NAME)
					try:
						data = self.recv_frame()
						name = data.decode()
						print(f"Current target: {name}")
					except KeyboardInterrupt:
						pass
				elif cmd_type == BLE_CMD.CONNECT:
					## connect using specified name
					try:
						name = paras[1]
					except Exception:
						name = self.PREFIX + str(self.cur_idx)
						self.udpate_idx()
					self.send_frame(bytes([BLE_CMD.CONNECT])+name.encode())
					print(f"Connecting to: {name}")
				elif cmd_type == BLE_CMD.NAMEFILTER:
					## enable/disable name filter
					try:
						if paras[1] == 'enable':
							self.namefilter = 1
						elif paras[1] == 'disable':
							self.namefilter = 0
					except Exception:
						self.namefilter = 1 - self.namefilter
					self.send_frame([BLE_CMD.NAMEFILTER, self.namefilter])
					print(f"{'Enable' if self.namefilter==1 else 'Disable'} name filter")
				elif cmd_type == BLE_CMD.PROTOCOL:
					## switch protocol
					try:
						self.protocol = BLE_PROTOCOL[paras[1].upper()]
					except Exception:
						self.protocol = BLE_PROTOCOL(1 - self.protocol)
					self.send_frame([BLE_CMD.PROTOCOL, self.protocol.value])
					print(f"Switch protocol to {self.protocol.name}")

			except Exception as e:
				# print(f"get exception: {e}")
				pass


def main(args):
	if args.enumerate:
		enumerate_ports()
		return

	my_controller = BLEController(args.port, args.baudrate, TIMEOUT)
	my_controller.interactive_cli()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-e', dest='enumerate', action=('store_true'), default=False, help="enumerate all serial ports")
	parser.add_argument('-p', dest='port', action=('store'), default=PORT, help="specify serial port")
	parser.add_argument('-b', dest='baudrate', action=('store'), default=BAUDRATE, type=int, help="specify baudrate")
	args = parser.parse_args()

	main(args)
