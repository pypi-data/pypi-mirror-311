import os
import subprocess
import re
import psutil


class AscendNPUUtils:
    """
    A utility class for interacting with Ascend NPUs using the npu-smi tool.

    This class provides methods to retrieve NPU device information, process information,
    and power dissipation statistics.
    """

    def __init__(self, env_script_path="/usr/local/Ascend/ascend-toolkit/set_env.sh"):
        """
        Initializes the AscendNPUUtils instance and sets the Ascend toolkit environment.

        Args:
            env_script_path (str): The path to the Ascend toolkit environment script.
        """
        self.set_ascend_tool_kit_env(env_script_path)
        self.npu_devices = []
        self.npu_processes = []
        self.power_dissipation = 0

    def set_ascend_tool_kit_env(self, path):
        """
        Sets the Ascend toolkit environment variable.

        Args:
            path (str): The path to the Ascend toolkit environment script.
        """
        os.environ["ASCEND_TOOLKIT_PATH"] = path
        subprocess.run(f"source {path}", shell=True, check=True)

    def npu_smi(self):
        """
        Executes the npu-smi command to retrieve NPU device and process information.

        Returns:
            tuple: A tuple containing lists of NPU devices and processes.
        """
        try:
            result = subprocess.run(['npu-smi', 'info'], capture_output=True, text=True, check=True)
            self.npu_devices, self.npu_processes = self.parse_npu_info(result.stdout)
            return self.npu_devices, self.npu_processes
        except subprocess.CalledProcessError as e:
            print(f"Error running npu-smi: {e}")
            return [], []

    def parse_npu_info(self, output):
        """
        Parses the output from npu-smi to extract NPU device and process information.

        Args:
            output (str): The output from the npu-smi command.

        Returns:
            tuple: Lists of NPU devices and processes.
        """
        npu_devices = self._parse_device_info(output)
        npu_processes = self._parse_process_info(output)
        return npu_devices, npu_processes

    def _parse_device_info(self, output):
        """
        Extracts device information from the npu-smi output.

        Args:
            output (str): The output from the npu-smi command.

        Returns:
            list: A list of dictionaries containing NPU device information.
        """
        device_info_section = output.split("=+\n")[1]
        device_rows = device_info_section.split("-+\n")

        npu_devices = []
        for row in device_rows:
            if not row.strip():
                continue
            parts = row.split("\n")
            row_1 = self._clean_row(parts[0])
            row_2 = self._clean_row(parts[1])

            npu_device = {
                "name": row_1[1],
                "health": row_1[2],
                "power_w": row_1[3],
                "temp_c": row_1[4],
                "hugepages_usage_in": row_1[5],
                "hugepages_usage_out": row_1[6],
                "device": row_2[1],
                "bus_id": row_2[2],
                "aicore_percentage": row_2[3],
                "memory_usage_mb": row_2[4].replace("/", ""),
                "memory_usage_mb_total": row_2[5],
            }
            npu_devices.append(npu_device)

        return npu_devices

    def _parse_process_info(self, output):
        """
        Extracts process information from the npu-smi output.

        Args:
            output (str): The output from the npu-smi command.

        Returns:
            list: A list of dictionaries containing NPU process information.
        """
        process_info_section = output.split("=+\n")[3]
        process_rows = process_info_section.split(" |\n")[:-1]

        npu_processes = []
        for row in process_rows:
            if "No running processes" in row:
                continue
            parts = self._clean_row(row)
            npu_process = {
                "device": parts[1],
                "process_id": parts[2],
                "process_name": parts[3],
                "process_memory_mb": parts[4],
            }
            npu_processes.append(npu_process)

        return npu_processes

    def _clean_row(self, row):
        """
        Cleans a row by splitting and filtering out unwanted characters.

        Args:
            row (str): The row to clean.

        Returns:
            list: A list of cleaned parts.
        """
        return [item for item in row.split(" ") if item and item not in {"|", "/"}]

    def npu_smi_query_power(self, npu_id=0):
        """
        Queries the power dissipation for a specific NPU.

        Args:
            npu_id (int): The index of the NPU.

        Returns:
            float: The power dissipation in watts.
        """
        try:
            result = subprocess.run(['npu-smi', 'info', '-t', 'power', '-i', str(npu_id)],
                                    capture_output=True, text=True, check=True)
            self.power_dissipation = self.parse_npu_smi_query_power(result.stdout)
            return self.power_dissipation
        except subprocess.CalledProcessError as e:
            print(f"Error running npu-smi: {e}")
            return None

    def parse_npu_smi_query_power(self, output):
        """
        Parses the output of the npu-smi power query.

        Args:
            output (str): The output from the power query.

        Returns:
            float: The power dissipation in watts, or None if not found.
        """
        match = re.search(r"\(W\)\s+:\s+([0-9]*\.?[0-9]+)", output)
        return float(match.group(1)) if match else None

    def list_npu_processes(self):
        """
        Returns a list of all processes running on the NPU.

        Returns:
            list: A list of dictionaries containing process information.
        """
        self.npu_smi()  # Update processes
        return self.npu_processes

    def get_memory_info(self, device_index=0):
        """
        Returns the total memory usage of the specified NPU device.

        Args:
            device_index (int): The index of the NPU device. Defaults to 0 for the first device.

        Returns:
            str: A string with total and used memory information for the specified NPU device.
        """
        self.npu_smi()  # Update device info
        if self.npu_devices:
            device = self.npu_devices[device_index]
            return f"Memory Usage: {device['memory_usage_mb']} MB / {device['memory_usage_mb_total']} MB"
        return "No NPU devices found."
