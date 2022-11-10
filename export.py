import stua, json
import dotenv, os, asyncio

ACTIVE_INDEX = 0

dotenv.load_dotenv()
stua.keyMTA(os.getenv("NYCT")) #os.getenv("NYCT"))
stua.keyBUSTIME(os.getenv("BusTime"))

def branch(terminus):
    if terminus == "Ozone Park-Lefferts Blvd":
        return "OP"
    elif terminus == "Far Rockaway-Mott Av":
        return "FR"
    elif terminus == "Rockaway Park-Beach 116 St":
        return "OP"

def delay():
    global DELAYS
    global ACTIVE_INDEX
    delays_export = []
    delays = stua.alertsSubway(planned=False)
    delays_export.append(len(delays))
    if delays_export[0] == 0:
        for i in range(5):
            delays_export.append("")
        return delays_export
    else:
        grouped_delays = [delays[n:n+3] for n in range(0, len(delays), 3)]
        #print(f"ACTIVE INDEX: {ACTIVE_INDEX}")
        #print(f"LEN DELAYS: {len(grouped_delays)}")
        if ACTIVE_INDEX + 1 >= len(grouped_delays):
            ACTIVE_INDEX = 0
        else:
            ACTIVE_INDEX = ACTIVE_INDEX + 1
        DELAYS = grouped_delays[ACTIVE_INDEX]
        if len(DELAYS[0]) == 1:
            large_emblem_str = ""
            for item in DELAYS[0][0]:
                large_emblem_str += f'<img src="/static/svg/{item.lower()}.svg" style="height: 30vh; width: 100%; flex: auto;">'
            iterate_i = 0
            while iterate_i < len(DELAYS[0][1]):
                if DELAYS[0][1][iterate_i] == "[":
                    iterate_j = iterate_i
                    while iterate_j < len(DELAYS[0][1]):
                        if DELAYS[0][1][iterate_j] == "]":
                            DELAYS[0][1] = DELAYS[0][1].replace(DELAYS[0][1][iterate_i:iterate_j+1], f'<img src="/static/svg/{DELAYS[0][1][iterate_i+1:iterate_j].lower()}.svg" style="height: 15%; margin-bottom: 1%;">')
                            #print(DELAYS[0][1])
                        iterate_j += 1
                iterate_i += 1
            delays_export.append(large_emblem_str)
            delays_export.append(DELAYS[0][1])
            for i in range(3):
                delays_export.append("")
            #print(delays_export)
            return delays_export
        else:
            iterate_k = 0
            while (iterate_k < len(DELAYS)):
                #print(iterate_k)
                iterate_i = 0
                while iterate_i < len(DELAYS[iterate_k][1]):
                    #print(iterate_i)
                    if DELAYS[iterate_k][1][iterate_i] == "[":
                        iterate_j = iterate_i
                        while iterate_j < len(DELAYS[iterate_k][1]):
                            if DELAYS[iterate_k][1][iterate_j] == "]":
                                #print(DELAYS[iterate_k][1])
                                #print(DELAYS[iterate_k][1][iterate_i:iterate_j+1])
                                DELAYS[iterate_k][1] = DELAYS[iterate_k][1].replace(DELAYS[iterate_k][1][iterate_i:iterate_j+1], f'<img src="/static/svg/{DELAYS[iterate_k][1][iterate_i+1:iterate_j].lower()}.svg" style="height: 6vh; margin-bottom: 1%;">')
                            iterate_j += 1
                    iterate_i += 1
                iterate_k += 1
            for i in range(2):
                delays_export.append("")
            for item in DELAYS:
                delays_export.append(item[1])
            #print(delays_export)
            if len(delays_export) != 6:
                delays_export.append("")
            return delays_export

def subway():

    seventh_ave_crit = 4
    eighth_avenue_crit = 9
    broadway_crit = 12
    nassau_crit = 12
    lexington_avenue_crit = 12

    masterlistSUBWAY = stua.gtfsSubwayBATCHED([("137", "N", 1, seventh_ave_crit, "NONE"), ("137", "N", 2, seventh_ave_crit, "NONE"), ("137", "N", 3, seventh_ave_crit, "NONE"), ("137", "N", 4, seventh_ave_crit, "NONE"), ("137", "N", 5, seventh_ave_crit, "NONE"), #0-4
                                        ("137", "S", 1, seventh_ave_crit, "NONE"), ("137", "S", 2, seventh_ave_crit, "NONE"), ("137", "S", 3, seventh_ave_crit, "NONE"), ("137", "S", 4, seventh_ave_crit, "NONE"), ("137", "S", 5, seventh_ave_crit, "NONE"), #5-9
                                        ("A34", "N", 1, eighth_avenue_crit, "NONE"), ("A34", "N", 2, eighth_avenue_crit, "NONE"), ("A34", "N", 3, eighth_avenue_crit, "NONE"), ("A34", "N", 4, eighth_avenue_crit, "NONE"), ("A34", "N", 5, eighth_avenue_crit, "NONE"), #10-14
                                        ("A36", "S", 1, eighth_avenue_crit, "NONE"), ("A36", "S", 2, eighth_avenue_crit, "NONE"), ("A36", "S", 3, eighth_avenue_crit, "NONE"), ("A36", "S", 4, eighth_avenue_crit, "NONE"), ("A36", "S", 5, eighth_avenue_crit, "NONE"), #15-19
                                        ("R24", "N", 1, broadway_crit, "NONE"), ("R24", "N", 2, broadway_crit, "NONE"), #20-21
                                        ("R28", "S", 1, broadway_crit, "NONE"), ("R28", "S", 2, broadway_crit, "NONE"), #22-23
                                        ("M21", "N", 1, nassau_crit, "NONE"), ("M21", "N", 2, nassau_crit, "NONE"), #24-25
                                        ("640", "N", 1, lexington_avenue_crit, "NONE"), ("640", "N", 2, lexington_avenue_crit, "NONE"), ("640", "N", 3, lexington_avenue_crit, "NONE"), ("640", "N", 4, lexington_avenue_crit, "NONE")]) #26-29
    return masterlistSUBWAY

def bus():
    masterlistBUS = stua.gtfsBusBATCHED([("404969", 0, 1, 1, "NONE"), ("404969", 0, 2, 1, "NONE"), #0-1
                                        ("803147", 0, 1, 2, "NONE"), ("803147", 0, 2, 2, "NONE"), #2-3
                                        ("404238", 1, 1, 7, "SIM1"), ("404238", 1, 2, 7, "SIM1"), ("404238", 1, 1, 7, "SIM2"), ("404238", 1, 2, 7, "SIM2"), #4-7
                                        ("404225", 1, 1, 7, "X27"), ("404225", 1, 2, 7, "X27"), ("404225", 1, 1, 7, "X28"), ("404225", 1, 2, 7, "X28"), ("405065", 0, 1, 1, "M20"), ("405065", 0, 2, 1, "M20"), ("903013", 1, 1, 6, "SIM7"), ("903013", 1, 2, 6, "SIM7"), #8-15
                                        ("903013", 1, 1, 6, "SIM33"), ("903013", 1, 2, 6, "SIM33"), ("404219", 1, 1, 7, "SIM34"), ("404219", 1, 2, 7, "SIM34")]) #16-19
    return masterlistBUS

def export():

    masterlistSUBWAY = subway()
    masterlistBUS = bus()

    json_string = {
        "delay_count": "x",
        "left_side": {
            "uptown_seventh": {
                "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[0].route_id).lower()}.svg' style='height: 97%;'>",
                "time": masterlistSUBWAY[0].time,
                "terminus": masterlistSUBWAY[0].terminus
            },
            "downtown_seventh": {
                "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[5].route_id).lower()}.svg' style='height: 97%;'>",
                "time": masterlistSUBWAY[5].time,
                "terminus": masterlistSUBWAY[5].terminus
            },
            "uptown_eighth": {
                "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[10].route_id).lower()}.svg' style='height: 97%;'>",
                "time": masterlistSUBWAY[10].time,
                "terminus": masterlistSUBWAY[10].terminus
            },
            "downtown_eighth": {
                "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[15].route_id).lower()}.svg' style='height: 97%;'>",
                "time": masterlistSUBWAY[15].time,
                "terminus": masterlistSUBWAY[15].terminus
            },
            "uptown_broadway": {
                "large": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[20].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[20].time,
                    "terminus": masterlistSUBWAY[20].terminus
                },
                "small": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[21].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[21].time,
                    "terminus": branch(masterlistSUBWAY[21].terminus)
                }
            
            }
        },
        "right_side_standard": {
            "uptown_seventh": {
                "one": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[1].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[1].time,
                    "branch": branch(masterlistSUBWAY[1].terminus)
                },
                "two": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[2].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[2].time,
                    "branch": branch(masterlistSUBWAY[2].terminus)
                },
                "three": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[3].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[3].time,
                    "branch": branch(masterlistSUBWAY[3].terminus)
                },
                "four": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[4].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[4].time,
                    "branch": branch(masterlistSUBWAY[4].terminus)
                }
            },
            "downtown_seventh": {
                "one": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[6].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[6].time,
                    "branch": branch(masterlistSUBWAY[6].terminus)
                },
                "two": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[7].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[7].time,
                    "branch": branch(masterlistSUBWAY[7].terminus)
                },
                "three": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[8].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[8].time,
                    "branch": branch(masterlistSUBWAY[8].terminus)
                },
                "four": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[9].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[9].time,
                    "branch": branch(masterlistSUBWAY[9].terminus)
                }
            },
            "uptown_eighth": {
                "one": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[11].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[11].time,
                    "branch": branch(masterlistSUBWAY[11].terminus)
                },
                "two": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[12].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[12].time,
                    "branch": branch(masterlistSUBWAY[12].terminus)
                },
                "three": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[13].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[13].time,
                    "branch": branch(masterlistSUBWAY[13].terminus)
                },
                "four": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[14].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[14].time,
                    "branch": branch(masterlistSUBWAY[14].terminus)
                }
            },
            "downtown_eighth": {
                "one": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[16].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[16].time,
                    "branch": branch(masterlistSUBWAY[16].terminus)
                },
                "two": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[17].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[17].time,
                    "branch": branch(masterlistSUBWAY[17].terminus)
                },
                "three": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[18].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[18].time,
                    "branch": branch(masterlistSUBWAY[18].terminus)
                },
                "four": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[19].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[19].time,
                    "branch": branch(masterlistSUBWAY[19].terminus)
                }
            },
            "downtown_broadway": {
                "large": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[22].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[22].time,
                },
                "small": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[23].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[23].time,
                    "branch": branch(masterlistSUBWAY[23].terminus)
                }
            }
        },
        "right_side_onedelay": {
            "emblem": delay()[1],
            "delay": delay()[2]
        },
        "right_side_multipledelay": {
            "one": delay()[3],
            "two": delay()[4],
            "three": delay()[5]
        },
        "bottom_side": {
            "uptown_nassau": {
                "one": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[24].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[24].time,
                    "branch": branch(masterlistSUBWAY[24].terminus)
                },
                "two": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[25].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[25].time,
                    "branch": branch(masterlistSUBWAY[25].terminus)
                }
            },
            "uptown_lex": {
                "one": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[26].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[26].time,
                    "branch": branch(masterlistSUBWAY[26].terminus)
                },
                "two": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[27].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[27].time,
                    "branch": branch(masterlistSUBWAY[27].terminus)
                },
                "three": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[28].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[28].time,
                    "branch": branch(masterlistSUBWAY[28].terminus)
                },
                "four": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[29].route_id).lower()}.svg' style='height: 97%;'>",
                    "time": masterlistSUBWAY[29].time,
                    "branch": branch(masterlistSUBWAY[29].terminus)
                }
            },
            "bus": {
                "one": {
                    "route": masterlistBUS[0].route_id,
                    "time1": masterlistBUS[0].time,
                    "time2": masterlistBUS[1].time
                },
                "two": {
                    "route": masterlistBUS[2].route_id,
                    "time1": masterlistBUS[2].time,
                    "time2": masterlistBUS[3].time
                },
                "three": {
                    "route": "SIM1",
                    "time1": masterlistBUS[4].time,
                    "time2": masterlistBUS[5].time
                },
                "four": {
                    "route": "SIM2",
                    "time1": masterlistBUS[6].time,
                    "time2": masterlistBUS[7].time
                },
                "five": {
                    "route": "X27",
                    "time1": masterlistBUS[8].time,
                    "time2": masterlistBUS[9].time
                },
                "six": {
                    "route": "X28",
                    "time1": masterlistBUS[10].time,
                    "time2": masterlistBUS[11].time
                },
                "seven": {
                    "route": "M20",
                    "time1": masterlistBUS[12].time,
                    "time2": masterlistBUS[13].time
                },
                "eight": {
                    "route": "SIM7",
                    "time1": masterlistBUS[14].time,
                    "time2": masterlistBUS[15].time
                },
                "nine": {
                    "route": "SIM33",
                    "time1": masterlistBUS[16].time,
                    "time2": masterlistBUS[17].time
                },
                "ten": {
                    "route": "SIM34",
                    "time1": masterlistBUS[18].time,
                    "time2": masterlistBUS[19].time
                }
            }
        }
    }

    return json.dumps(json_string)   

print(export())
#delay()
#delay()
