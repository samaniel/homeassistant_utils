############################
#   name: clean_rooms.py   #
#   author: Samaniel       #
############################


##############################################################
############ Dictionary of region ID's and RID's #############
##############################################################
######### ->>ADD YOUR STUFF TO THIS SECTION!!!!!!<<- #########

regionsDictionary = {
    'entrada': {'region_id': '7', 'type': 'rid'},
    //add your stuff
}



##############################################################
######################## Setup vars ##########################
##############################################################
######### ->>ADD YOUR STUFF TO THIS SECTION!!!!!!<<- #########

ENTITY_ID = 'REPLACEME'
PMAP_ID = 'REPLACEME'
USER_PMAPV_ID = 'REPLACEME'



##############################################################
############### Configure cleaning options ###################
##############################################################
twoPass = True if hass.states.get('input_boolean.roombatwopass').state == 'on' else False
swScrub = 1 if hass.states.get('input_boolean.roombascrub').state == 'on' else 0
noAutoPasses = True
vacHigh = True if hass.states.get('input_boolean.roombapowerful').state == 'on' else False
should_mop = True if hass.states.get('input_boolean.roombamop').state == 'on' else False
mopMode = 3 if hass.states.get('input_boolean.roombamopultrawater').state == 'on' else 2

mop_parameters = { 
    "carpetBoost": True, 
    "noAutoPasses": noAutoPasses, 
    "operatingMode": 6, 
    "padWetness": { 
        "disposable": mopMode, 
        "reusable": mopMode 
    }, 
    "swScrub": swScrub, 
    "twoPass": twoPass, 
    "vacHigh": vacHigh
}

vacuum_parameters = { 
    "carpetBoost": False, 
    "noAutoPasses": noAutoPasses, 
    "operatingMode": 2, 
    "twoPass": twoPass, 
    "vacHigh": vacHigh 
}
region_params = mop_parameters if should_mop else vacuum_parameters



##############################################################
## Add toggled rooms from input_booleans to selection_list ###
##############################################################
######### ->>ADD YOUR STUFF TO THIS SECTION!!!!!!<<- #########

selection_list_ordered = []

# Add Boolean State Objects to Selection List if True
if hass.states.get('input_boolean.entrada').state == 'on':
    selection_list_ordered.append(hass.states.get('input_boolean.entrada'))
//add one condition per regionsDictionary entry 
    
# Sort Selections by Timestamp (In Order of Selection)
selection_list_ordered.sort(key=lambda x:x.last_updated)



##############################################################
################## Configure regions field ###################
##############################################################
######### ->>ADD YOUR STUFF TO THIS SECTION!!!!!!<<- #########

regions = []
# Pack Region Data into Region List in Sorted Order
for selection in selection_list_ordered:
    # Hard coded check for boolean states and append region list
    if selection == hass.states.get('input_boolean.entrada'):
        regions.append(
            { 
                "params": region_params,
                "region_id": regionsDictionary['entrada']['region_id'], 
                "type": regionsDictionary['entrada']['type'],
            } 
        )
    //add one condition per regionsDictionary entry (remember to create input_booleans)

        

##############################################################
############# Merge fields to full json and Send #############
##############################################################
commands_to_send = {
        "command": "start",
        "id": "1",
        "ordered": 1,
        "pmap_id": PMAP_ID,
        "regions": regions,
        "select_all": False,
        "user_pmapv_id": USER_PMAPV_ID
}
        

# Send Data to Roomba
hass.services.call('vacuum', 'send_command', { 
    "command": "start",
    "entity_id": ENTITY_ID, 
    "params": commands_to_send 
}, False)



##############################################################
############# Clear all boolean states to false ##############
##############################################################
######### ->>ADD YOUR STUFF TO THIS SECTION!!!!!!<<- #########
hass.states.set('input_boolean.roombatwopass', 'off', '')
hass.states.set('input_boolean.roombascrub', 'off', '')
hass.states.set('input_boolean.roombapowerful', 'off', '')
hass.states.set('input_boolean.roombamop', 'off', '')
hass.states.set('input_boolean.roombamopultrawater', 'off', '')

//add one entry per existing input_boolean, eg:
hass.states.set('input_boolean.entrada', 'off', '')



##############################################################
##########################  LOGS  ############################
##############################################################
logger.warning('Roomba cleaning script finished with params: %s', str(commanddefs))
