#
# psuutil.py
# Platform-specific PSU status interface for SONiC
#


import os.path

try:
    from sonic_psu.psu_base import PsuBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


class PsuUtil(PsuBase):
    """Platform-specific PSUutil class"""

    """CPLD address"""
    PSU_DIR = "/sys/bus/i2c/devices/i2c-inv_cpld/"

    def __init__(self):
        PsuBase.__init__(self)

    # Get sysfs attribute
    def get_attr_value(self, attr_path):
        
        retval = 'ERR'        
        if (not os.path.isfile(attr_path)):
            return retval

        try:
            with open(attr_path, 'r') as fd:
                retval = fd.read()
        except Exception as error:
            logging.error("Unable to open ", attr_path, " file !")

        retval = retval.rstrip(' \t\n\r')
        return retval
    
    def get_num_psus(self):
        """
        Retrieves the number of PSUs available on the device
        :return: An integer, the number of PSUs available on the device
         """
        MAX_PSUS = 2
        return MAX_PSUS

    def get_psu_status(self, index):
        """
        Retrieves the oprational status of power supply unit (PSU) defined
                by index <index>
        :param index: An integer, index of the PSU of which to query status
        :return: Boolean, True if PSU is operating properly, False if PSU is\
        faulty
        """
        status = 0
        attr_file ='psu'+ str(index)
        attr_path = self.PSU_DIR +'/' + attr_file
        normal_attr_value = '1:normal'
        unpower_attr_value = '0:unpowered'
        attr_value = self.get_attr_value(attr_path)
        if (attr_value != 'ERR'):
            # Check for PSU presence
            if (attr_value == normal_attr_value):
                    status = 1
            elif (attr_value == unpower_attr_value):
                    status = 0
        return status

    def get_psu_presence(self, index):
        """
        Retrieves the presence status of power supply unit (PSU) defined
                by index <index>
        :param index: An integer, index of the PSU of which to query status
        :return: Boolean, True if PSU is plugged, False if not
        """
        status = 0
        attr_file ='psu'+ str(index)
        attr_path = self.PSU_DIR +'/' + attr_file
        normal_attr_value = '1:normal'
        unpower_attr_value = '0:unpowered'
        attr_value = self.get_attr_value(attr_path)
        if (attr_value != 'ERR'):
            # Check for PSU presence
            if (attr_value == normal_attr_value):
                    status = 1
            if (attr_value == unpower_attr_value):
                    status = 1
        return status
