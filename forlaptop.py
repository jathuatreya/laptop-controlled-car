import tkinter as tk
import serial.tools.list_ports
from pynput import keyboard
import serial
import time

class RemoteControlApp:
    def __init__(self, master):
        self.master = master
        master.title("Bluetooth Remote Control")

        self.label = tk.Label(master, text="Press arrow keys to move the remote")
        self.label.pack()

        self.status = tk.Label(master, text="Bluetooth status: Disconnected")
        self.status.pack()

        self.connect_button = tk.Button(master, text="Connect", command=self.connect_bluetooth)
        self.connect_button.pack()

        self.disconnect_button = tk.Button(master, text="Disconnect", command=self.disconnect_bluetooth)
        self.disconnect_button.pack()

        self.port_variable = tk.StringVar(master)
        self.port_variable.set("")  # Initialize with an empty string

        self.port_label = tk.Label(master, text="Select COM Port:")
        self.port_label.pack()

        self.port_menu = tk.OptionMenu(master, self.port_variable, "")
        self.port_menu.pack()

        self.baudrate = 9600
        self.serial_connection = None

        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def connect_bluetooth(self):
        try:            self.port_menu['menu'].delete(0, 'end')


            available_ports = [port.device for port in serial.tools.list_ports.comports()]
            if available_ports:
                for port in available_ports:
                    self.port_menu['menu'].add_command(label=port, command=tk._setit(self.port_variable, port))
                self.status.config(text="Bluetooth status: Ports available")
            else:
                self.status.config(text="Bluetooth status: No ports available")


            self.master.wait_variable(self.port_variable)

            # Connect to the selected port
            self.serial_connection = serial.Serial(self.port_variable.get(), self.baudrate)
            time.sleep(2)  # Wait for the connection to establish
            self.status.config(text="Bluetooth status: Connected")
        except serial.SerialException as err:
            self.status.config(text=f"Bluetooth status: Connection failed - {err}")

    def disconnect_bluetooth(self):
        if self.serial_connection:
            self.serial_connection.close()
            self.serial_connection = None
            self.status.config(text="Bluetooth status: Disconnected")

    def on_press(self, key):
        try:
            if key == keyboard.Key.up:
                self.send_command('F')
            elif key == keyboard.Key.down:
                self.send_command('B')
            elif key == keyboard.Key.left:
                self.send_command('L')
            elif key == keyboard.Key.right:
                self.send_command('R')
        except AttributeError:
            pass

    def on_release(self, key):
        self.send_command('S')

    def send_command(self, command):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.write(command.encode())

root = tk.Tk()
app = RemoteControlApp(root)
root.mainloop()
