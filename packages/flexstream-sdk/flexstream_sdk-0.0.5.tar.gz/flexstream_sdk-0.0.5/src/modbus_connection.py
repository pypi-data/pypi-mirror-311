
from abc import ABC, abstractmethod
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
import struct
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder


class ModbusConnection(ABC):
    def __init__(self, ip: str, port: int):
        self.modbus_ip = ip
        self.modbus_port = port
        self.client = None

    @abstractmethod
    def connect(self):
        """Connect to the Modbus device."""
        pass

    @abstractmethod
    def disconnect(self):
        """Disconnect from the Modbus device."""
        pass

    @abstractmethod
    def read(self, register):
        """Read a register from the Modbus device."""
        pass

    @abstractmethod
    def write(self, register, value):
        """Write a value to a register on the Modbus device."""
        pass




class MyModbusConnection(ModbusConnection):
    def connect(self):
        self.client = ModbusTcpClient(self.modbus_ip, port=self.modbus_port)
        if self.client.connect():
            print(f"Connected to Modbus at {self.modbus_ip}:{self.modbus_port}")
        else:
            print(f"Failed to connect to Modbus at {self.modbus_ip}:{self.modbus_port}")

    def disconnect(self):
        if self.client:
            self.client.close()
            print(f"Disconnected from Modbus at {self.modbus_ip}:{self.modbus_port}")

    def read(self, register):
        try:
            pymodbus_register = register - 1
            result = self.client.read_holding_registers(pymodbus_register, 1)
            if isinstance(result, ModbusIOException) or result.isError():
                print(f"Error reading register {register}")
                print(result)
                return None
            return result.registers[0]
        except Exception as e:
            print(f"Exception while reading register {register}: {e}")
            return None

    def write(self, register, value):
        try:
            pymodbus_register = register - 1
            result = self.client.write_register(pymodbus_register, value)
            if isinstance(result, ModbusIOException) or result.isError():
                print(result)
                print(f"Error writing value {value} to register {register}")
                return False
            print(result)
            return True
        except Exception as e:
            print(f"Exception while writing to register {register}: {e}")
            return False


    def write_float_to_registers(self, register, value):
        """
        Writes a floating-point value to two consecutive Modbus registers, probably will use float_to_registers.
        :param register: Starting address of the two consecutive registers.
        :param value: Floating-point value to write.
        """
        pymodbus_register = register - 1
        # Create a BinaryPayloadBuilder to build the payload
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)  # Use little-endian byte order
        builder.add_32bit_float(value)  # Add a 32-bit float to the payload

        # Build the payload, which will be two 16-bit registers
        payload = builder.build()
        result = self.client.write_registers(pymodbus_register, payload,skip_encode=True)
        if isinstance(result, ModbusIOException) or result.isError():
            print(result)
            print(f"Error writing value {value} to register {register}")
            return False
        print(result)
        return True

    def read_float_from_registers(self, register):
        """
        Reads a floating-point value from two consecutive Modbus registers.
        :param register: Starting address of the two consecutive registers.
        :return: Floating-point value.
        """
        try:
            pymodbus_register = register - 1

            # Read two consecutive 16-bit registers from Modbus
            result = self.client.read_holding_registers(pymodbus_register, 2)


            # Create a BinaryPayloadDecoder to interpret the registers as a float
            decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.BIG,wordorder=Endian.LITTLE)

            # Decode the 32-bit float from the registers
            float_value = decoder.decode_32bit_float()

            return float_value

        except Exception as e:
            print(f"Exception while reading from register {register}: {e}")
            return None