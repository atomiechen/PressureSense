import argparse

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


class BLEController:

	PREFIX = "Presenab"
	TOTAL = 2

	def __init__(self, port, baudrate, timeout=None):
		self.isOpen = False
		self.my_serial = Serial(port, baudrate, timeout=timeout)
		self.isOpen = True
		print(self.my_serial)

		self.cur_idx = 0

	def __del__(self):
		self.close()

	def close(self):
		if self.isOpen:
			self.my_serial.close()
			print("Serial port closed.")

	def refresh(self):
		self.my_serial.write(("RR").encode())

		data_bytes = bytearray()
		while True:
			recv = self.my_serial.read()
			data_bytes += recv
			data_len = len(data_bytes)
			k = 0
			while k + 14 <= data_len:
				# 收到主机目前正在搜索的蓝牙名称
				if data_bytes[k] == 0XEE and data_bytes[k + 1] == 0X88 and data_bytes[k + 12] == 0XEE and data_bytes[k + 13] == 0X77:
					name_buffer = ""
					for k5 in range(10):
						if data_bytes[k + 2 + k5] != 0xEE:
							name_buffer = name_buffer + chr(data_bytes[k + 2 + k5])
					print(f"Target: {name_buffer}")
					k = k + 14
					return
				else:
					k = k + 1

	def update(self, data_send_update):
		print("data_send_update值为：" + data_send_update)
		self.my_serial.write((data_send_update + "UU").encode())

	def udpate_idx(self):
		self.cur_idx += 1
		if self.cur_idx == self.TOTAL:
			self.cur_idx = 0

	def interactive_cli(self):
		while True:
			cmd = input(">> ")
			paras = cmd.strip().split()
			cmd_type = int(paras[0])
			if cmd_type == 1:
				## refresh
				self.refresh()
			elif cmd_type == 2:
				## update
				try:
					data_send_update = paras[1]
				except:
					data_send_update = self.PREFIX + str(self.cur_idx)
					self.udpate_idx()
				self.update(data_send_update)
			elif cmd_type == 0:
				## quit
				print("quit BLE controller.")
				return


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
