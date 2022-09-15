# Enigma Template Code for CNU Information Security 2022
# Resources from https://www.cryptomuseum.com/crypto/enigma

# This Enigma code implements Enigma I, which is utilized by 
# Wehrmacht and Luftwaffe, Nazi Germany. 
# This version of Enigma does not contain wheel settings, skipped for
# adjusting difficulty of the assignment.

from copy import deepcopy
from ctypes import ArgumentError

# Enigma Components
ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

WHEELS = {
    "I" : {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "turn": 16
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "turn": 4
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "turn": 21
    }
}
#반사체
UKW = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

# Enigma Settings
SETTINGS = {
    "UKW": None,
    "WHEELS": [],
    "WHEEL_POS": [],
    "ETW": ETW,
    "PLUGBOARD": []
}

def apply_settings(ukw, wheel, wheel_pos, plugboard):
    #UKW에 있는 값인지 확인 후 설정
    if not ukw in UKW:
        raise ArgumentError(f"UKW {ukw} does not exist!")
    SETTINGS["UKW"] = UKW[ukw]
    #휠 설정
    wheels = wheel.split(' ')
    for wh in wheels:
        if not wh in WHEELS:
            raise ArgumentError(f"WHEEL {wh} does not exist!")
        SETTINGS["WHEELS"].append(WHEELS[wh])
    #휠 위치 설정
    wheel_poses = wheel_pos.split(' ')
    for wp in wheel_poses:
        if not wp in ETW:
            raise ArgumentError(f"WHEEL position must be in A-Z!")
        SETTINGS["WHEEL_POS"].append(ord(wp) - ord('A'))
    if len(SETTINGS["WHEELS"]) != len(SETTINGS["WHEEL_POS"]):
        raise ArgumentError(f"WHEEL number must be match WHEEL_POS")
    #플래그 보드들 설정
    plugboard_setup = plugboard.split(' ')
    for ps in plugboard_setup:
        if not len(ps) == 2 or not ps.isupper():
            raise ArgumentError(f"Each plugboard setting must be sized in 2 and caplitalized; {ps} is invalid")
        SETTINGS["PLUGBOARD"].append(ps)

# Enigma Logics Start

# Plugboard
#설정된 플러그 보드들에 해당하는지 확인 후 변경
def pass_plugboard(input):
    for plug in SETTINGS["PLUGBOARD"]:
        if str.startswith(plug, input):
            return plug[1]
        elif str.endswith(plug, input):
            return plug[0]

    return input

# ETW
#ETW에 설정된 값으로 치환
def pass_etw(input):
    return SETTINGS["ETW"][ord(input) - ord('A')]

# Wheels
def pass_wheels(input, reverse = False):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order
    wheel = SETTINGS["WHEELS"]
    wheel_Pos = SETTINGS["WHEEL_POS"]
    # 반사체를 갔다가 돌아올 때
    if reverse:
        # 마지막 휠부터 하기 위해 인덱스 거꾸로
        for i in range(len(wheel)-1,-1,-1):
            #휠 연산
            input=ETW[(wheel[i]["wire"].find(ETW[(ETW.find(input)+wheel_Pos[i])%26])-wheel_Pos[i]+26)%26]
    else:
        for i in range(len(wheel)):
            #휠 연산
            input=ETW[(ETW.find(wheel[i]["wire"][(ETW.find(input)+wheel_Pos[i])%26])-wheel_Pos[i]+26)%26]
    return input

# UKW
def pass_ukw(input):
    return SETTINGS["UKW"][ord(input) - ord('A')]

# Wheel Rotation
def rotate_wheels():
    # Implement Wheel Rotation Logics
    wheel = SETTINGS["WHEELS"]
    wheel_Pos =  SETTINGS["WHEEL_POS"]
    #첫번째 휠의 위치가 노치일때 두번째 휠 회전
    if wheel_Pos[0]==wheel[0]["turn"]:
        # 두번째 휠의 위치가 노치일때 세번째 휠 회전
        if wheel_Pos[1]==wheel[1]["turn"]:
            wheel_Pos[2]+=1
        wheel_Pos[1]+=1
    wheel_Pos[0]+=1
    pass

# Enigma Exec Start
#평문 입력
plaintext = input("Plaintext to Encode: ")
#UKW 선택
ukw_select = input("Set Reflector (A, B, C): ")
#휠 선택 오른쪽에서 왼쪽(첫번째 휠부터 선택)
wheel_select = input("Set Wheel Sequence R->L (I, II, III): ")
wheel_pos_select = input("Set Wheel Position R->L (A~Z): ")
#플래그 보드 설정, ex)AB CD IH
plugboard_setup = input("Plugboard Setup: ")
#셋팅
apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)

for ch in plaintext:
    rotate_wheels()

    encoded_ch = ch
    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse = True)
    encoded_ch = pass_plugboard(encoded_ch)

    print(encoded_ch, end='')
