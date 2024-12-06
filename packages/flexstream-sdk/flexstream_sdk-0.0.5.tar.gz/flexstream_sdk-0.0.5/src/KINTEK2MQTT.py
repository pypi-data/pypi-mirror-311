import sys

import paho.mqtt.client as pahoc
import time


from src.flexstream_app import FlexStreamApp


class KINTEK2MQTT(pahoc.Client):
    def __init__(self, PrintDebug=False, kintek_ip='192.168.1.103',
                 mqtt_name=None ,broker_address = "localhost",port = 1883,client_id="", userdata=None, protocol=pahoc.MQTTv5):
        super().__init__(client_id, userdata, protocol)
        # MQTT Broker Settings
        self.broker_address = broker_address
        self.port = port  # Default MQTT port
        self.flexstream_app = FlexStreamApp(kintek_ip)
        # Set the callback functions
        self.on_connect = self.on_connect_callback
        self.on_message = self.on_message_callback
        self.messages = None
        self.last_update_time = None
        self.connected = False

        # Connect to the broker
        if self.connect(broker_address, port, 60) != 0:
            print("Couldn't connect to the mqtt broker")
            sys.exit(1)

        self.command_to_execute = []
        self.PrintDebug = PrintDebug
        if (mqtt_name!=None):
            self.Channel_Name = "KINTEK2MQTT/"+mqtt_name
        self.start_time = time.time()

    def on_connect_callback(self, client, userdata, flags, rc,properties):
        print(f"Connected to kintek2mqtt with result code {rc}")

    def on_message_callback(self, client, userdata, msg):
        command = msg.payload.decode()
        print("Received message: {}".format(command))
        command = eval(command)
        self.messages.append(command)


    def execute_command_from_que (self):
        if len(self.messages)>0:
            command = self.messages.pop(0)[0]
            name = command[0]
            cmd_type = command[1]
            mode = command[2]
            value = command[3]
            if name == 'KINTEK':
                if cmd_type == 'Set':
                    if mode == 'Zero':
                        self.flexstream_app.set_zero_mode(value)
                    elif mode == 'Standby':
                        self.flexstream_app.set_standby_mode()
                if cmd_type == 'Read':
                    self.flexstream_app.get_message()


    def Start(self):
            self.messages = []
            self.subscribe(self.Channel_Name + '/Cmd', qos=2)
            print("Subscribed to : " + self.Channel_Name + '/Cmd')
            self.last_update_time = time.time()-1
            self.loop_start()
            self.connected = True


    def Stop(self):
        if self.connected:
            self.flexstream_app.disconnect()
            self.connected = False
            self.loop_stop()
            self.disconnect()

    def Update(self):
        if self.connected:
            self.execute_command_from_que()
            if time.time()-self.last_update_time > 1:
                self.last_update_time = time.time()
                textprint = self.flexstream_app.get_message()
                if self.PrintDebug:
                    print (textprint)
                self.publish(self.Channel_Name + "/Data", textprint, qos=2)
                self.subscribe(self.Channel_Name + '/Cmd', qos=2)


class MRC2MQTT(pahoc.Client):
    def __init__(self, Comport='', PrintDebug=False, StrMode=True, SyncClock=False, mqtt_name=None ,broker_address = "localhost",port = 1883,client_id="", clean_session=True, userdata=None, protocol=pahoc.MQTTv5, transport="tcp"):
        #super().__init__(client_id, clean_session, userdata, protocol)
        super().__init__(CallbackAPIVersion.VERSION2, client_id, userdata, protocol)
        # MQTT Broker Settings
        self.broker_address = broker_address  # Replace with your MQTT broker address
        self.port = port  # Default MQTT port

        # Set the callback functions
        self.on_connect = self.on_connect_callback
        self.on_message = self.on_message_callback

        # Connect to the broker
        if self.connect(broker_address, port, 60) != 0:
            print("Couldn't connect to the mqtt broker")
            sys.exit(1)

        self.command_to_execute = []
        self.reading_from_device = False
        self.Comport = Comport
        self.PrintDebug = PrintDebug
        self.UARTconnected = False
        self.State = 0
        self.ComRate = 115200
        self.StrMode = StrMode
        self.force_name = mqtt_name
        if (mqtt_name!=None):
            self.Channel_Name = "COM2MQTT/"+mqtt_name
        self.SyncClock = SyncClock
        self.SyncedClock = False
        self.DeltaTime = 0
        self.start_time = time.time()
        return None

    def on_connect_callback(self, client, userdata, flags, rc,properties):
        print(f"Connected with result code {rc}")

    def on_message_callback(self, client, userdata, msg):
        command = msg.payload.decode()
        print("Received message: {}".format(command))
        command = eval(command)
        self.messages.append(command)


    def execute_command_from_que (self):
        if len(self.messages)>0:
            command = self.messages.pop(0)
            if (command[0][0]==self.force_name+'_MRC') and (command[0][1]=='Set'):
                if (command[0][2]=='Rate'):
                    rate = int(float(command[0][3])*100)
                    try:
                        self.instrument.write_registers(35, [rate])
                    except:
                        print("Failed sending command")
                if (command[0][2]=='TGSP'):
                    tgsp = int(float(command[0][3])*10)
                    try:
                        self.instrument.write_registers(2, [tgsp])
                    except:
                        print("Failed sending command")
                if (command[0][2]=='RMSP'):
                    self.rmsp = float(float(command[0][3]))
                    try:
                        if (self.rmsp==0):
                            self.instrument.write_registers(276, [0])
                        else:
                            self.instrument.write_registers(276, [1])
                    except:
                        print("Failed sending command")

    def SetComport (self,Comport=''):
        self.Stop()
        self.Comport = Comport

    def Start(self):
        if (self.Comport!='') and (self.Comport!='None') and (self.port!=0):
            self.instrument = minimalmodbus.Instrument(self.Comport, 1)  # port name, slave address (in decimal)
            self.instrument.serial.baudrate = 9600  # Baud
            self.instrument.serial.timeout = 1  # seconds

            self.state = 1
            self.messages = []
            self.subscribe(self.Channel_Name + '/Cmd', qos=2)
            print("Subscribed to : " + self.Channel_Name + '/Cmd')
            self.last_update_time = time.time()-1
            self.loop_start()
            remote_enable = self.instrument.read_registers(276,1)[0]
            if (remote_enable):
                self.rmsp = self.instrument.read_registers(26,1)[0]/10
            else:
                self.rmsp = 0
            self.connected = True

    def Stop(self):
        if (self.connected):
            #self.instrument.write_registers(0x1248, [0])
            self.instrument.serial.close()
            self.connected=False
            self.loop_stop()
            self.disconnect()

    def Generate_status_text(self):
        try:
            if (self.rmsp != 0):
                self.instrument.write_registers(26, [int(10 * self.rmsp)])
            pv_read = self.instrument.read_registers(1, 1)[0] / 10
            tg_sp_read = self.instrument.read_registers(2, 1)[0] / 10
            rmt_sp_read = self.instrument.read_registers(26, 1)[0] / 10
            rate_read = self.instrument.read_registers(35, 1)[0] / 100
            remote_enable = self.instrument.read_registers(276, 1)[0]
            textprint = "{'Name':'" + self.force_name + "_MRC','Type':'MRC','Time':%d,'PV':%.1f,'TGSP':%.1f,'RMSP':%.1f,'REN':%d,'Rate':%.2f}" \
                        % (1000 * (time.time()), pv_read, tg_sp_read, rmt_sp_read, remote_enable,
                           rate_read)  # -self.start_time
        except:
            self.reading_from_device = False
            print("Error getting data from MRC - try again")
            textprint = "{'Name':'" + self.force_name + "_MRC','Type':'MRC','Time':%d,'PV':%.1f,'TGSP':%.1f,'RMSP':%.1f,'REN':%d,'Rate':%.2f}" \
                        % (1000 * (time.time()), -1, -1, -1, -1, -1)
        return textprint

    def Update(self):
        if (self.connected):
            self.execute_command_from_que()
            if (time.time()-self.last_update_time > 1):
                self.last_update_time = time.time()
                textprint = self.Generate_status_text()
                if (self.PrintDebug):
                    print (textprint)
                self.publish(self.Channel_Name + "/Data", textprint, qos=2)
                self.subscribe(self.Channel_Name + '/Cmd', qos=2)
