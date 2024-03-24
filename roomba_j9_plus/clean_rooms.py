####################################
#   author: DescubriendoelCodigo   #
####################################


##############################################################
############ Dictionary of region ID's and RID's #############
##            ADD YOUR STUFF TO THIS SECTION               ###
##############################################################
regions = {
    'hallway': {'region_id': '3', 'type': 'rid'},
    //fill with your defined regions
}



##############################################################
######################## Setup vars ##########################
##            ADD YOUR STUFF TO THIS SECTION               ###
##############################################################
ENTITY = 'REPLACEME'
PMAP_ID = 'REPLACEME'
USER_PMAPV_ID = 'REPLACEME'
//Replace with your own values



##############################################################
############### Configure cleaning options ###################
##############################################################
twoPass = True if hass.states.get('input_boolean.roombatwopass').state == 'on' else False
swScrub = 1 if hass.states.get('input_boolean.roombascrub').state == 'on' else 0
carpetBoost = True
noAutoPasses = True
vacHigh = True if hass.states.get('input_boolean.roombapowerful').state == 'on' else False
should_mop = True if hass.states.get('input_boolean.roombamop').state == 'on' else False
mopMode = 3 if hass.states.get('input_boolean.roombamopultrawater').state == 'on' else 2

mop_parameters = { 
    "carpetBoost": carpetBoost, 
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
    "carpetBoost": carpetBoost, 
    "noAutoPasses": noAutoPasses, 
    "operatingMode": 2, 
    "twoPass": twoPass, 
    "vacHigh": vacHigh 
}
mopOrVacuumParameters = mop_parameters if should_mop else vacuum_parameters



##############################################################
## Add toggled rooms from input_booleans to selection_list ###
##            ADD YOUR STUFF TO THIS SECTION               ###
##############################################################
selection_list = []

# Add Boolean State Objects to Selection List if True
if hass.states.get('input_boolean.hallway').state == 'on':
    selection_list.append(hass.states.get('input_boolean.hallway'))
//Add one if per input_toggle/region
    
# Sort Selections by Timestamp (In Order of Selection)
selection_list.sort(key=lambda x:x.last_updated)



##############################################################
############# Add rooms and modes to regions list ############
##            ADD YOUR STUFF TO THIS SECTION               ###
##############################################################
regions = []
# Pack Region Data into Region List in Sorted Order
for selection in selection_list:
    # Hard coded check for boolean states and append region list
    if selection == hass.states.get('input_boolean.hallway'):
        regions.append( { 
            "region_id": 3, 
            "type": "rid", 
            "params": mopOrVacuumParameters
        } )
//Add one if per region
        
        

##############################################################
################ Build petition data and Send ################
##############################################################
service_data = {
    'command': 'start',
    'entity_id': ENTITY,
    'params': { 
        "pmap_id": PMAP_ID, 
        "user_pmapv_id": USER_PMAPV_ID, 
        "ordered": 1, # this will keep the order from vacuum_room_list
        "regions": regions 
    }
}

# Send Data to Roomba
hass.services.call(
    'vacuum', 
    'send_command', 
    { 
        "command": "start",
        "entity_id": ENTITY, 
        "params": service_data 
    },
    False)



##############################################################
############# Clear all boolean states to false ##############
##            ADD YOUR STUFF TO THIS SECTION               ###
##############################################################
hass.states.set('input_boolean.roombatwopass', 'off', '')
hass.states.set('input_boolean.roombascrub', 'off', '')
hass.states.set('input_boolean.roombapowerful', 'off', '')
hass.states.set('input_boolean.roombamop', 'off', '')
hass.states.set('input_boolean.roombamopultrawater', 'off', '')
hass.states.set('input_boolean.hallway', 'off', '')
//add a reset for each input_boolean/region you created




##############################################################
##########################  LOGS  ############################
##############################################################
logger.warning('Roomba cleaning script finished with params: %s', str(service_data))
