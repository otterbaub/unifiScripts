import pandas as pd
# pip install pandas
import unificontrol as uic
# https://github.com/nickovs/unificontrol

# Controller Username
unifiUsername = 'username'
# Controller User Password
unifPassword = 'password'

# Controller web address (IP or FQDN)
aasControllerAddress = 'customer.domain.com'

# Site Id can be found from the URL of the web page site of the controller
siteId = '99SiteID99'

#File path to the file that has the devices to be changed
renameFile = 'mac_rename.csv'
# list is a .csv
# First line of .csv must contain "mac,name"

# Example:
# mac,name
# 11:22:33:AA:BB:CC,RenameThisDevice

# Initialize and authenticate to Controller
ui = uic.UnifiClient(host=aasControllerAddress, port=8443, username=unifiUsername, password=unifPassword, site=siteId, cert = None)

# Read .csv into Pandas DataFrame, use first line as column names
macRename = pd.read_csv(renameFile,header=[0])

# Return all Network Hardware for the site
response = ui.list_devices()
# Convert JSON response from controller to Pandas DataFrame 
deviceDf = pd.DataFrame(response)
# Filter response to just MAC and Unifi Device ID
deviceDf = deviceDf.filter(['mac','_id'])
# Perform an Inner/Left between the Dataframes
deviceDfMerge = deviceDf.merge(macRename, left_on='mac',right_on='mac')

# Create/define funtcion to rename AP
def renameAP(deviceId, deviceName, deviceMac):
    """
    Renames an access point.

    Args:
        deviceId (str): The ID of the device.
        deviceName (str): The new name for the device.
        deviceMac (str): The MAC address of the device.

    Returns:
        None

    Examples:
        renameAP('12345', 'NewAP', '00:11:22:33:44:55')
    """
    ui.rename_ap(str(deviceId), str(deviceName))
    print(f'{deviceMac} has been changed to {deviceName}.')

# Loop over the list and update the devices on the list
for index, device in deviceDfMerge.iterrows():
    # Call and set the individual attributes of each device
    deviceId = device['_id']
    deviceMac = device['mac']
    deviceName = device['name']
    # Rename the device
    renameAP(deviceId, deviceName, deviceMac)
print("Rename Completed")
#End of Script
