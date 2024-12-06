from flexstream_device import FlexStreamDevice

class FlexStreamApp:
    def __init__(self, ip : str):

        self.device = FlexStreamDevice(ip)

    def set_zero_mode(self,fil_flow_rate: int,sec_dill_installed = False,hum_gas_installed = False,target_rh_sp = 0):
        mode_success = self.device.set_zero_mode(fil_flow_rate,sec_dill_installed,hum_gas_installed,target_rh_sp)
        if mode_success:
            print(f"Zero mode set successfully with flow rate {fil_flow_rate} and target RH set to {target_rh_sp}")


    def disconnect(self):
        del self.device
        print("Disconnected from device")

    def set_standby_mode(self):
        mode_success = self.device.set_standby()
        if mode_success:
            print("Standby mode set successfully")


    def get_message(self) -> str:
        #TODO will probably need to add more fields to this message
        message_dict = {}
        message_dict['name'] = self.device.get_device_name()
        message_dict['mode'] = self.device.get_mode()
        message_dict['component'] = self.device.read_component_name
        message_dict['dil_flow'] = self.device.read_base_flow()
        message_dict['hg_flow'] = self.device.read_hg_flow()
        message_dict['hg_dut_temp'] = self.device.read_hg_dut_temp()
        message_dict['hg_dut_sp'] = self.device.read_hg_dut_sp()
        message_dict['hg_dut_sensor'] = self.device.read_hg_dut_rh()
        str_representation = str(message_dict)
        return str_representation