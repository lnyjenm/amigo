from flask import Flask, render_template, request
import subprocess
import ntpath
import os
import time
import psutil
import re
from flask import jsonify
import amigo as a

app = Flask(__name__)

dkp_bat_files = {


    'DKP1611004_Website_DHCP_01': [
        '01DKP1611004_0001.DHCP.bat',
    ],

    'DKP1611015_Upgrade_DHCP(dlink auto lite)_02': [
    '02DKP1611015_0003.DHCP.bat',
    '02DKP1611015_0004.DHCP.bat',
    '02DKP1611015_0005.DHCP.bat',
    '02DKP1611015_0008.DHCP.bat',
    ],

    'DKP1611022_TimeSchedule_DHCP(dlink auto lite)_03': [
    '03DKP1611022_0004.DHCP.bat',
    '03DKP1611022_0005.DHCP.bat',
    '03DKP1611022_0007.DHCP.bat',
    '03DKP1611022_0008.DHCP.bat',
    '03DKP1611022_0009.DHCP.bat',
    ],

    'DKP1611017_Wizard_DHCPCHT_04': [
        '04DKP1611017_0001.DHCP.CHT.bat',
        '04DKP1611017_0002.DHCP.CHT.bat',
        '04DKP1611017_0003.DHCP.CHT.bat',
    ],

    'DKP1611017_Wizard_DHCP_04': [
        '04DKP1611017_0004.DHCP.bat',
    ],

    'DKP2003007_NewParentalControl_CHT_05': [
        '05DKP2003007_0001.CHT.bat',
        '05DKP2003007_0002.CHT.bat',
        '05DKP2003007_0003.CHT.bat',
        '05DKP2003007_0004.CHT.bat',
        '05DKP2003007_0013.CHT.bat',
        '05DKP2003007_0037.CHT.bat',
        '05DKP2003007_0038.CHT.bat',
        '05DKP2003007_0044.CHT.bat',
        '05DKP2003007_0045.CHT.bat',
        '05DKP2003007_0046.CHT.bat',
        '05DKP2003007_0047.CHT.bat',
        '05DKP2003007_0048.CHT.bat',
        '05DKP2003007_0049.CHT.bat',
        '05DKP2003007_0050.CHT.bat',
        '05DKP2003007_0054.CHT.bat',
    ],

    'DKP2003007_NewParentalControl_CHT(NoVM)(wireless:40.41)_05': [
        '05DKP2003007_0011.CHT(lnk).bat.lnk',
        '05DKP2003007_0020.CHT(lnk).bat.lnk',
        '05DKP2003007_0040.CHT(lnk)(wireless).bat.lnk',
        '05DKP2003007_0041.CHT(lnk)(wireless).bat.lnk',
    ],

    'DKP1611014_SystemAdmin_CHT_06': [
        '06DKP1611014_0019.CHT.bat',
        '06DKP1611014_0020.CHT.bat',
        '06DKP1611014_0021.CHT(lnk).bat.lnk',
        '06DKP1611014_0022.CHT.bat',
        '06DKP1611014_0023.CHT.bat',
        '06DKP1611014_0025.CHT.bat',
    ],

    'DKP1611014_SystemAdmin_DHCP(dlink auto lite)_06': [
    '06DKP1611014_0001.DHCP.bat',
    '06DKP1611014_0007.DHCP.bat',
    '06DKP1611014_0008.DHCP.bat',
    '06DKP1611014_0009.DHCP.bat',
    '06DKP1611014_0010.DHCP.bat',
    '06DKP1611014_0011.DHCP.bat',
    '06DKP1611014_0012.DHCP.bat',
    '06DKP1611014_0013.DHCP.bat',
    '06DKP1611014_0014.DHCP.bat',
    '06DKP1611014_0015.DHCP.bat',
    '06DKP1611014_0016.DHCP.bat',
    '06DKP1611014_0024.DHCP.bat',
    ],

    'DKP1611020_Network_DHCP_07': [
        '07DKP1611020_0003.DHCP.bat',
        '07DKP1611020_0004.DHCP.bat',
        '07DKP1611020_0005.DHCP.bat',
        '07DKP1611020_0007.DHCP(lnk).bat.lnk',
        '07DKP1611020_0008.DHCP.bat',
        '07DKP1611020_0010.DHCP(lnk).bat.lnk',
        '07DKP1611020_0011.DHCP(lnk).bat.lnk',
        '07DKP1611020_0012.DHCP(lnk).bat.lnk',
        '07DKP1611020_0033.DHCP(lnk).bat.lnk',
        '07DKP1611020_0034.DHCP(lnk).bat.lnk',
        '07DKP1611020_0036.DHCP(lnk).bat.lnk',
        '07DKP1611020_0037.DHCP(lnk).bat.lnk',
        '07DKP1611020_0038.DHCP(lnk).bat.lnk',
        '07DKP1611020_0041.DHCP.bat',
        '07DKP1611020_0042.DHCP(lnk).bat.lnk',
        '07DKP1611020_0043.DHCP(lnk).bat.lnk',
        '07DKP1611020_0044.DHCP(lnk).bat.lnk',
        '07DKP1611020_0045.DHCP(lnk).bat.lnk',
        '07DKP1611020_0046.DHCP.bat',
        '07DKP1611020_0047.DHCP(lnk).bat.lnk',
        '07DKP1611020_0048.DHCP(lnk).bat.lnk',
    ],

    'DKP1611019_Wireless_DHCP(Wireless)_08': [
        '08DKP1611019_0001.DHCP(lnk).bat.lnk',
        '08DKP1611019_0002.DHCP(lnk).bat.lnk',
        '08DKP1611019_0004.DHCP(lnk).bat.lnk',
        '08DKP1611019_0005.DHCP(lnk).bat.lnk',
        '08DKP1611019_0006.DHCP(lnk).bat.lnk',
        '08DKP1611019_0007.DHCP(lnk).bat.lnk',
        '08DKP1611019_0009.DHCP(lnk).bat.lnk',
        '08DKP1611019_0010.DHCP(lnk).bat.lnk',
        '08DKP1611019_0011.DHCP(lnk).bat.lnk',
        '08DKP1611019_0013.DHCP(lnk).bat.lnk',
        '08DKP1611019_0014.DHCP(lnk).bat.lnk',
        '08DKP1611019_0015.DHCP(lnk).bat.lnk',
        '08DKP1611019_0018.DHCP(lnk).bat.lnk',
        '08DKP1611019_0032.DHCP(lnk).bat.lnk',
        '08DKP1611019_0061.DHCP(lnk).bat.lnk',
        '08DKP1611019_0062.DHCP(lnk).bat.lnk',
        '08DKP1611019_0063.DHCP(lnk).bat.lnk',
        '08DKP1611019_0064.DHCP(lnk).bat.lnk',
        '08DKP1611019_0065.DHCP(lnk).bat.lnk',
        '08DKP1611019_0066.DHCP(lnk).bat.lnk',
        '08DKP1611019_0067.DHCP(lnk).bat.lnk',
        '08DKP1611019_0068.DHCP(lnk).bat.lnk',
        '08DKP1611019_0069.DHCP(lnk).bat.lnk',
        '08DKP1611019_0070.DHCP(lnk).bat.lnk',
        '08DKP1611019_0071.DHCP(lnk).bat.lnk',
        '08DKP1611019_0072.DHCP(lnk).bat.lnk',
        '08DKP1611019_0073.DHCP(lnk).bat.lnk',
        '08DKP1611019_0074.DHCP(lnk).bat.lnk',
        '08DKP1611019_0075.DHCP(lnk).bat.lnk',
        '08DKP1611019_0076.DHCP(lnk).bat.lnk',
        '08DKP1611019_0077.DHCP(lnk).bat.lnk',
        '08DKP1611019_0078.DHCP(lnk).bat.lnk',
        '08DKP1611019_0079.DHCP(lnk).bat.lnk',
        '08DKP1611019_0081.DHCP(lnk).bat.lnk',
        '08DKP1611019_0082.DHCP(lnk).bat.lnk',
        '08DKP1611019_0083.DHCP(lnk).bat.lnk',
        '08DKP1611019_0084.DHCP(lnk).bat.lnk',
        '08DKP1611019_0085.DHCP(lnk).bat.lnk',
        '08DKP1611019_0086.DHCP(lnk).bat.lnk',
        '08DKP1611019_0087.DHCP(lnk).bat.lnk',
        '08DKP1611019_0089.DHCP(lnk).bat.lnk',
        '08DKP1611019_0090.DHCP(lnk).bat.lnk',

    ],

    'DKP1611011_Home_DHCP(wireless:13.14)_09': [
        '09DKP1611011_0013.DHCP(lnk)(wireless).bat.lnk',
        '09DKP1611011_0014.DHCP(lnk)(wireless).bat.lnk',
        '09DKP1611011_0016.DHCP.bat',
        '09DKP1611011_0017.DHCP.bat',
        '09DKP1611011_0021.DHCP.bat',
        '09DKP1611011_0028.DHCP.bat',
        '09DKP1611011_0067.DHCP.bat',
        '09DKP1611011_0076.DHCP.bat',
        '09DKP1611011_0077.DHCP.bat',
    ],

    'DKP1611011_Home_DHCP(dlink auto lite)_09': [
    '09DKP1611011_0001.DHCP.bat',
    '09DKP1611011_0003.DHCP.bat',
    '09DKP1611011_0004.DHCP.bat',
    '09DKP1611011_0005.DHCP.bat',
    '09DKP1611011_0006.DHCP.bat',
    '09DKP1611011_0007.DHCP.bat',
    '09DKP1611011_0008.DHCP.bat',
    '09DKP1611011_0009.DHCP.bat',
    '09DKP1611011_0010.DHCP.bat',
    '09DKP1611011_0011.DHCP.bat',
    '09DKP1611011_0012.DHCP.bat',
    '09DKP1611011_0015.DHCP.bat',
    ],

    'DKP1611011_Home_PPTP.L2TP_09': [
        '09DKP1611011_0023.DHCP.PPTP.bat',
        '09DKP1611011_0024.DHCP.PPTP.bat',
        '09DKP1611011_0025.DHCP.L2TP.bat',
        '09DKP1611011_0026.DHCP.L2TP.bat',
        '09DKP1611011_0029.DHCP.PPTP.bat',
        '09DKP1611011_0030.DHCP.L2TP.bat',
        '09DKP1611011_0071.DHCP.PPTP.bat',
        '09DKP1611011_0073.DHCP.PPTP.bat',
        '09DKP1611011_0074.DHCP.L2TP.bat',
        '09DKP1611011_0078.DHCP.L2TP.bat',
    ],

    'DKP1611011_Home_CHT_09': [
        '09DKP1611011_0019.CHT.bat',
        '09DKP1611011_0020.CHT.bat',
        '09DKP1611011_0027.CHT.bat',
        '09DKP1611011_0069.CHT.bat',
        '09DKP1611011_0070.CHT.bat',
        '09DKP1611011_0072.CHT.bat',
        '09DKP1611011_0079.CHT.bat',
    ],

    'DKP1611011_Home_CHT(dlink auto lite)_09': [
    '09DKP1611011_0034.CHT.bat',
    '09DKP1611011_0036.CHT.bat',
    '09DKP1611011_0040.CHT.bat',
    '09DKP1611011_0042.CHT.bat',
    '09DKP1611011_0043.CHT.bat',
    '09DKP1611011_0045.CHT.bat',
    '09DKP1611011_0055.CHT.bat',
    '09DKP1611011_0057.CHT.bat',
    '09DKP1611011_0075.CHT.bat',
    ],

    'DKP1611018_Internet_DHCP_10': [
        '10DKP1611018_0001.DHCP.bat',
        '10DKP1611018_0002.DHCP.bat',
        '10DKP1611018_0003.DHCP.bat',
        '10DKP1611018_0004.DHCP.bat',
    ],

    'DKP1611018_Internet_PPTP.L2TP_10': [
        '10DKP1611018_0018.DHCP.PPTP.bat',
        '10DKP1611018_0025.DHCP.L2TP.bat',
        '10DKP1611018_0070.DHCP.PPTP.bat',
        '10DKP1611018_0108.DHCP.PPTP.bat',
        '10DKP1611018_0110.DHCP.PPTP.bat',
        '10DKP1611018_0111.DHCP.PPTP.bat',
        '10DKP1611018_0112.DHCP.L2TP.bat',
        '10DKP1611018_0114.DHCP.L2TP.bat',
        '10DKP1611018_0115.DHCP.L2TP.bat',
        '10DKP1611018_0117.DHCP.L2TP.bat',
    ],

    'DKP1611018_Internet_CHT_10': [
        '10DKP1611018_0005.CHT.bat',
        '10DKP1611018_0048.CHT.bat',
        '10DKP1611018_0049.CHT.bat',
        '10DKP1611018_0052.CHT.bat',
        '10DKP1611018_0053.CHT.bat',
        '10DKP1611018_0064.CHT.bat',
        '10DKP1611018_0065.CHT.bat',
        '10DKP1611018_0068.CHT.bat',
        '10DKP1611018_0069.CHT.bat',
    ],

    'DKP1611018_Internet_CHT(dlink auto lite)_10': [
    '10DKP1611018_0089.CHT.bat',
    '10DKP1611018_0090.CHT.bat',
    '10DKP1611018_0091.CHT.bat',
    '10DKP1611018_0092.CHT.bat',
    '10DKP1611018_0093.CHT.bat',
    '10DKP1611018_0094.CHT.bat',
    '10DKP1611018_0101.CHT.bat',
    '10DKP1611018_0102.CHT.bat',
    '10DKP1611018_0103.CHT.bat',
    '10DKP1611018_0104.CHT.bat',
    '10DKP1611018_0105.CHT.bat',
    '10DKP1611018_0106.CHT.bat',
    '10DKP1611018_0130.CHT.bat',
    '10DKP1611018_0132.CHT(lnk).bat.lnk',
    '10DKP1611018_0146.CHT(lnk).bat.lnk',
    ],

    'DKP1001131_BrowserCompatibilityTest_DHCP(dlink auto lite)_11': [
    '11DKP1001131_0001.DHCP.bat',
    '11DKP1001131_0004.DHCP.bat',
    '11DKP1001131_0008.DHCP.bat',
    '11DKP1001131_0009.DHCP.bat',
    '11DKP1001131_0013.DHCP.bat',
    '11DKP1001131_0014.DHCP.bat',
    ],

    'DKP1810004_WEBGUIInputFields_DHCP(dlink auto lite)_12': [
    '12DKP1810004_0001.DHCP.bat',
    '12DKP1810004_0002.DHCP.bat',
    '12DKP1810004_0003.DHCP.bat',
    '12DKP1810004_0004.DHCP.bat',
    '12DKP1810004_0005.DHCP.bat',
    '12DKP1810004_0018.DHCP.bat',
    '12DKP1810004_0019.DHCP.bat',
    '12DKP1810004_0020.DHCP.bat',
    '12DKP1810004_0021.DHCP.bat',
    '12DKP1810004_0022.DHCP.bat',
    '12DKP1810004_0023.DHCP.bat',
    '12DKP1810004_0024.DHCP.bat',
    '12DKP1810004_0025.DHCP.bat',
    '12DKP1810004_0026.DHCP.bat',
    '12DKP1810004_0027.DHCP.bat',
    '12DKP1810004_0028.DHCP.bat',
    '12DKP1810004_0029.DHCP.bat',
    '12DKP1810004_0030.DHCP.bat',
    '12DKP1810004_0031.DHCP.bat',
    '12DKP1810004_0033.DHCP.bat',
    '12DKP1810004_0034.DHCP.bat',
    '12DKP1810004_0035.DHCP.bat',
    '12DKP1810004_0036.DHCP.bat',
    '12DKP1810004_0037.DHCP.bat',
    '12DKP1810004_0038.DHCP.bat',
    '12DKP1810004_0039.DHCP.bat',
    '12DKP1810004_0040.DHCP.bat',
    '12DKP1810004_0041.DHCP.bat',
    '12DKP1810004_0045.DHCP.bat',
    '12DKP1810004_0046.DHCP.bat',
    '12DKP1810004_0047.DHCP.bat',
    '12DKP1810004_0048.DHCP.bat',
    '12DKP1810004_0049.DHCP.bat',
    '12DKP1810004_0050.DHCP.bat',
    '12DKP1810004_0051.DHCP.bat',
    '12DKP1810004_0052.DHCP.bat',
    '12DKP1810004_0053.DHCP.bat',
    '12DKP1810004_0054.DHCP.bat',
    '12DKP1810004_0055.DHCP.bat',
    '12DKP1810004_0056.DHCP.bat',
    '12DKP1810004_0057.DHCP.bat',
    '12DKP1810004_0058.DHCP.bat',
    '12DKP1810004_0059.DHCP.bat',
    '12DKP1810004_0060.DHCP.bat',
    '12DKP1810004_0061.DHCP.bat',
    '12DKP1810004_0062.DHCP.bat',
    '12DKP1810004_0063.DHCP.bat',
    '12DKP1810004_0065.DHCP.bat',
    '12DKP1810004_0066.DHCP.bat',
    '12DKP1810004_0067.DHCP.bat',
    '12DKP1810004_0068.DHCP.bat',
    '12DKP1810004_0069.DHCP.bat',
    '12DKP1810004_0070.DHCP.bat',
    '12DKP1810004_0071.DHCP.bat',
    '12DKP1810004_0072.DHCP.bat',
    ],

    'DKP1810004_WEBGUIInputFields_CHT(dlink auto lite)_12': [
    '12DKP1810004_0006.CHT.bat',
    '12DKP1810004_0007.CHT.bat',
    '12DKP1810004_0008.CHT.bat',
    '12DKP1810004_0009.CHT.bat',
    '12DKP1810004_0042.CHT.bat',
    '12DKP1810004_0064.CHT.bat',
    ],

    'DKP1810004_WEBGUIInputFields_PPTP.L2TP(dlink auto lite)_12': [
    '12DKP1810004_0010.DHCP.PPTP.bat',
    '12DKP1810004_0011.DHCP.PPTP.bat',
    '12DKP1810004_0012.DHCP.PPTP.bat',
    '12DKP1810004_0013.DHCP.PPTP.bat',
    '12DKP1810004_0014.DHCP.L2TP.bat',
    '12DKP1810004_0015.DHCP.L2TP.bat',
    '12DKP1810004_0016.DHCP.L2TP.bat',
    '12DKP1810004_0017.DHCP.L2TP.bat',
    '12DKP1810004_0043.DHCP.PPTP.bat',
    '12DKP1810004_0044.DHCP.L2TP.bat',
    ],

    'DKP1810005_SmartConnect_DHCP(dlink auto lite)_13': [
    '13DKP1810005_0001.DHCP.bat',
    '13DKP1810005_0002.DHCP.bat',
    '13DKP1810005_0003.DHCP.bat',
    '13DKP1810005_0004.DHCP.bat',
    '13DKP1810005_0005.DHCP.bat',
    ],

    'DKP1810010_BrowserCharacters_DHCP(dlink auto lite)_14': [
    '14DKP1810010_0001.DHCP.bat',
    '14DKP1810010_0002.DHCP.bat',
    '14DKP1810010_0003.DHCP.bat',
    '14DKP1810010_0004.DHCP.bat',
    '14DKP1810010_0005.DHCP.bat',
    '14DKP1810010_0006.DHCP.bat',
    '14DKP1810010_0007.DHCP.bat',
    '14DKP1810010_0008.DHCP.bat',
    '14DKP1810010_0009.DHCP.bat',
    '14DKP1810010_0010.DHCP.bat',
    '14DKP1810010_0011.DHCP.bat',
    '14DKP1810010_0021.DHCP.bat',
    '14DKP1810010_0031.DHCP.bat',
    '14DKP1810010_0032.DHCP.bat',
    ],

    'DKP1811005_WizardSetup_DHCP(dlink auto lite)_15': [
    '15DKP1811005_0001.DHCP.bat',
    '15DKP1811005_0002.DHCP.bat',
    '15DKP1811005_0003.DHCP.bat',
    '15DKP1811005_0004.DHCP.bat',
    '15DKP1811005_0005.DHCP.bat',
    '15DKP1811005_0006.DHCP.bat',
    '15DKP1811005_0007.DHCP.bat',
    '15DKP1811005_0008.DHCP.bat',
    '15DKP1811005_0009.DHCP.bat',
    '15DKP1811005_0010.DHCP.bat',
    '15DKP1811005_0031.DHCP.bat',
    '15DKP1811005_0061.DHCP.bat',
    '15DKP1811005_0121.DHCP.bat',
    ],

    'DKP1811005_WizardSetup_CHT(dlink auto lite)_15': [
    '15DKP1811005_0021.CHT.bat',
    '15DKP1811005_0022.CHT.bat',
    '15DKP1811005_0023.CHT.bat',
    '15DKP1811005_0024.CHT.bat',
    '15DKP1811005_0025.CHT.bat',
    '15DKP1811005_0026.CHT.bat',
    '15DKP1811005_0027.CHT.bat',
    '15DKP1811005_0028.CHT.bat',
    '15DKP1811005_0029.CHT.bat',
    '15DKP1811005_0030.CHT.bat',
    '15DKP1811005_0051.CHT.bat',
    '15DKP1811005_0081.CHT.bat',
    '15DKP1811005_0123.CHT.bat',
    ],

    'DKP1811005_WizardSetup_NoWAN(dlink auto lite)_15': [
    '15DKP1811005_0091.NoWAN.bat',
    '15DKP1811005_0092.NoWAN.bat',
    '15DKP1811005_0093.NoWAN.bat',
    '15DKP1811005_0094.NoWAN.bat',
    '15DKP1811005_0095.NoWAN.bat',
    '15DKP1811005_0096.NoWAN.bat',
    '15DKP1811005_0097.NoWAN.bat',
    '15DKP1811005_0098.NoWAN.bat',
    '15DKP1811005_0099.NoWAN.bat',
    '15DKP1811005_0100.NoWAN.bat',
    '15DKP1811005_0101.NoWAN.bat',
    '15DKP1811005_0111.NoWAN.bat',
    '15DKP1811005_0122.NoWAN.bat',
    ],

    'DKP1811005_WizardSetup_StaticIP(dlink auto lite)_15': [
    '15DKP1811005_0011.StaticIP.bat',
    '15DKP1811005_0012.StaticIP.bat',
    '15DKP1811005_0013.StaticIP.bat',
    '15DKP1811005_0014.StaticIP.bat',
    '15DKP1811005_0015.StaticIP.bat',
    '15DKP1811005_0016.StaticIP.bat',
    '15DKP1811005_0017.StaticIP.bat',
    '15DKP1811005_0018.StaticIP.bat',
    '15DKP1811005_0019.StaticIP.bat',
    '15DKP1811005_0020.StaticIP.bat',
    '15DKP1811005_0041.StaticIP.bat',
    '15DKP1811005_0071.StaticIP.bat',
    '15DKP1811005_0124.StaticIP.bat',
    ],

    'DKP2103013_AiParentalControl_DHCP.CHT_16': [
        '16DKP2103013_0009.DHCPCHT(lnk).bat.lnk',
    ],

    'DKP2103013_AiParentalControl_CHT_16': [
        '16DKP2103013_0011.CHT.bat',
        '16DKP2103013_0018.CHT.bat',
        '16DKP2103013_0019.CHT.bat',
    ],

    'DKP2103013_AiParentalControl_CHT(dlink auto lite)_16': [
    '16DKP2103013_0001.CHT.bat',
    '16DKP2103013_0002.CHT.bat',
    '16DKP2103013_0003.CHT.bat',
    '16DKP2103013_0004.CHT.bat',
    '16DKP2103013_0005.CHT.bat',
    '16DKP2103013_0006.CHT(lnk).bat.lnk',
    '16DKP2103013_0007.CHT.bat',
    '16DKP2103013_0010.CHT.bat',
    '16DKP2103013_0012.CHT.bat',
    '16DKP2103013_0013.CHT.bat',
    '16DKP2103013_0014.CHT.bat',
    '16DKP2103013_0015.CHT.bat',
    '16DKP2103013_0016.CHT.bat',
    '16DKP2103013_0017.CHT.bat',
    ],

    'DKP1608016_DefaultSetupWizard_DHCP.CHT_17': [
        '17DKP1608016_0027.DHCP.CHT.bat',
        '17DKP1608016_0028.DHCP.CHT.bat',
    ],

    'DKP1908011_WLANCompatibilityWPA3_CHT_20': [
        '20DKP1908011_0001.CHT(lnk).bat.lnk',
        '20DKP1908011_0002.CHT(lnk).bat.lnk',
        '20DKP1908011_0003.CHT(lnk).bat.lnk',
    ],

    'DKP2104008_SecureDNS_CHT_21': [
        '21DKP2104008_0005.CHT.bat',
    ],

    'DKP2104022_QoSEngine_DHCP_22': [
        '22DKP2104022_0001.DHCP.bat',
        '22DKP2104022_0004.DHCP.bat',
        '22DKP2104022_0006.DHCP(lnk).bat.lnk',
        '22DKP2104022_0012.DHCP.bat',
        '22DKP2104022_0015.DHCP.bat',
    ],

}

log_files = [
    'ReportExcute.bat',
]

rename_files = [
    'RenameTestReport.bat',
]



terminate_flag = False

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', dkp_list=dkp_bat_files.keys(), bat_files=[])

@app.route('/execute_bat_files', methods=['POST'])
def execute_bat_files():
    global terminate_flag
    if request.method == 'POST':
        all_bat_files = request.json.get('allBatFiles', [])
        for selected_dkp in all_bat_files: 
            dkp_number = selected_dkp.split('_')[0]
    # Check if the dkp_number exists in dkp_bat_files dictionary
            if any(dkp_number in key for key in dkp_bat_files):
        # Get the list of corresponding values (complete bat file names) from the dictionary
                complete_bat_files = [bat_file for key, bat_files in dkp_bat_files.items() if dkp_number in key for bat_file in bat_files if selected_dkp in bat_file]
                for complete_bat_file in complete_bat_files:
                    bat_path = os.path.abspath(complete_bat_file)
                    print(f"Executing batch file: {bat_path}")
                    if terminate_flag:
                        break
                    try:
                        startupinfo = subprocess.STARTUPINFO()
                        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                        process = subprocess.Popen(f'"{bat_path}"', shell=True, startupinfo=startupinfo)
                        process.wait()
                    except subprocess.CalledProcessError as e:
                        print(f"Error executing {bat_path}: {e}")
                    except Exception as e:
                        print(f"An error occurred: {e}")
        for bat_file in log_files:
            subprocess.Popen([bat_file], shell=True)
        time.sleep(3)
        response_data = "successful"
        return jsonify(response_data)


@app.route('/terminate', methods=['GET'])
def terminate():
    global terminate_flag
    terminate_flag = True

    try:
        # 终止所有cmd.exe及其子进程
        subprocess.run(["taskkill", "/F", "/T", "/IM", "cmd.exe"], shell=True)
        time.sleep(2)
        terminate_flag = False
        return 'Termination successful.'
    except Exception as e:
        return f'Termination failed: {str(e)}'


@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        log_content = get_log_content()
        if log_content == '':
            return 'Log execution failed.'
        else:
            for rename_file in rename_files:
                subprocess.Popen([rename_file], shell=True)
        return log_content
    
    


@app.route('/get_bat_files', methods=['POST'])
def get_bat_files():
    selected_dkp = request.form['dkp']
    bat_files = dkp_bat_files.get(selected_dkp, [])

    # 使用正則表達式提取想要的檔名部分
    pattern = r'DKP\d+_\d+'
    modified_bat_files_names = [re.search(pattern, ntpath.basename(bat_file)).group() for bat_file in bat_files if re.search(pattern, ntpath.basename(bat_file))]

    return {'bat_files': modified_bat_files_names}
    

@app.route('/get_log_content')
def get_log_content():
    try:
        with open(a.Result_log, 'r') as f:
            log_content = f.read()
    except FileNotFoundError:
        log_content = ''
    return log_content


if __name__ == '__main__':
    app.run(debug=True)
