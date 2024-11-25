import sys
import uuid
import hashlib
import requests
import getmac
import json
import os
import psutil


# from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton
# from PySide6.QtGui import QAction, QIcon, QPixmap, QImage, QClipboard

# import sys

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("QMessageBox Success Example")
#         self.setGeometry(100, 100, 400, 300)

#         # Add a button to trigger the success message
#         self.button = QPushButton("Show Success Message", self)
#         self.button.clicked.connect(self.show_success_message)
#         self.button.setGeometry(100, 100, 200, 50)

#     def show_success_message(self):
#         # Create a custom QMessageBox
#         msg_box = QMessageBox(self)
#         msg_box.setWindowTitle("Success")
#         msg_box.setText("The operation was completed successfully!")
#         msg_box.setStandardButtons(QMessageBox.Ok)
#         msg_box.setIconPixmap(QPixmap("../images/icons/cil-3d.png"))  # Custom success icon
#         msg_box.exec()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())




class EnhancedLicenseManager:
    def __init__(self, app_name='.myapp'):
        # Determine the appropriate config directory
        self.config_dir = self._get_config_dir(app_name)
        os.makedirs(self.config_dir, exist_ok=True)
        
        # License file path
        self.license_file = os.path.join(self.config_dir, 'licenses.json')
        
        # API URL (update as needed)
        self.api_url = "http://localhost:8000/api/licenses"
        
        # Machine ID
        self.machine_id = self.get_machine_id()

    def _get_config_dir(self, app_name):
        """Determine the config directory based on the OS."""
        if os.name == 'nt':  # Windows
            return os.path.join(os.getenv('APPDATA', ''), app_name)
        else:  # macOS and Linux
            return os.path.join(os.path.expanduser('~'), app_name)
        
        
        

        
    def get_active_interface_mac(self):
        """Identify the active network interface and get its MAC address."""
        active_interfaces = []
        
        # Iterate through network interfaces and their statuses
        for nic, addrs in psutil.net_if_addrs().items():
            stats = psutil.net_if_stats().get(nic)
            if stats and stats.isup:  # Check if the interface is up (active)
                for addr in addrs:
                    if addr.family == psutil.AF_LINK:  # Check if it's a MAC address
                        active_interfaces.append((nic, addr.address))
        
        if active_interfaces:
            # Assuming the first active interface is the main one
            interface, mac = active_interfaces[1]
            return interface, mac
        return None, None


    def get_machine_id(self):
        """Get a hashed machine ID based on the MAC address of the active interface."""
        interface, mac = self.get_active_interface_mac()
        if interface and mac:
            hashed_mac = hashlib.sha256(mac.encode()).hexdigest()
            # print(f"Hashed MAC: {hashed_mac}")
        else:
            print("No active network interface found!")
        
        return hashed_mac

    # def get_machine_id(self):
    #     """Get unique machine identifier using MAC address"""
    #     mac = getmac.get_mac_address()
    #     return hashlib.sha256(mac.encode()).hexdigest()

    def _read_license_file(self):
        """Read license information from JSON file"""
        try:
            if os.path.exists(self.license_file):
                with open(self.license_file, 'r') as f:
                    return json.load(f)
            return None
        except (json.JSONDecodeError, IOError):
            return None

    def _write_license_file(self, license_data):
        """Write license information to JSON file"""
        try:
            with open(self.license_file, 'w') as f:
                json.dump(license_data, f, indent=4)
        except IOError as e:
            log(f"Error writing license file: {e}")

    def check_license_status(self, force_server_check=False):
        """
        Check license status with fallback to local file
        
        :param force_server_check: Force verification with server even if local file exists
        :return: License status dictionary
        """
        # First, check local license file
        local_license = self._read_license_file()
        

        # If local license exists and the user is offline, use the local license info
        if local_license:
            # If we're offline and the license is valid (ACTIVE), don't force server check
            print('Local response')
            if not force_server_check and self._is_online() is False:
                # If the license is marked as ACTIVE, proceed with the local data
                if local_license.get('status') == 'ACTIVE':
                    return local_license
                else:
                    # If the status is not ACTIVE, it could be expired or invalid, handle it accordingly
                    return {'valid': False, 'status': 'INVALID', 'message': 'License not valid'}

        # If we're online or forced to check with the server, validate with the server
        return self._check_license_with_server(local_license)

    def _is_online(self):
        """Check if the machine is online by pinging the server or performing a request."""
        try:
            response = requests.get(self.api_url, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def _check_license_with_server(self, local_license):
        """Check the license status with the server (force check)"""
        try:
            response = requests.post(
                f"{self.api_url}/verify/",
                json={
                    'machine_id': self.machine_id,
                    'license_key': local_license.get('license_key') if local_license else None
                }
            )

            if response.status_code == 200:
                server_status = response.json()
                
                # if server_status.get('status') != local_license.get('status'):
                #     local_license['status'] = server_status.get('status')
                #     local_license['days_remaining'] = server_status.get('days_remaining')
                #     local_license['message'] = server_status.get('message')
                #     self._write_license_file(server_status)
                
                # Save server response to local file
                if server_status.get('valid'):
                    self._write_license_file(server_status)
                
                return server_status
            else:
                print('NOE')
        except Exception as e:
            print(f"License check error: {e}")
        
        # Fallback if all checks fail
        return {'valid': False, 'status': 'INVALID', 'message': 'Unable to verify license'}

    def activate_trial(self):
        """Activate trial license"""
        try:
            # Send trial activation request
            response = requests.post(
                f"{self.api_url}/trial-activate/",
                json={'machine_id': self.machine_id}
            )

            if response.status_code == 201:
                trial_data = response.json()
                license_data = {
                    'machine_id': self.machine_id,
                    'license_key': f"TRIAL-{self.machine_id[:32]}",
                    'status': 'TRIAL',
                    'trial_start': trial_data.get('trial_start'),
                    'expiry_date': trial_data.get('expiry_date'),
                    'days_remaining': trial_data.get('days_remaining')
                }

                self._write_license_file(license_data)

                return license_data
            return None
        except Exception as e:
            print(f"Error activating trial: {e}")
            return None
        
    def upgrade_license(self, license_key):
        """
        Upgrade from trial to full license
        
        :param license_key: Full license key
        :return: Updated license information
        """
        try:
            response = requests.post(
                f"{self.api_url}/verify/",
                json={
                    'machine_id': self.machine_id,
                    'license_key': license_key
                }
            )
            
            if response.status_code == 200:
                license_data = response.json()
                
                # If license is valid, save to file
                if license_data.get('valid'):
                    self._write_license_file(license_data)
                    return license_data
            
            return None
        
        except Exception as e:
            print(f"License upgrade error: {e}")
            return None







# class EnhancedLicenseManager:
#     def __init__(self, app_name='.myapp'):
#         # Determine the appropriate config directory
#         self.config_dir = self._get_config_dir(app_name)
        
#         # License file path
#         self.license_file = os.path.join(self.config_dir, 'license.json')
        
#         # API URL (update as needed)
#         self.api_url = "http://localhost:8000/api/licenses"
        
#         # Machine ID
#         self.machine_id = self.get_machine_id()

#     def _get_config_dir(self, app_name):
#         """Determine the config directory based on the OS."""
#         if os.name == 'nt':  # Windows
#             return os.path.join(os.getenv('APPDATA', ''), app_name)
#         else:  # macOS and Linux
#             return os.path.join(os.path.expanduser('~'), app_name)

#     def get_machine_id(self):
#         """Get unique machine identifier using MAC address"""
#         mac = getmac.get_mac_address()
#         return hashlib.sha256(mac.encode()).hexdigest()

#     def _read_license_file(self):
#         """Read license information from JSON file"""
#         try:
#             if os.path.exists(self.license_file):
#                 with open(self.license_file, 'r') as f:
#                     return json.load(f)
#             return None
#         except (json.JSONDecodeError, IOError):
#             return None

#     def _write_license_file(self, license_data):
#         """Write license information to JSON file"""
#         try:
#             with open(self.license_file, 'w') as f:
#                 json.dump(license_data, f, indent=4)
#         except IOError as e:
#             print(f"Error writing license file: {e}")

#     def _is_online(self):
#         """Check if the machine is online by pinging the server or performing a request."""
#         try:
#             response = requests.get(self.api_url, timeout=5)
#             return response.status_code == 200
#         except requests.RequestException:
#             return False

#     def check_license_status(self, force_server_check=False):
#         """
#         Check license status with fallback to local file
        
#         :param force_server_check: Force verification with server even if local file exists
#         :return: License status dictionary
#         """
#         # First, check local license file
#         local_license = self._read_license_file()

#         # If local license exists and the user is offline, use the local license info
#         if local_license:
#             # If we're offline and the license is valid (ACTIVE), don't force server check
#             if not force_server_check and self._is_online() is False:
#                 # If the license is marked as ACTIVE, proceed with the local data
#                 if local_license.get('status') == 'ACTIVE':
#                     return local_license
#                 else:
#                     # If the status is not ACTIVE, it could be expired or invalid, handle it accordingly
#                     return {'valid': False, 'status': 'INVALID', 'message': 'License not valid'}

#         # If we're online or forced to check with the server, validate with the server
#         return self._check_license_with_server(local_license)

#     def _check_license_with_server(self, local_license):
#         """Check the license status with the server (force check)"""
#         if self._is_online():
#             try:
#                 response = requests.post(
#                     f"{self.api_url}/verify/",
#                     json={
#                         'machine_id': self.machine_id,
#                         'license_key': local_license.get('license_key') if local_license else None
#                     }
#                 )

#                 if response.status_code == 200:
#                     license_status = response.json()
                    
#                     # Save server response to local file
#                     if license_status.get('valid'):
#                         self._write_license_file(license_status)
                    
#                     return license_status
#             except requests.RequestException as e:
#                 print(f"Error during server license check: {e}")
#                 # If there was a network error, return the local status as fallback
#                 return local_license
#         else:
#             print("Offline, using local license data.")
#             return local_license

#     def activate_trial(self):
#         """Activate trial license"""
#         if self._is_online():
#             try:
#                 # Send trial activation request
#                 response = requests.post(
#                     f"{self.api_url}/trial-activate/",
#                     json={'machine_id': self.machine_id}
#                 )

#                 if response.status_code == 201:
#                     trial_data = response.json()
#                     license_data = {
#                         'machine_id': self.machine_id,
#                         'license_key': f"TRIAL-{self.machine_id[:32]}",
#                         'status': 'TRIAL',
#                         'trial_start': trial_data.get('trial_start'),
#                         'expiry_date': trial_data.get('expiry_date'),
#                         'days_remaining': trial_data.get('days_remaining')
#                     }

#                     self._write_license_file(license_data)

#                     return license_data
#                 return None
#             except requests.RequestException as e:
#                 print(f"Error activating trial: {e}")
#                 return None
#         else:
#             print("Offline, cannot activate trial.")
#             return None



# class EnhancedLicenseManager:
#     def __init__(self, app_name='.myapp'):
#         # Determine the appropriate config directory
#         self.config_dir = self._get_config_dir(app_name)
        
#         # License file path
#         self.license_file = os.path.join(self.config_dir, 'license.json')
        
#         # API URL (update as needed)
#         self.api_url = "http://localhost:8000/api/licenses"
        
#         # Machine ID
#         self.machine_id = self.get_machine_id()

#     def _get_config_dir(self, app_name):
#         """Determine the config directory based on the OS."""
#         if os.name == 'nt':  # Windows
#             return os.path.join(os.getenv('APPDATA', ''), app_name)
#         else:  # macOS and Linux
#             return os.path.join(os.path.expanduser('~'), app_name)

#     def get_machine_id(self):
#         """Get unique machine identifier using MAC address"""
#         mac = getmac.get_mac_address()
#         return hashlib.sha256(mac.encode()).hexdigest()

#     def _read_license_file(self):
#         """Read license information from JSON file"""
#         try:
#             if os.path.exists(self.license_file):
#                 with open(self.license_file, 'r') as f:
#                     return json.load(f)
#             return None
#         except (json.JSONDecodeError, IOError):
#             return None

#     def _write_license_file(self, license_data):
#         """Write license information to JSON file"""
#         try:
#             with open(self.license_file, 'w') as f:
#                 json.dump(license_data, f, indent=4)
#         except IOError as e:
#             print(f"Error writing license file: {e}")

#     def _is_online(self):
#         """Check if the machine is online by pinging the server or performing a request."""
#         try:
#             response = requests.get(self.api_url, timeout=5)
#             return response.status_code == 200
#         except requests.RequestException:
#             return False

#     def check_license_status(self, force_server_check=False):
#         """
#         Check license status with fallback to local file
        
#         :param force_server_check: Force verification with server even if local file exists
#         :return: License status dictionary
#         """
#         # First, check local license file
#         local_license = self._read_license_file()

#         # If we're offline, use the local license info
#         if local_license:
#             # If we're not forcing server check, use the local license status when offline
#             if not force_server_check and not self._is_online():
#                 if local_license.get('status') == 'ACTIVE':
#                     return local_license
#                 else:
#                     # If the license is invalid or expired locally, return that status
#                     return {'valid': False, 'status': 'INVALID', 'message': 'License is invalid or expired'}

#         # If we're online or forced to check with the server, validate with the server
#         return self._check_license_with_server(local_license)

#     def _check_license_with_server(self, local_license):
#         """Check the license status with the server (force check)"""
#         if self._is_online():
#             try:
#                 response = requests.post(
#                     f"{self.api_url}/verify/",
#                     json={
#                         'machine_id': self.machine_id,
#                         'license_key': local_license.get('license_key') if local_license else None
#                     }
#                 )

#                 if response.status_code == 200:
#                     license_status = response.json()
                    
#                     # Save server response to local file
#                     if license_status.get('valid'):
#                         self._write_license_file(license_status)
                    
#                     return license_status
#             except requests.RequestException as e:
#                 print(f"Error during server license check: {e}")
#                 # If there was a network error, return the local status as fallback
#                 return local_license
#         else:
#             print("Offline, using local license data.")
#             return local_license

#     def activate_trial(self):
#         """Activate trial license"""
#         if self._is_online():
#             try:
#                 # Send trial activation request
#                 response = requests.post(
#                     f"{self.api_url}/trial-activate/",
#                     json={'machine_id': self.machine_id}
#                 )

#                 if response.status_code == 201:
#                     trial_data = response.json()
#                     license_data = {
#                         'machine_id': self.machine_id,
#                         'license_key': f"TRIAL-{self.machine_id[:32]}",
#                         'status': 'TRIAL',
#                         'trial_start': trial_data.get('trial_start'),
#                         'expiry_date': trial_data.get('expiry_date'),
#                         'days_remaining': trial_data.get('days_remaining')
#                     }

#                     self._write_license_file(license_data)

#                     return license_data
#                 return None
#             except requests.RequestException as e:
#                 print(f"Error activating trial: {e}")
#                 return None
#         else:
#             print("Offline, cannot activate trial.")
#             return None
