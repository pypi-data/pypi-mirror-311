from modbus_connection import MyModbusConnection
from src.constants import *
import time

class FlexStreamDevice:

    def __init__(self, ip: str):
        self.connection = MyModbusConnection(ip,502)
        self.connection.connect()

    def __del__(self):
        """
        Destructor to ensure the connection is properly disconnected
        when the object is destroyed.
        """
        if self.connection:
            try:
                self.connection.disconnect()
                print("Connection successfully disconnected.")
            except Exception as e:
                print(f"Error while disconnecting: {e}")

    def get_device_name(self):
        """
        Get the device name from the Modbus register.
        :return: Device name as a string.
        """
        return self.name

    def set_primary_dilution_flow_rate(self, flow_rate):
        """
        Set the primary dilution flow rate (register 1338).
        :param flow_rate: Desired flow rate in sccm (Standard Cubic Centimeters per Minute).
        """
        self.connection.write(1345, flow_rate)

    def set_secondary_dilution_flow_rate(self, flow_rate):
        """
        Set the secondary dilution flow rate (register 1346).
        :param flow_rate: Desired flow rate in sccm.
        """
        self.connection.write(SECONDARY_DILUTION_FLOW_RATE_REGISTER, flow_rate)

    def set_secondary_component_flow_rate(self, flow_rate):
        """
        Set the secondary component flow rate (register 1347).
        :param flow_rate: Desired flow rate in sccm.
        """
        self.connection.write(SECONDARY_COMPONENT_FLOW_RATE_REGISTER, flow_rate)

    def set_target_source_module(self, module):
        """
        Sets the target source module for gas emission.

        Parameters:
            module (int): Module code (1=Base, 2=PM1, 3=PM2, 4=PM3, 5=PM4, 6=PM5).

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        return self.connection.write(TARGET_SOURCE_MODULE_REGISTER, module)

    def set_new_mode(self, mode_value):
        """
        Sets a new system mode by clearing the confirmation register, writing the new mode to the mode register,
        and then checks the confirmation register to ensure it was set successfully.

        Parameters:
            mode_value (int): The mode to set (0=standby, 1=zero, 2=span_by_flow, 3=span_by_conc, 4=purge)

        Returns:
            bool: True if mode was set successfully, False otherwise.
        """
        # Step 1: Clear the confirmation register (write 0 to MODE_CONFIRM_REGISTER)
        if not self.connection.write(MODE_CONFIRM_REGISTER, 0):
            print(f"Failed to clear confirmation register {MODE_CONFIRM_REGISTER}")
            return False

        # Step 2: Write the mode to MODE_REGISTER
        self.connection.write(MODE_REGISTER, mode_value)

        time.sleep(3)
        # Step 3: Read the confirmation register (MODE_CONFIRM_REGISTER) for the mode status
        confirm_value = self.connection.read(MODE_CONFIRM_REGISTER)
        mode_mapping = {
            0:'standby',
            1: "zero",
            2: "span_by_flow",
            3: "span_by_concentration"
        }

        # Step 4: Check the confirmation response
        if confirm_value == MODE_CONFIRM_SUCCESS:
            print(f"Mode {mode_mapping[mode_value]} set successfully.")
            return True
        elif confirm_value == MODE_CONFIRM_FAILURE:
            print(f"Mode {mode_mapping[mode_value]} could not be initiated.")
            error = device.connection.read(MODE_INIT_ERROR_CODE)
            error_mapping = {
                0: "No error",
                1: "Flow low limit fail",
                2: "Flow low limit warning",
                3: "Flow normal (not reported)",
                4: "Flow high limit warning",
                5: "Flow high limit fail",
                6: "Invalid flow requested"
            }
            print(error_mapping[error])
            return False
        else:
            print(f"Unexpected response in confirmation register: {confirm_value}")
            return False

    def get_mode(self):
        mode = self.connection.read(MODE_REGISTER)
        if mode == 0:
            return  "Standby"
        if mode == 1:
           return "Zero"
        if mode == 2:
            return "Span-by-flow"
        if mode == 3:
            return "Span-by-conc"

    def set_target_tube(self, tube_number):
        """
        Sets the target tube number within the selected permeation or source module.

        Parameters:
            tube_number (int): The tube to set as the target, ranging from 1 to 8.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        return self.connection.write(TARGET_TUBE_REGISTER, tube_number)

    def configure_module_span_status(self, base_span, pm1_span, pm2_span, pm3_span, pm4_span, pm5_span):
        """
        Configures the span status for multiple source modules.
        Each module can be set to either "keep on standby" (0) or "allow span" (1).

        :param base_span: 0 to keep the Base module on standby, 1 to allow the Base module to span.
        :param pm1_span: 0 to keep PM1 module on standby, 1 to allow the PM1 module to span.
        :param pm2_span: 0 to keep PM2 module on standby, 1 to allow the PM2 module to span.
        :param pm3_span: 0 to keep PM3 module on standby, 1 to allow the PM3 module to span.
        :param pm4_span: 0 to keep PM4 module on standby, 1 to allow the PM4 module to span.
        :param pm5_span: 0 to keep PM5 module on standby, 1 to allow the PM5 module to span.
        :return: None
        """
        self.connection.write(MODULE_SPAN_STATUS_REGISTER_BASE, base_span)
        self.connection.write(MODULE_SPAN_STATUS_REGISTER_BASE + 1, pm1_span)
        # self.connection.write(MODULE_SPAN_STATUS_REGISTER_BASE + 2, pm2_span)
        # self.connection.write(MODULE_SPAN_STATUS_REGISTER_BASE + 3, pm3_span)
        # self.connection.write(MODULE_SPAN_STATUS_REGISTER_BASE + 4, pm4_span)
        # self.connection.write(MODULE_SPAN_STATUS_REGISTER_BASE + 5, pm5_span)

    def set_minimum_output_flow(self, flow_rate):
        """
        Sets the minimum output flow (in sccm) required at the downstream "Span Gas Out" port.
        This is configured in register 1342.
        The flow rate should meet or exceed the 'low fail' limit of the secondary mass flow controller
        if a Secondary Dilution module is installed. Set to 0 if not used.

        :param flow_rate: The minimum flow rate to be set in sccm.
        :return: None
        """
        return self.connection.write(MIN_OUTPUT_FLOW_REGISTER, flow_rate)

    def set_concentration_unit(self, unit_code=0):
        """
        Sets the concentration unit for the system.
        The unit code corresponds to a specific unit of measurement for concentration.
        The default unit is ppmv (parts per million by volume), which corresponds to unit_code = 0.

        :param unit_code: The unit code to set for concentration measurement.
                          0=ppmv, 1=ppbv, 2=pptv.
        :return: None
        """
        return self.connection.write(CONCENTRATION_UNIT_REGISTER, unit_code)

    def set_target_concentration(self, concentration_value):
        """
        Sets the target concentration (in units from CONCENTRATION_UNIT_REGISTER) in register 9001.
        A value of 0.0 vents all source modules using the primary dilution flow rate
        (register 1338), and secondary dilution/component flow rates (registers 1346, 1347).

        :param concentration_value: Desired target concentration.
        :return: None
        """
        return self.connection.write_float_to_registers(TARGET_CONCENTRATION_REGISTER, concentration_value)

    def set_zero_mode(self, primary_dilution_flow_rate: int, secondary_dilution_installed: bool = False,
                      humidified_gas_installed: bool = False, target_rh_setpoint: float = 0.0):
        """
        Sets the FlexStream device to zero mode using the primary dilution flow rate and optional secondary and
        humidified gas configurations.

        Args:
            primary_dilution_flow_rate (int): The desired zero primary dilution flow rate in sccm (without decimal fraction).
            secondary_dilution_installed (bool): True if secondary dilution module is installed, otherwise False.
            humidified_gas_installed (bool): True if humidified gas module is installed, otherwise False.
            target_rh_setpoint (float): Target %RH setpoint (multiplied by 10). Set to 0 to turn off %RH generation.

        Returns:
            bool: True if zero mode is confirmed, False otherwise.
        """

        # Write the desired zero primary dilution flow rate into register
        self.connection.write(PRIMARY_DILUTION_FLOW_RATE_REGISTER , primary_dilution_flow_rate)

        # If secondary dilution module is installed, set registers 1346 and 1347 to 0
        if secondary_dilution_installed:
            self.connection.write(SECONDARY_DILUTION_FLOW_RATE_REGISTER , 0)
            self.connection.write(SECONDARY_COMPONENT_FLOW_RATE_REGISTER , 0)


        # If humidified gas module is installed, set the target %RH setpoint
        if humidified_gas_installed:
            target_rh_value = int(target_rh_setpoint * 10)
            self.connection.write(TARGET_RH, target_rh_value)
        # Sets the Zero mode
        return self.set_new_mode(1)




    def set_target_humidity(self, humidity_percent):
        """
        Set the target humidity level by writing to register 1370.

        :param humidity_percent: The desired humidity level in percentage (0 to 100).
        The value is converted by multiplying by 10 to match the register's scale.
        For example, a humidity value of 50.0 will be written as 500 to register 1370.
        """
        return self.connection.write(TARGET_HUMIDITY_REGISTER, humidity_percent)


    def check_confirmation_mode(self):
        time.sleep(2)
        result = self.connection.read(MODE_CONFIRM_REGISTER)
        if result == 2:
            print("Mode changed successfully")
        else:
            print("Mode didn't changed correctly")

    def clear_confirmation_mode(self):
        """
        Clears the confirmation register (MODE_CONFIRM_REGISTER).
        This register is typically used to store the status of the last command or mode change.
        Writing a value of 0 to this register resets its status, allowing for a fresh operation.

        Returns:
            bool: True if the write operation to clear the confirmation register was successful, False otherwise.
        """
        return self.connection.write(MODE_CONFIRM_REGISTER, 0)

    def write_component_properties(self, e_rate: float, m_weight: float, temp: float):
        """
        Writes component properties (emission rate, molecular weight, and temperature) to specified Modbus registers.

        :param e_rate: Emission rate as a floating-point value to write to the E_RATE_REGISTER.
        :param m_weight: Molecular weight as a floating-point value to write to the M_WEIGHT_REGISTER.
        :param temp: Temperature as a floating-point value to write to the TEMP_REGISTER.
        """

        # Write emission rate to its designated Modbus register
        self.connection.write_float_to_registers(E_RATE_REGISTER, e_rate)

        # Write molecular weight to its designated Modbus register
        self.connection.write_float_to_registers(M_WEIGHT_REGISTER, m_weight)

        # Write temperature to its designated Modbus register
        self.connection.write_float_to_registers(TEMP_REGISTER, temp)

    def set_standby(self):
        """
        Sets the FlexStream device to standby mode by writing appropriate values to Modbus registers.
        It clears the MODE_CONFIRM_REGISTER (1318) and checks for a confirmation of standby mode(done inside set_new_mode function)

        Returns:
            bool: True if standby mode is confirmed, False otherwise.
        """
        if self.set_new_mode(0):
            return True
        else:
            return False

    def span_by_concentration(self, module, tube_number, concentration, humidity=None):
        # Set source and target parameters
        self.set_target_source_module(module)
        self.set_target_tube(tube_number)
        self.configure_module_span_status(base_span=1, pm1_span=0, pm2_span=0, pm3_span=0,
                                          pm4_span=0, pm5_span=0)

        # Set flow rates
        # only if Secondary Dilution module is installed.
        # self.set_minimum_output_flow(500)  # or desired minimum flow (set primary dilution flow rate)
        # self.set_primary_dilution_flow_rate(500)  # Example: Set primary dilution flow rate to 200 sccm
        # self.set_secondary_dilution_flow_rate(0)  # Example: Set secondary dilution flow rate if applicable
        # self.set_secondary_component_flow_rate(0)  # Example: Set secondary component flow rate if applicable

        # Set concentration parameters
        self.set_concentration_unit()
        self.set_target_concentration(concentration)

        # Optional: Set humidity
        if humidity is not None:
            self.set_target_humidity(humidity)
        self.set_target_humidity(0)


        # Set span-by-concentration mode
        return self.set_new_mode(3)



    def span_by_flow(self, primary_flow: int, secondary_flow=0, secondary_component_flow=0,
                     base_span=0, pm1_span=0, pm2_span=0, pm3_span=0, pm4_span=0, pm5_span=0,
                     concentration_unit=0):
        """
        Configures the FlexStream to operate in span-by-flow mode.

        Parameters:
            primary_flow (int): Desired primary dilution flow rate (in sccm without decimals).
            secondary_flow (int): Desired secondary dilution flow rate (in sccm without decimals).
                                  Default is 0 (no secondary dilution).
            secondary_component_flow (int): Desired secondary component flow rate (in sccm x 10).
                                             Default is 0 (no secondary dilution).
            base_span (int): 0 = Keep base source module on standby, 1 = Allow span. Default is 0.
            pm1_span (int): PM1 source module status (0 = standby, 1 = allow span). Default is 0.
            concentration_unit (int): 0 = ppmv, 1 = ppbv, 2 = pptv. Default is 0 (ppmv).

        Returns:
            bool: True if succeed False otherwise
        """
        # Set concentration unit
        self.set_concentration_unit(concentration_unit) #0=ppmv, 1=ppbv, 2=pptv
        # Set flow rates
        # Step 1: Write the desired zero primary dilution flow rate into register
        self.connection.write(PRIMARY_DILUTION_FLOW_RATE_REGISTER , primary_flow)

        # Step 2: If secondary dilution module is installed, set registers 1346 and 1347 to 0

        self.connection.write(SECONDARY_DILUTION_FLOW_RATE_REGISTER , secondary_flow)
        self.connection.write(SECONDARY_COMPONENT_FLOW_RATE_REGISTER , secondary_component_flow)

        # Configure span status for modules
        self.configure_module_span_status(base_span,pm1_span,pm2_span,pm3_span,pm4_span,pm5_span)


        # Set span-by-flow mode
        if self.set_new_mode(2):
            return True
        else:
            return False
    #BASE PARAMETERS
    def read_base_flow(self):
        result = self.connection.read(BASE_FLOW)
        print(f"Base flow rate is {result} sscm")
        return result

    def read_base_sp(self):
        result = self.connection.read(BASE_SP)
        print(f"Base flow set point is {result}")
        return result

    def read_base_temp(self):
        result = self.connection.read(BASE_TEMP) / 10
        print(f"Base oven temperature is {result} C")
        return result

    # DUT PARAMETERS
    def read_hg_dut_temp(self):
        result = self.connection.read(HG_DUT_TEMP) / 10
        print(f"HG dut temperature is {result} C")
        return result

    def read_hg_dut_rh(self):
        result = self.connection.read(HG_DUT_RH) / 10
        print(f"HG dut RH is {result} %")
        return result

    def read_hg_flow(self):
        result = self.connection.read(HG_FLOW)
        print(f"HG module flow rate is {result} sscm")
        return result

    def read_hg_dut_sp(self):
        result = self.connection.read(HG_DUT_SP) / 10
        print(f"HG dut set point is {result} %")
        return result

    # NEAR EXIT OF HG MODULE
    def read_hg_device_temp(self):
        result = self.connection.read(HG_DEVICE_TEMP) / 10
        print(f"HG temp near exit of HG module is {result} C")
        return result

    def read_hg_device_rh(self):
        result = self.connection.read(HG_DEVICE_RH) / 10
        print(f"HG RH near exit of HG module is {result} %")
        return result

    def read_hg_device_ps(self):
        result = self.connection.read(HG_DEVICE_PS)
        print(f"HG pressure near exit of HG module is {result} psig")
        return result
    def read_base_concentration(self):
        result = self.connection.read_float_from_registers(BASE_CONCENTRATION_REGISTERS)
        print(f"Base concentration {result} ppm")
        return result

# TODO get component name, figure out how to read words from modbus
    def read_component_name(self):
        pass
if __name__ == "__main__":
    modbus_server_ip = '192.168.1.103'
    modbus_port = 502

    # Create a Modbus TCP client instance
    device = FlexStreamDevice(modbus_server_ip,"fs_01")
    # device.span_by_flow(500,base_span=1)
    # time.sleep(10)
    device.span_by_concentration(1,1,3)
    for i in range(20):
        print(device.connection.read_float_from_registers(8011))
        time.sleep(1)
    device.set_standby()
    # device.set_zero_mode(primary_dilution_flow_rate=2000,humidified_gas_installed=True,target_rh_setpoint=50)
    #
    # for i in range(200):
    #     device.read_hg_dut_rh()
    #     device.read_hg_dut_temp()
    #     device.read_hg_flow()
    #     device.read_hg_dut_sp()
    #
    #     # device.read_hg_device_ps()
    #     # device.read_hg_device_rh()
    #     # device.read_hg_device_temp()
    #     #
    #     # device.read_base_sp()
    #     # device.read_base_temp()
    #     device.read_base_flow()
    #     time.sleep(1)
    # device.set_zero_mode(primary_dilution_flow_rate=2000,target_rh_setpoint=0)
    # for i in range(10):
    #     device.read_hg_dut_rh()
    #     device.read_hg_dut_temp()
    #     device.read_hg_flow()
    #     device.read_hg_dut_sp()
    #
    #     device.read_hg_device_ps()
    #     device.read_hg_device_rh()
    #     device.read_hg_device_temp()
    #
    #     device.read_base_sp()
    #     device.read_base_temp()
    #     device.read_base_flow()
    #     time.sleep(2)

