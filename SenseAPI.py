"""
 SenseAPI  -Randy Spencer 2022
 Python app to test functions of the Sense API
"""

#username = 'elon@tesla.com'         # Sense's login
#password = 'password'               # Sense's password

# To install support module:
# Python3 -m pip install sense_energy
print ("Initating connection to Sense...")
from sense_energy import Senseable
sense = Senseable(wss_timeout=30,api_timeout=30)
sense.authenticate(username, password)

import asyncio
import sense_link
async def test():
    import time
    def test_devices():
        devices = [PlugInstance("lamp1", start_time=time()-20, alias="Lamp", power=10),
                   PlugInstance("fan1", start_time=time()-300, alias="Fan", power=140)]
        for d in devices:
            yield d
    sl = SenseLink(test_devices)
    await sl.start()
    try:
        await asyncio.sleep(180)  # Serve for 3 minutes
    finally:
        await sl.stop()

if __name__ == "__main__":
    asyncio.run(test())

def myloop(mydict, nest) :                                 # print out contents of dicts and lists
    for i, option in enumerate(mydict, 1):
        if isinstance(mydict[option], dict) :
            if not i % 2 : print()
            print(" " * nest, option, ';')
            myloop(mydict[option], nest + 2)
        elif isinstance(mydict[option], list) :
            if not i % 2 : print()
            print(" " * nest, option, '=')
            listofstrings = False
            for j, suboption in enumerate(mydict[option],1):
                if isinstance(suboption, dict) :
                    print("+", end='')
                    myloop(suboption, nest + 2)
                else :
                    #print(' ', suboption, end = '')
                    listofstrings = True
            if listofstrings : print(" " * (nest+2), mydict[option])
        else :
            print(" " * nest,'{:38}'.format(str(option) + ' : ' + str(mydict[option])), end='' if i % 2 else '\n')
    if i % 2 : print()

lst = ['Refresh', 'Realtime Data', 'Recent Usage', 'Device Names', 'Device Data', 'Device Info', 'Always On Info', 'Monitor Info', 'Monitor Data', 'All API Functions']
opt = 0
while True:
    print()
    sense.update_realtime()                        # Update Sense info
    print('-' * 22, "  Active Devices  ", '-' * 38)
    for i, option in enumerate(sense.active_devices, 1):
        print('{:20}'.format(option), end='' if i % 4 else '\n')
    if i % 4:
        print()
    print('-' * 27, "  Stats  ", '-' * 42)
    fmt = 'Solar Prod:  {:26} Power Usage:  {} watts'
    print(fmt.format(str(int(sense.active_solar_power))+" watts", int(sense.active_power)))
    fmt = 'Frequency:  {:27} Voltages:  {}, {}'
    print(fmt.format(str(round(sense.active_frequency,4))+" hertz", round(sense.active_voltage[0],2), round(sense.active_voltage[1],2)))
    
    sense.get_trend_data('WEEK')
    print('-' * 22, " Weekly Production ", '-' * 37)
    fmt = 'From Grid  {:26}   Production  {} kWh'
    print(fmt.format(str(round(sense.weekly_from_grid,2))+" kWh", round(sense.weekly_production,2)))
    
    fmt = 'To Grid  {:28}   Usage  {} kWh'
    print(fmt.format(str(round(sense.weekly_to_grid, 2))+" kWh", round(sense.weekly_usage,2)))
    
    fmt = 'Net Production  {:23} Production  {} %'
    print(fmt.format(str(round(sense.weekly_net_production,2))+" kWh", sense.weekly_production_pct))
    
    print("Solar Powered ", sense.weekly_solar_powered , "%")
    
    print('-' * 80)
    # Display 3 column menu
    for i, option in enumerate(lst, 1):
        print('{:2} {:25}'.format(i, option), end='' if i % 3 else '\n')
    if i % 3:
        print()
    print('-' * 80)
    # Get user choice
    opt = int(input("Choice (0 to quit): "))
    print()
    nest=0
     # Perform menu option
    if opt == 0:
        break
    if opt == 1:                                           # Refresh
        pass
    elif opt == 2:                                         # Realtime data
        myloop(sense.get_realtime(), nest)
    elif opt == 3:                                         # Recent usage
        myloop(sense.get_all_usage_data(), nest)
    elif opt == 4:                                         # Device names
        sorted_device_names = list(dict.fromkeys(sense.get_discovered_device_names()))
        sorted_device_names.sort()
        for i, option in enumerate(sorted_device_names, 1):
            print('   {:23}'.format(option), end='' if i % 3 else '\n')
        if i % 3:
            print()
    elif opt == 5:                                         # Device data
        for i, option in enumerate(sense.get_discovered_device_data(), 1) :
            myloop(option, nest)
            print(">")
    elif opt == 6:                                         # Device info
        sorted_device_names=[]
        for i, option in enumerate(sense.get_discovered_device_data()):
            sorted_device_names.append(option["name"]+" |"+option["id"]+"|")
        sorted_device_names.sort()
        for i, option in enumerate(sorted_device_names,1):
            print('{:2} {:40}'.format(i, option), end='' if i % 2 else '\n')
        if i % 2:
            print()
        dev = input("Device #: ")
        print("-"*80)
        j,k = 0,int(dev)
        while j < k :
            dev = sorted_device_names[j].split('|')[1]
            j += 1
        myloop(sense.get_device_info(dev), nest)
    elif opt == 7:                                         # Always On info
        myloop(sense.always_on_info(), nest)
    elif opt == 8:                                         # Monitor info
        myloop(sense.get_monitor_info(), nest)
    elif opt == 9:                                         # Monitor data
        myloop(sense.get_monitor_data(), nest)
    elif opt == 10:                                        # All available APIs
        for i, option in enumerate(dir(Senseable), 1):
            print('  {:23}'.format(option), end='' if i % 3 else '\n')
        if i % 3:
            print()
    elif opt == 11:
        print(type(sense.devices()))
