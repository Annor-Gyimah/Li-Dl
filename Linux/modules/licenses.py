import sys
import uuid
import hashlib
import requests
import getmac
import json
import os
from .utils import log
import psutil
from cryptography.fernet import Fernet
import base64



class EnhancedLicenseManager:
    def __init__(self, app_name=".myapp"):

        if os.name == 'nt': # Windows
            config_dir = os.path.join(os.getenv('APPDATA', ''), app_name)
        
        elif os.name == 'posix': # Mac and Linux
            config_dir = os.path.join(os.path.expanduser('~'), app_name)
        
        else:
            config_dir = os.path.join(os.path.expanduser('~'), app_name)


        # Ensure config directory exist
        os.makedirs(config_dir, exist_ok=True)

        # License path file
        self.license_file = os.path.join(config_dir, 'licenses.json')


        # API URL 
        self.api_url = "http://localhost:8000/api/licenses"

        # Machine ID
        self.machine_id = self.get_machine_id()

        # Key file path
        self.key_file = os.path.join(config_dir, 'key.key')

        # Encryption key
        self.cipher = self._initialize_cipher()


    def _initialize_cipher(self):
        """Initialize or load the encryption key."""
        if not os.path.exists(self.key_file):
            # Generate a new key if it doesn't exist
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        else:
            # Load the existing key
            with open(self.key_file, 'rb') as f:
                key = f.read()
        return Fernet(key)

    def _encrypt(self, data):
        """Encrypt data using the encryption key."""
        return self.cipher.encrypt(data.encode())

    def _decrypt(self, encrypted_data):
        """Decrypt data using the encryption key."""
        return self.cipher.decrypt(encrypted_data).decode()

    def _read_license_file(self):
        """Read and decrypt license information from the JSON file."""
        try:
            if os.path.exists(self.license_file):
                with open(self.license_file, 'rb') as f:
                    encrypted_data = f.read()
                    decrypted_data = self._decrypt(encrypted_data)
                    return json.loads(decrypted_data)
            return None
        except (json.JSONDecodeError, IOError, Exception) as e:
            print(f"Error reading license file: {e}")
            return None

    def _write_license_file(self, license_data):
        """Encrypt and write license information to the JSON file."""
        try:
            data_str = json.dumps(license_data, indent=4)
            encrypted_data = self._encrypt(data_str)
            with open(self.license_file, 'wb') as f:
                f.write(encrypted_data)
        except Exception as e:
            print(f"Error writing to license file: {e}")
    
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
    

    # def _read_license_file(self):
    #     """Read license information from JSON file"""
    #     try:
    #         if os.path.exists(self.license_file):
    #             with open(self.license_file, 'r') as f:
    #                 return json.load(f)
    #         return None
    #     except (json.JSONDecodeError, IOError) as e:
    #         return None
        
    
    # def _write_license_file(self, license_data):
    #     """Write license information from JSON file"""
    #     try:
    #         with open(self.license_file, 'w') as f:
    #             json.dump(license_data, f, indent=4)
    #     except (IOError) as e:
    #         log(f'Error writing to license file {e}')


    def activate_trial(self):
        """Activating trial licenses"""
        try:
            # Send trial activation requests
            response = requests.post(
                f"{self.api_url}/trial-activate/",
                json={'machine_id': self.machine_id}
            )

            if response.status_code == 201:
                # Save trial license information to a file
                trial_data = response.json()
                license_data = {
                    'machine_id': self.machine_id,
                    'license_key': f"TRIAL-{self.machine_id[:32]}",
                    'status': 'TRIAL',
                    'trial_start': trial_data.get('trial_start'),
                    'expiry_date': trial_data.get('expiry_date'),
                    'days_remaining': trial_data.get('days_remaining')
                }

                # Write license to a file
                self._write_license_file(license_data)

                return license_data
            
            return None

        except Exception as e:
            log(f"Error activating trial {e}")
            return None
        

    def check_license_status(self, force_server_check=False):
        """
        Check license status with fallback to local file
        
        :param force_server_check: Force verification with server even if local file exists
        :return: License status dictionary
        """

        # First check local license file
        local_license = self._read_license_file()

        # If local license file exists and not forced to check server
        if local_license and not force_server_check:
            try:
                # Verify local license with server
                response = requests.post(
                    f"{self.api_url}/verify/",
                    json = {
                        'machine_id': self.machine_id,
                        'license_key': local_license.get('license_key')
                    }
                )
                print(f'this is : {response}')

                # If server verification is successful
                if response.status_code == 200:
                    server_status = response.json()

                    # Update local license file if server differs
                    if server_status.get('status') != local_license.get('status'):
                        local_license['status'] = server_status.get('status')
                        local_license['days_remaining'] = server_status.get('days_remaining')
                        local_license['message'] = server_status.get('message')
                        # if license_status.get('valid') == True:
                        #     local_license['valid'] = False
                        # else:
                        #     local_license['valid'] = True

                        self._write_license_file(local_license)
                    print(server_status)
                    return server_status
                # else:
                #     if local_license.get('status') == 'ACTIVE':
                #       return local_license
                    
            except requests.RequestException:
                # If server is unreachable, return local license status
                print('returning local license')
                return local_license


            
        # If no local license or forced server check
        try:
            response = requests.post(
                f"{self.api_url}/verify/",
                json={
                    'machine_id': self.machine_id,
                    'license_key': local_license.get('license_key') if local_license else None
                }
            )
            
            if response.status_code == 200:
                license_status = response.json()
                print(license_status)
                self._write_license_file(license_status)
                
                # Save server response to local file
                if license_status.get('valid'):
                    print('yes executed here')
                    self._write_license_file(license_status)
                
                return license_status
        
        except Exception as e:
            log(f"License check error: {e}")
        
        # Fallback if all checks fail
        return {
            'valid': False, 
            'status': 'INVALID', 
            'message': 'Unable to verify license'
        }
    

    
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
            log(f"License upgrade error: {e}")
            return None
        
    
    def final_license_status_check(self):
        """
        Check license status with fallback to local file
        
        :param force_server_check: Force verification with server even if local file exists
        :return: License status dictionary
        """

        # First check local license file
        local_license = self._read_license_file()

        # If local license file exists and not forced to check server
        if local_license:
            try:
                # Verify local license with server
                response = requests.post(
                    f"{self.api_url}/verify/",
                    json = {
                        'machine_id': self.machine_id,
                        'license_key': local_license.get('license_key')
                    }
                )

                # If server verification is successful
                if response.status_code == 200:
                    server_status = response.json()

                    # Update local license file if server differs
                    if server_status.get('status') != local_license.get('status') or server_status.get('days_remaining') != local_license.get('days_remaining'):
                        local_license['status'] = server_status.get('status')
                        local_license['expiry_date'] = server_status.get('expiry_date')
                        local_license['days_remaining'] = server_status.get('days_remaining')
                        local_license['message'] = server_status.get('message')
                        # if license_status.get('valid') == True:
                        #     local_license['valid'] = False
                        # else:
                        #     local_license['valid'] = True
                        print('Yes wrote it')
                        self._write_license_file(local_license)
                    print(f"FINAL LICENSE STATUS CHECK{server_status}")
                    return server_status
                # else:
                #     if local_license.get('status') == 'ACTIVE':
                #       return local_license
                    
            except requests.RequestException:
                # If server is unreachable, return local license status
                print('returning local license')
                return local_license




