#!python
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
from datetime import date 
import csv
import js
import json
import asyncio
import io
from io import StringIO
from js import Blob, document, window, dfd
from pyodide.ffi import create_proxy, to_js
import datetime
import os


async def DATA_CLEANER(FILE):
   
    DATA = [row for row in csv.reader(FILE.splitlines(), delimiter=',')]
    df = pd.DataFrame(list(DATA)[1:], columns = list(DATA)[0:1][0])
    print(list(DATA)[0:1][0])
    #VARIABLES ATTACHED WITH THE STRING OF A CLUMN VARIABLE FROM THE RANKING DETAIL FILE
    KW = 'Keyword'
    VSBY = 'Visibility'
    SE = "SE"
    NOTE = "NOTE"
    RP = 'Ranking page(s)'
    _URL_ = "URL"
    URL_RANK =  "Google URL Found"
    GMHUF = "Google Mobile HOU URL Found"
    GHUF=  "Google HOU URL Found"
    BUUF =  "Bing US URL Found"
    YUF = "Yahoo! URL Found"
    URL_FOUND = "Google URL Found"
    LP_1= "Local Pack (1)"
    GOD_SERP = "Google HOU SERP Features"
    GOM_SERP = "Google Mobile HOU SERP Features"
    BNG_SERP = "Bing US SERP Features"
    YAH_SERP =  "Yahoo! SERP Features"
    NEW_GOD_SERP = "Google Houston SERP Features"
    NEW_GOM_SERP = "Houston MOB SERP Features"  
    GMH_SERP = 'Google Mob HOU SERP Features'
    GHOU_SERP = 'Google Houston SERP Features'
    ARRAY_GOOGLE = []
    ARRAY_GOOGLE_MOBILE = []
    ARRAY_BING = []
    ARRAY_YAHOO = []
    

    def check_word_in_list(word, string_list): 
        for string in string_list:
            if word in string:
                return True
        return False

    def COLUMN_NAME():
        for x in range(len(list(DATA)[0:1][0])):
            if "Google" in list(DATA)[0:1][0][x]:
                if "mobile" in list(DATA)[0:1][0][x] or "Mobile" in list(DATA)[0:1][0][x] or "MOB" in list(DATA)[0:1][0][x] or "Mob" in list(DATA)[0:1][0][x] or "mob" in list(DATA)[0:1][0][x]:
                    if "previous" in list(DATA)[0:1][0][x] or "Previous" in list(DATA)[0:1][0][x]:
                        global GOOGLE_MOBILE_PREVIOUS
                        GOOGLE_MOBILE_PREVIOUS = list(DATA)[0:1][0][x]
                    else:
                        if "Difference" in list(DATA)[0:1][0][x] or "difference" in list(DATA)[0:1][0][x]:
                            global GOOGLE_MOBILE_DIFFERENCE
                            GOOGLE_MOBILE_DIFFERENCE = list(DATA)[0:1][0][x]

                        else:
                            if "Rank" in list(DATA)[0:1][0][x]:
                                global GOOGLE_MOBILE_RANK 
                                GOOGLE_MOBILE_RANK = list(DATA)[0:1][0][x]

                            else:
                                if "URL" in list(DATA)[0:1][0][x]:
                                    global GOOGLE_MOBILE_URL
                                    GOOGLE_MOBILE_URL = list(DATA)[0:1][0][x]
                                else:
                                    if "SERP" in list(DATA)[0:1][0][x]:
                                        global GOOGLE_MOBILE_SERP
                                        GOOGLE_MOBILE_SERP = list(DATA)[0:1][0][x]
                                    else:
                                        pass
                                
                else:
                    if "previous" in list(DATA)[0:1][0][x] or "Previous" in list(DATA)[0:1][0][x]:
                        global GOOGLE_PREVIOUS
                        GOOGLE_PREVIOUS = list(DATA)[0:1][0][x]

                    else:
                        if "Difference" in list(DATA)[0:1][0][x] or "difference" in list(DATA)[0:1][0][x]:
                            global GOOGLE_DIFFERENCE
                            GOOGLE_DIFFERENCE = list(DATA)[0:1][0][x]

                        else:
                            if "Rank" in list(DATA)[0:1][0][x]:
                                global GOOGLE_RANK 
                                GOOGLE_RANK = list(DATA)[0:1][0][x]

                            else:
                                if "URL" in list(DATA)[0:1][0][x]:
                                    global GOOGLE_URL
                                    GOOGLE_URL = list(DATA)[0:1][0][x]
                                else:
                                    if "SERP" in list(DATA)[0:1][0][x]:
                                        global GOOGLE_SERP
                                        GOOGLE_SERP = list(DATA)[0:1][0][x]
                                    else:
                                        pass
            else:
                if "Houston MOB" in list(DATA)[0:1][0][x]:
                    if "previous" in list(DATA)[0:1][0][x] or "Previous" in list(DATA)[0:1][0][x]:
                        GOOGLE_MOBILE_PREVIOUS = list(DATA)[0:1][0][x]
                    else:
                        if "Difference" in list(DATA)[0:1][0][x] or "difference" in list(DATA)[0:1][0][x]:
                            GOOGLE_MOBILE_DIFFERENCE = list(DATA)[0:1][0][x]
                        else:
                            if "Rank" in list(DATA)[0:1][0][x]:
                                GOOGLE_MOBILE_RANK = list(DATA)[0:1][0][x]
                            else:
                                if "URL" in list(DATA)[0:1][0][x]:
                                    GOOGLE_MOBILE_URL = list(DATA)[0:1][0][x]
                                else:
                                    if "SERP" in list(DATA)[0:1][0][x]:
                                        GOOGLE_MOBILE_SERP = list(DATA)[0:1][0][x]
                                    else:
                                        pass
                else:
                    if "Yahoo" in list(DATA)[0:1][0][x] or "yahoo" in list(DATA)[0:1][0][x]:
                        if "previous" in list(DATA)[0:1][0][x] or "Previous" in list(DATA)[0:1][0][x]:
                            global YAHOO_PREVIOUS
                            YAHOO_PREVIOUS = list(DATA)[0:1][0][x]

                        else:
                            if "Difference" in list(DATA)[0:1][0][x] or "difference" in list(DATA)[0:1][0][x]:
                                global YAHOO_DIFFERENCE
                                YAHOO_DIFFERENCE = list(DATA)[0:1][0][x]

                            else:
                                if "Rank" in list(DATA)[0:1][0][x]:
                                    global YAHOO_RANK
                                    YAHOO_RANK = list(DATA)[0:1][0][x]

                                else:
                                    if "URL" in list(DATA)[0:1][0][x]:
                                        global YAHOO_URL
                                        YAHOO_URL = list(DATA)[0:1][0][x]
                                    else:
                                        if "SERP" in list(DATA)[0:1][0][x]:
                                            global YAHOO_SERP
                                            YAHOO_SERP = list(DATA)[0:1][0][x]
                                        else:
                                            pass
                                        
                    else:
                        if "Bing" in list(DATA)[0:1][0][x] or "bing" in list(DATA)[0:1][0][x]:
                            if "previous" in list(DATA)[0:1][0][x] or "Previous" in list(DATA)[0:1][0][x]:
                                global BING_PREVIOUS
                                BING_PREVIOUS = list(DATA)[0:1][0][x]

                            else:
                                if "Difference" in list(DATA)[0:1][0][x] or "difference" in list(DATA)[0:1][0][x]:
                                    global BING_DIFFERENCE
                                    BING_DIFFERENCE = list(DATA)[0:1][0][x]

                                else:
                                    if "Rank" in list(DATA)[0:1][0][x]:
                                        global BING_RANK
                                        BING_RANK = list(DATA)[0:1][0][x]

                                    else:
                                        if "URL" in list(DATA)[0:1][0][x]:
                                            global BING_URL
                                            BING_URL = list(DATA)[0:1][0][x]
                                        else:
                                            if "SERP" in list(DATA)[0:1][0][x]:
                                                global BING_SERP
                                                BING_SERP = list(DATA)[0:1][0][x]
                                            else:
                                                pass
                                            
                        else:
                            pass
        
        return GOOGLE_MOBILE_PREVIOUS, GOOGLE_MOBILE_DIFFERENCE, GOOGLE_MOBILE_RANK, GOOGLE_PREVIOUS, GOOGLE_DIFFERENCE, GOOGLE_RANK, YAHOO_PREVIOUS, YAHOO_DIFFERENCE, YAHOO_RANK, BING_RANK, BING_DIFFERENCE, BING_PREVIOUS;    

          
    COLUMN_NAME()
 
   



    GOD_F = {KW: df[KW], GOOGLE_URL: df[GOOGLE_URL], GOOGLE_RANK: df[GOOGLE_RANK], GOOGLE_PREVIOUS: df[GOOGLE_PREVIOUS], GOOGLE_DIFFERENCE: df[GOOGLE_DIFFERENCE]}
    GOM_F = {KW: df[KW],GOOGLE_MOBILE_URL: df[GOOGLE_MOBILE_URL], GOOGLE_MOBILE_PREVIOUS: df[GOOGLE_MOBILE_PREVIOUS], GOOGLE_MOBILE_RANK: df[GOOGLE_MOBILE_RANK], GOOGLE_MOBILE_DIFFERENCE: df[GOOGLE_MOBILE_DIFFERENCE]}            
    BNG_F = {KW: df[KW],BING_URL: df[BING_URL], BING_RANK: df[BING_RANK], BING_DIFFERENCE: df[BING_DIFFERENCE], BING_PREVIOUS: df[BING_PREVIOUS]}
    YAH_F = {KW: df[KW],YAHOO_URL: df[YAHOO_URL], YAHOO_RANK: df[YAHOO_RANK],YAHOO_PREVIOUS: df[YAHOO_PREVIOUS], YAHOO_DIFFERENCE: df[YAHOO_DIFFERENCE]}
    
    GOD_H = pd.DataFrame(GOD_F)

    GOM_H = pd.DataFrame(GOM_F)

    BNG_H = pd.DataFrame(BNG_F)

    YAH_H = pd.DataFrame(YAH_F)
    
   
    GOD_CLEAN_1 = GOD_H[GOD_H[GOOGLE_DIFFERENCE] != "Stays out"]   
    GOM_CLEAN_1 = GOM_H[GOM_H[GOOGLE_MOBILE_DIFFERENCE] != "Stays out"]    
    BNG_CLEAN_1 = BNG_H[BNG_H[BING_DIFFERENCE] != "Stays out"]
    YAH_CLEAN_1 = YAH_H[YAH_H[YAHOO_DIFFERENCE] != "Stays out"]
    GOD_CLEAN_2 = GOD_CLEAN_1[GOD_CLEAN_1[GOOGLE_DIFFERENCE] != "Dropped"]
    GOM_CLEAN_2 = GOM_CLEAN_1[GOM_CLEAN_1[GOOGLE_MOBILE_DIFFERENCE] != "Dropped"]   
    BNG_CLEAN_2 = BNG_CLEAN_1[BNG_CLEAN_1[BING_DIFFERENCE] != "Dropped"]
    YAH_CLEAN_2 = YAH_CLEAN_1[YAH_CLEAN_1[YAHOO_DIFFERENCE] != "Dropped"]
    ArrayGOOGLE_RANK = pd.array(GOD_CLEAN_2[GOOGLE_RANK])
    ArrayGOOGLE_DIFFERENCE = pd.array(GOD_CLEAN_2[GOOGLE_DIFFERENCE])
    ArrayGOOGLE_MOBILE_RANK = pd.array(GOM_CLEAN_2[GOOGLE_MOBILE_RANK])
    ArrayGOOGLE_MOBILE_DIFFERENCE = pd.array(GOM_CLEAN_2[GOOGLE_MOBILE_DIFFERENCE])           
           

  
    def NEG_Y_FUNCTION(X, Y, ARRAY):
        Y = int(Y)
        X = int(X)
        z =  Y + X 
        ARRAY.append(z)
        
    def X_GRT_Y_LOGIC_FUNCTION(X, Y, ARRAY):
        Y = int(Y)
        X = int(X)

        if X > Y or X == Y:
            z = X + Y
            ARRAY.append(z)
        else:
            Y = str(Y)
            if "-" in Y:
                Y = int(Y)
                ARRAY.append(Y)
            else:
                z = X + int(Y)
                ARRAY.append(z)      

                
    def Y_FUNCTION(X, Y, ARRAY):
        Y = int(Y)

        if Y >= 0:
            X_GRT_Y_LOGIC_FUNCTION(X, Y, ARRAY)
            
        else:
            NEG_Y_FUNCTION(X, Y, ARRAY)

            
    def LOGIC_X_Y_STR(X, Y, RA):
        if "+" in str(Y):
            POS_Y = int(str(Y)[1])
            X_GRT_Y_LOGIC_FUNCTION(X, POS_Y, RA)
        else:
            POS_X = int(X)
            Y_FUNCTION(POS_X, Y, RA)
            

            
    def STANDARD_XY_FUNCTION(AR, AD, RA):
        if "(" in str(AR) or str(AD):
            if "(" in str(AD):
                NEW_AD = str(AD)
                RANK_Y = int(NEW_AD[0])
                if "(" in str(AR):
                    NEW_AR = str(AR)
                    RANK_X = int(NEW_AR[0])
                    Y_FUNCTION(RANK_X, RANK_Y, RA)
                else:
                    Y_FUNCTION(int(AR), RANK_Y, RA)
            else:
                if "(" in str(AR):
                    NEW_AR = str(AR)
                    RANK_X = int(NEW_AR[0])
                    y = int(AD)
                    Y_FUNCTION(RANK_X, y, RA)
                else:
                    y = int(AD)
                    Y_FUNCTION(AR, y, RA)
        else:
            DIF_Y = int(AD)
            LOGIC_X_Y_STR(AR, DIF_Y, RA)
            


    def REMOVE_BARS_FUNCTION(ARRAY_R, X, R_A):
        
        if "(" in str(ARRAY_R[X]):
            NEW_AR = str(ARRAY_R[X])
            RANK_X = NEW_AR[0]
            R_A.append(RANK_X)
            
        else:
            R_A.append(ARRAY_R[X])

    def BAR_RMV_ARRAY_OUTPUT (ARRAY_RANK):
        RankArray = []
        
        
        for x in range(len(ARRAY_RANK)):
            REMOVE_BARS_FUNCTION(ARRAY_RANK, x, RankArray)
        return RankArray

    def NOT_A_FLOAT_FUNCTION(AR, AD, RA):
        if len(AD) > 3 or pd.isna(AD) == True or str(AD) == '':
            if "(" in str(AD):
                NEW_AD = str(AD)
                RANK_Y = int(NEW_AD[0])
                STANDARD_XY_FUNCTION(AR, RANK_Y, RA)
            else:
                if "N" in str(AR):
                    RA.append(30)
                else:
                    RA.append(30)
            
        else:
            if "N" in str(AR):
                RA.append(30)
            else:
                STANDARD_XY_FUNCTION(AR, AD, RA)

    #def DEL_STR (AR, AD, RA):
        #if len(NEW_AR) > 3 == True: 
            
            


    def ITS_A_FLOAT_FUNCTION(AR, AD, RA): 
        if pd.isna(AD) == True:
            if "N" in str(AR):
                RA.append(30)
            else:
                RA.append(30)
        else:
            STANDARD_XY_FUNCTION(AR, AD, RA)
            




    ##ARRAY_OUTPUT IS THE CONCLUSION LOGIC FORM FUNCTION INTEGRATED FROM OF ALL ABOVE FUNCTIONS 
    ##ARRAY_DIF TAKES IN THE ARRAY HOLDING THE DIFFERENCE COLUMN VARIABLES
    ##ARRAY_RANK TAKES IN THE ARRAY HOLDING THE RANK COLUMN VARIABLES
    ##DCDF TAKES IN THE WHOLE DATAFRAME OF THE DC VARIABLE


    def ARRAY_OUTPUT (ARRAY_DIF, ARRAY_RANK):
        
        ## CREATES AN BLANK ARRAY TO APPEND NEW VARIABLES TO
        RankArray = []
        
        ##A FOR LOOP IS CREATED TO GO OVER ALL VARIABLES IN THE RANGE OF THE LENGTH 
        ##OF THE DIFFERENCE COLUMNS VARIABLE (ARRAY_DIF)
        
        for x in range(len(ARRAY_DIF)):
            
            ##IF THE ARRAYS VARIABLE AT THE INDEX POSITION IS A FLOAT THEN THIS WILL EXECUTE A FUNCTION
            #CALLED ITS_A_FLOAT_FUNCTION
            if isinstance(ARRAY_DIF[x], float) == True:
                ITS_A_FLOAT_FUNCTION(ARRAY_RANK[x], ARRAY_DIF[x], RankArray)
                
            ##IF THE ARRAYS VARIABLE AT THE INDEX POSITION IS 
            #NOT A FLOAT THEN THIS WILL EXECUTE A FUNCTION
            #CALLED NOT_A_FLOAT_FUNCTION


            else:
                NOT_A_FLOAT_FUNCTION(ARRAY_RANK[x], ARRAY_DIF[x], RankArray)

        
        ##RETURNS THE DATA STORED IN THE VARIABLE SO IT CAN BE STORED ELSEWHERE
        ##FOR FURTHER DATA MANIPLUATION
        return RankArray
            
    def ENTER_NEG_Y_FUNCTION(X, Y, ARRAY):
        Y = -Y
        
        ARRAY.append(Y)

    def ENTER_X_GRT_Y_LOGIC_FUNCTION(X, Y, ARRAY):
        ARRAY.append(Y)
        
        
    def ENTER_Y_FUNCTION(X, Y, ARRAY):
        Y = int(Y)
        if Y >= 0:
            ENTER_X_GRT_Y_LOGIC_FUNCTION(X, Y, ARRAY)
            
        else:
            ENTER_NEG_Y_FUNCTION(X, Y, ARRAY)
        
    def ENTER_LOGIC_X_Y_STR(ARRAY, Y, RA):
        Y = str(Y)
        if "+" in str(Y):
            POS_Y = int(str(Y)[1])
            ENTER_X_GRT_Y_LOGIC_FUNCTION(ARRAY, POS_Y, RA)
        else:
            if "N" in ARRAY:
                RA.append(30)
            else:
                POS_X = int(ARRAY)
                ENTER_Y_FUNCTION(POS_X, Y, RA)
            
            
            
    def ENTER_STANDARD_XY_FUNCTION(AR, AD, RA):
        if "(" in str(AR) or str(AD):
            if "(" in str(AD):
                NEW_AD = str(AD)
                RANK_Y = int(NEW_AD[0])
                if "(" in str(AR):
                    NEW_AR = str(AR)
                    RANK_X = int(NEW_AR[0])
                    ENTER_Y_FUNCTION(RANK_X, RANK_Y, RA)
                else:
                    ENTER_Y_FUNCTION(int(AR), RANK_Y, RA)
            else:
                if "(" in str(AR):
                    NEW_AR = str(AR)
                    RANK_X = int(NEW_AR[0])
                    y = int(AD)
                    ENTER_Y_FUNCTION(RANK_X, y, RA)
                else:
                    ENTER_Y_FUNCTION(AR, AD, RA)
        else:
            DIF_Y = int(AD)
            ENTER_LOGIC_X_Y_STR(AR, DIF_Y, RA)
    #####
    def ENTER_NOT_A_FLOAT_FUNCTION(AR, AD, RA):
        if len(AD) > 3 or pd.isna(AD) == True or str(AD) == '':
            if "(" in str(AR) or "(" in str(AD):
                ENTER_STANDARD_XY_FUNCTION(AR, AD, RA)
            else:
                if "N" in str(AR):
                    RA.append(30)
                else:
                    if str(AD) == '':
                        RA.append(30)
                    else:
                        RA.append(30-int(AR))
        else:
            ENTER_STANDARD_XY_FUNCTION(AR, AD, RA)
            
    def ENTER_ITS_A_FLOAT_FUNCTION(AR, AD, RA): 
        if pd.isna(AD) == True:
            if "N" in str(AR):
                RA.append(30)
            else:
                RA.append(30-int(AR))
        else:
            ENTER_STANDARD_XY_FUNCTION(AR, AD, RA)




    def CHANGE_ENTER_FUNCTION(AR, AD, AP):
        RankArray = []
        
        for x in range(len(AD)):
            if isinstance(AD[x], float) == True:
                if pd.isna(AD[x]) == True or "E" in str(AD[x]):
                    if len(str(AR[x])) > 3 or pd.isna(AR[x]) == True:
                        if "E" in str(AD[x]):
                            ARX = int(AR[x])
                            RankArray.append(30-AR[x])
                        else:
                            ENTER_ITS_A_FLOAT_FUNCTION(AR[x], AD[x], RankArray)
                    else:
                        ENTER_ITS_A_FLOAT_FUNCTION(AR[x], AD[x], RankArray)

                else:
                    ENTER_ITS_A_FLOAT_FUNCTION(AR[x], AD[x], RankArray)
            
            else:
                if len(AD[x]) > 3 or pd.isna(AD[x]) == True or "E" in str(AD[x]):
                    if len(str(AR[x])) > 3 or pd.isna(AR[x]) == True or "E" in str(AD[x]):
                        if "E" in str(AD[x]):
                            ARX = int(AR[x])
                            RankArray.append(30-ARX)
                        else:
                            ENTER_NOT_A_FLOAT_FUNCTION(AR[x], AD[x], RankArray)
                    else:
                        ENTER_NOT_A_FLOAT_FUNCTION(AR[x], AD[x], RankArray)

                else:
                    ENTER_NOT_A_FLOAT_FUNCTION(AR[x], AD[x], RankArray)
            
        return RankArray
            

    def NOTE_Y_FUNCTION(X, Y, ARRAY): 
        X = int(X)
        Y = int(Y)
        if X < Y:
            ARRAY.append("UP")
            
        if X > Y:
            ARRAY.append("DOWN")
        
        if X == Y:
            ARRAY.append("EQ")


    def CHANGE_NOTE_FUNCTION(AR, AP):
        RankArray = []
        
        for x in range(len(AP)):
            
            if AP[x] == 30 or len(AR[x]) > 3 or len(str(AP[x])) > 3:
                RankArray.append('NEW')
            else:
                ARX = int(AR[x])
                NOTE_Y_FUNCTION(ARX, AP[x], RankArray)
            
        return RankArray


    Array_GOOGLE_RANK = BAR_RMV_ARRAY_OUTPUT(ArrayGOOGLE_RANK)

    GPD = ARRAY_OUTPUT(ArrayGOOGLE_DIFFERENCE, Array_GOOGLE_RANK)

    Array_GOOGLE_MOBILE_RANK = BAR_RMV_ARRAY_OUTPUT(ArrayGOOGLE_MOBILE_RANK)
    GOOGLE_MOBILE_PREVIOUSDF = ARRAY_OUTPUT(ArrayGOOGLE_MOBILE_DIFFERENCE, Array_GOOGLE_MOBILE_RANK)
    ArrayBING_DIFFERENCE = pd.array(BNG_CLEAN_2[BING_DIFFERENCE])
    ArrayBING_RANK = pd.array(BNG_CLEAN_2[BING_RANK])
    Array_BING_RANK = BAR_RMV_ARRAY_OUTPUT(ArrayBING_RANK)
    Array_BING_DIFFERENCE = BAR_RMV_ARRAY_OUTPUT(ArrayBING_DIFFERENCE)

    BING_DIFFERENCEF = ARRAY_OUTPUT(Array_BING_DIFFERENCE, Array_BING_RANK)

    ArrayYAHOO_DIFFERENCE = pd.array(YAH_CLEAN_2[YAHOO_DIFFERENCE])

    ArrayYAHOO_RANK = pd.array(YAH_CLEAN_2[YAHOO_RANK])

    Array_YAHOO_RANK = BAR_RMV_ARRAY_OUTPUT(ArrayYAHOO_RANK)

    YAHDF = ARRAY_OUTPUT(ArrayYAHOO_DIFFERENCE, Array_YAHOO_RANK)

    GODIF_NEW = CHANGE_ENTER_FUNCTION(Array_GOOGLE_RANK, ArrayGOOGLE_DIFFERENCE, GPD)
    GOMDIF_NEW = CHANGE_ENTER_FUNCTION(Array_GOOGLE_MOBILE_RANK, ArrayGOOGLE_MOBILE_DIFFERENCE, GOOGLE_MOBILE_PREVIOUSDF)
    BNGDIF_NEW = CHANGE_ENTER_FUNCTION(Array_BING_RANK, ArrayBING_DIFFERENCE, BING_DIFFERENCEF)
    YAHOO_DIFFERENCE_NEW = CHANGE_ENTER_FUNCTION(Array_YAHOO_RANK, ArrayYAHOO_DIFFERENCE, YAHDF)
    GOD_NOTE = CHANGE_NOTE_FUNCTION(Array_GOOGLE_RANK, GPD)
    GOM_NOTE = CHANGE_NOTE_FUNCTION(Array_GOOGLE_MOBILE_RANK, GOOGLE_MOBILE_PREVIOUSDF)
    BNG_NOTE = CHANGE_NOTE_FUNCTION(Array_BING_RANK, BING_DIFFERENCEF)
    YAH_NOTE = CHANGE_NOTE_FUNCTION(Array_YAHOO_RANK, YAHDF)

    
    GOD = {KW: GOD_CLEAN_2[KW],RP: GOD_CLEAN_2[GOOGLE_URL], GOOGLE_RANK: Array_GOOGLE_RANK,
            GOOGLE_PREVIOUS: GPD, GOOGLE_DIFFERENCE: GODIF_NEW, NOTE: GOD_NOTE}

    GOM = {KW: GOM_CLEAN_2[KW], RP: GOM_CLEAN_2[GOOGLE_MOBILE_URL], GOOGLE_MOBILE_RANK: Array_GOOGLE_MOBILE_RANK, 
            GOOGLE_MOBILE_PREVIOUS: GOOGLE_MOBILE_PREVIOUSDF, GOOGLE_MOBILE_DIFFERENCE: GOMDIF_NEW, NOTE: GOM_NOTE}           
        
    BNG = {KW: BNG_CLEAN_2[KW], RP: BNG_CLEAN_2[BING_URL], BING_RANK: Array_BING_RANK,
            BING_PREVIOUS: BING_DIFFERENCEF, BING_DIFFERENCE: BNGDIF_NEW, NOTE: BNG_NOTE}

    YAH = {KW: YAH_CLEAN_2[KW],RP: YAH_CLEAN_2[YAHOO_URL], YAHOO_RANK: Array_YAHOO_RANK,
            YAHOO_PREVIOUS: YAHDF, YAHOO_DIFFERENCE: YAHOO_DIFFERENCE_NEW, NOTE: YAH_NOTE}


    GOD_DF = pd.DataFrame(data=GOD)
    GOD_NEW = pd.DataFrame(data=GOD_DF[GOD_DF[GOOGLE_RANK] != "Not in top 30"])
    GOD_NEW = pd.DataFrame(data=GOD_NEW[GOD_NEW[GOOGLE_RANK] != "Not in top 50"])
    GOD_LEN = len(GOD_NEW)
    GOD_1 = pd.DataFrame(data=GOD_NEW[GOD_NEW[GOOGLE_RANK] == "1"])
    GOD_NEW_NOTE = pd.DataFrame(data=GOD_NEW[GOD_NEW[NOTE] == "NEW"])
    GOD_NOTE = len(GOD_NEW_NOTE)
    GOD_UP_NOTE = pd.DataFrame(data=GOD_NEW[GOD_NEW[NOTE] == "UP"])
    GOD_UP = len(GOD_UP_NOTE)
    GOD_DOWN_NOTE = pd.DataFrame(data=GOD_NEW[GOD_NEW[NOTE] == "DOWN"])
    GOD_DOWN = len(GOD_DOWN_NOTE)
    GOD_EQ_NOTE = pd.DataFrame(data=GOD_NEW[GOD_NEW[NOTE] == "EQ"])
    GOD_EQ = len(GOD_EQ_NOTE)
    GOD_LP_LEN = pd.DataFrame(data=df[GOOGLE_SERP])
   
    GOD_LP = len(GOD_LP_LEN)
    GOD_1_LEN = len(GOD_1)
    LP_GOD_ = []
    for x in range(len(df)):
        if LP_1 in str(GOD_LP_LEN[GOOGLE_SERP][x]):
            LP_GOD_.append(GOD_LP_LEN[GOOGLE_SERP][x])
        else:
            False       
 
 
    TOP_5GOD = []
    GOD_FIRST_PAGE = []
    GOD_TWO_PAGE = []

    LP_GOD = pd.DataFrame()
    for x in range(5):
        TOP_5GOD.append(len(GOD_NEW[GOD_NEW[GOOGLE_RANK] == str(x+1)]))

    for x in range(10):
        GOD_NEW[GOOGLE_RANK]
        GOD_FIRST = len(pd.DataFrame(data=GOD_NEW[GOD_NEW[GOOGLE_RANK] == str(x+1)]))
        GOD_FIRST_PAGE.append(GOD_FIRST)

    for x in range(20):
        GOD_TWO = len(pd.DataFrame(data=GOD_NEW[GOD_NEW[GOOGLE_RANK] == str(x+1)]))
        GOD_TWO_PAGE.append(GOD_TWO)

    GOD_5_TOP = pd.DataFrame(data=TOP_5GOD)
    GOD5_TOP = GOD_5_TOP.sum()[0]
    GOD_FIRST_PAGE_TOP = pd.DataFrame(data=GOD_FIRST_PAGE)
    GODFIRST_TOP = GOD_FIRST_PAGE_TOP.sum()[0]
    GOD_TWO_PAGE_TOP = pd.DataFrame(data=GOD_TWO_PAGE)
    GODTWO_TOP= GOD_TWO_PAGE_TOP.sum()[0]
    GOM_DF = pd.DataFrame(data=GOM)
    TOP_5GOM = []
    GOM_FIRST_PAGE = []
    GOM_TWO_PAGE = []
    LP_GOM = []
    GOM_NEW = pd.DataFrame(data=GOM_DF[GOM_DF[GOOGLE_MOBILE_RANK] != "Not in top 30"])
    GOM_NEW = pd.DataFrame(data=GOM_NEW[GOM_NEW[GOOGLE_MOBILE_RANK] != "Not in top 50"])
    GOM_1 = pd.DataFrame(data=GOM_NEW[GOM_NEW[GOOGLE_MOBILE_RANK] == "1"])
    for x in range(5):
        GOM_5 = len(pd.DataFrame(data=GOM_NEW[GOM_NEW[GOOGLE_MOBILE_RANK] == str(x+1)]))
        TOP_5GOM.append(GOM_5)
        
    for x in range(10):
        GOM_FIRST = len(pd.DataFrame(data=GOM_NEW[GOM_NEW[GOOGLE_MOBILE_RANK] == str(x+1)]))
        GOM_FIRST_PAGE.append(GOM_FIRST)

    for x in range(20):
        GOM_TWO = len(pd.DataFrame(data=GOM_NEW[GOM_NEW[GOOGLE_MOBILE_RANK] == str(x+1)]))
        GOM_TWO_PAGE.append(GOM_TWO)
          
        
            
    GOM_LEN = len(GOM_DF)
    GOM_NEW_NOTE = pd.DataFrame(data=GOM_NEW[GOM_NEW[NOTE] == "NEW"])
    GOM_NOTE = len(GOM_NEW_NOTE)
    GOM_UP_NOTE = pd.DataFrame(data=GOM_NEW[GOM_NEW[NOTE] == "UP"])
    GOM_UP = len(GOM_UP_NOTE)
    GOM_DOWN_NOTE = pd.DataFrame(data=GOM_NEW[GOM_NEW[NOTE] == "DOWN"])
    GOM_DOWN = len(GOM_DOWN_NOTE)
    GOM_EQ_NOTE = pd.DataFrame(data=GOM_NEW[GOM_NEW[NOTE] == "EQ"])
    GOM_EQ = len(GOM_EQ_NOTE)
    GOM_LP_LEN = pd.DataFrame(data=df[GOOGLE_MOBILE_SERP])
       

    GOM_LP = len(GOM_LP_LEN)
    GOM_1_LEN = len(GOM_1)
    for x in range(len(df)):
        if LP_1 in str(GOM_LP_LEN[GOOGLE_MOBILE_SERP][x]):
            LP_GOM.append(GOM_LP_LEN[GOOGLE_MOBILE_SERP][x])
        else:
            False
 

      
            

    GOM_5_TOP = pd.DataFrame(data=TOP_5GOM)
    GOM5_TOP = GOM_5_TOP.sum()[0]
    GOM_FIRST_PAGE_TOP = pd.DataFrame(data=GOM_FIRST_PAGE)

    GOMFIRST_TOP = GOM_FIRST_PAGE_TOP.sum()[0]
    GOM_TWO_PAGE_TOP = pd.DataFrame(data=GOM_TWO_PAGE)
    GOMTWO_TOP= GOM_TWO_PAGE_TOP.sum()[0]
    BNG_DF = pd.DataFrame(data=BNG)
    BNG_NEW = pd.DataFrame(data=BNG_DF[BNG_DF[BING_RANK] != "Not in top 30"])
    BNG_NEW = pd.DataFrame(data=BNG_NEW[BNG_NEW[BING_RANK] != "Not in top 50"])
    BNG_LEN = len(BNG_NEW)
    BNG_1= pd.DataFrame(data=BNG_NEW[BNG_NEW[BING_RANK] == "1"])
    BNG_NEW_NOTE = pd.DataFrame(data=BNG_NEW[BNG_NEW[NOTE] == "NEW"])
    BNG_NOTE = len(BNG_NEW_NOTE)
    BNG_UP_NOTE = pd.DataFrame(data=BNG_NEW[BNG_NEW[NOTE] == "UP"])
    BNG_UP = len(BNG_UP_NOTE)
    BNG_DOWN_NOTE = pd.DataFrame(data=BNG_NEW[BNG_NEW[NOTE] == "DOWN"])
    BNG_DOWN = len(BNG_DOWN_NOTE)
    BNG_EQ_NOTE = pd.DataFrame(data=BNG_NEW[BNG_NEW[NOTE] == "EQ"])
    BNG_EQ = len(BNG_EQ_NOTE)
    BNG_LP_LEN = pd.DataFrame(data=df[BNG_SERP])
    BNG_LP = len(BNG_LP_LEN)
    BNG_1_LEN = len(BNG_1)
    TOP_5BNG = []
    BNG_FIRST_PAGE = []
    BNG_TWO_PAGE = []
    LP_BNG_ = []
    if LP_1 in str(BNG_LP_LEN[BING_SERP][x]):
        LP_BNG_.append(BNG_LP_LEN[BING_SERP][x])
    else:
        False
            
    for x in range(5):
        BNG_5 = len(pd.DataFrame(data=BNG_NEW[BNG_NEW[BING_RANK] == str(x+1)]))
        TOP_5BNG.append(BNG_5)
        
    for x in range(10):
        BNG_FIRST = len(pd.DataFrame(data=BNG_NEW[BNG_NEW[BING_RANK] == str(x+1)]))
        BNG_FIRST_PAGE.append(BNG_FIRST)

    for x in range(20):
        BNG_TWO = len(pd.DataFrame(data=BNG_NEW[BNG_NEW[BING_RANK] == str(x+1)]))
        BNG_TWO_PAGE.append(BNG_TWO)
        

    BNG_5_TOP = pd.DataFrame(data=TOP_5BNG)
    BNG5_TOP = BNG_5_TOP.sum()[0]
    BNG_FIRST_PAGE_TOP = pd.DataFrame(data=BNG_FIRST_PAGE)
    BNGFIRST_TOP = BNG_FIRST_PAGE_TOP.sum()[0]
    BNG_TWO_PAGE_TOP = pd.DataFrame(data=BNG_TWO_PAGE)
    BNGTWO_TOP= BNG_TWO_PAGE_TOP.sum()[0]
    LP_BNG_ = []

    YAH_DF = pd.DataFrame(data=YAH)
    YAH_NEW = pd.DataFrame(data=YAH_DF[YAH_DF [YAHOO_RANK] != "Not in top 30"])
    YAH_NEW = pd.DataFrame(data=YAH_NEW[YAH_NEW[YAHOO_RANK] != "Not in top 50"])
    YAH_LEN = len(YAH_NEW)
    YAH_1= pd.DataFrame(data=YAH_NEW[YAH_NEW[YAHOO_RANK] == "1"])
    YAH_NEW_NOTE = pd.DataFrame(data=YAH_NEW[YAH_NEW[NOTE] == "NEW"])
    YAH_NOTE = len(YAH_NEW_NOTE)
    YAH_UP_NOTE = pd.DataFrame(data=YAH_NEW[YAH_NEW[NOTE] == "UP"])
    YAH_UP = len(YAH_UP_NOTE)
    YAH_DOWN_NOTE = pd.DataFrame(data=YAH_NEW[YAH_NEW[NOTE] == "DOWN"])
    YAH_DOWN = len(YAH_DOWN_NOTE)
    YAH_EQ_NOTE = pd.DataFrame(data=YAH_NEW[YAH_NEW[NOTE] == "EQ"])
    YAH_EQ = len(YAH_EQ_NOTE)
    YAH_LP_LEN = pd.DataFrame(data=df[YAH_SERP])
    YAH_LP = len(YAH_LP_LEN)
    YAH_1_LEN = len(YAH_1)
    TOP_5YAH = []
    YAH_FIRST_PAGE = []
    YAH_TWO_PAGE = []
    LP_YAH_ = []

    for x in range(len(df)):
        if LP_1 in str(YAH_LP_LEN[YAHOO_SERP][x]):
            LP_YAH_.append(YAH_LP_LEN[YAHOO_SERP][x])
        else:
            False

    for x in range(5):
        YAH_5 = len(pd.DataFrame(data=YAH_NEW[YAH_NEW[YAHOO_RANK] == str(x+1)]))
        TOP_5YAH.append(YAH_5)
        
    for x in range(10):
        YAH_FIRST = len(pd.DataFrame(data=YAH_NEW[YAH_NEW[YAHOO_RANK] == str(x+1)]))
        YAH_FIRST_PAGE.append(YAH_FIRST)

    for x in range(20):
        YAH_TWO = len(pd.DataFrame(data=YAH_NEW[YAH_NEW[YAHOO_RANK] == str(x+1)]))
        YAH_TWO_PAGE.append(YAH_TWO)
        

    YAH_5_TOP = pd.DataFrame(data=TOP_5YAH)
    YAH5_TOP = YAH_5_TOP.sum()[0]
    YAH_FIRST_PAGE_TOP = pd.DataFrame(data=YAH_FIRST_PAGE)
    YAH_FIRST_TOP = YAH_FIRST_PAGE_TOP.sum()[0]
    YAH_TWO_PAGE_TOP = pd.DataFrame(data=YAH_TWO_PAGE)
    YAH_TWO_TOP= YAH_TWO_PAGE_TOP.sum()[0]

    for x in range(len(df)):
        if LP_1 in str(df[YAHOO_SERP][x]):
            LP_YAH_.append(df[YAHOO_SERP][x])
        else:
            False

    ARR = [GOM_1_LEN, GOD_1_LEN, BNG_1_LEN, YAH_1_LEN]
    ARR_1 = pd.DataFrame(ARR)
    TOP_1 = ARR_1.sum()[0]

    ARR_TOP_5 = [GOM5_TOP, GOD5_TOP, BNG5_TOP, YAH5_TOP]
    TOP_5 = pd.DataFrame(ARR_TOP_5)
    TOP_5 = TOP_5.sum()[0]

    ARR_FIRST_PAGE = [GODFIRST_TOP, GOMFIRST_TOP, BNGFIRST_TOP, YAH_FIRST_TOP]
    FIRST_PAGE_DF = pd.DataFrame(ARR_FIRST_PAGE)
    FIRST_PAGE = FIRST_PAGE_DF.sum()[0]


    ARR_TWO_PAGE = [GODTWO_TOP, GOMTWO_TOP, BNGTWO_TOP, YAH_TWO_TOP]
    FIRST_TWO_DF = pd.DataFrame(ARR_TWO_PAGE)
    FIRST_TWO = FIRST_TWO_DF.sum()[0]

    ARR_NEW_PAGE = [len(GOD_NEW_NOTE[GOD_NEW_NOTE['Ranking page(s)'].isnull() == False]), len(GOM_NEW_NOTE[GOM_NEW_NOTE['Ranking page(s)'].isnull() == False]), len(BNG_NEW_NOTE[BNG_NEW_NOTE['Ranking page(s)'].isnull() == False]), len(YAH_NEW_NOTE[YAH_NEW_NOTE['Ranking page(s)'].isnull() == False])]
    FIRST_NEW_DF = pd.DataFrame(ARR_NEW_PAGE)
    FIRST_NEW = FIRST_NEW_DF.sum()[0]
    ARR_UP_PAGE = [GOD_UP, GOM_UP, BNG_UP, YAH_UP]
    ARR_UP_DF = pd.DataFrame(ARR_UP_PAGE)
    ARR_UP = ARR_UP_DF.sum()[0]

    ARR_DOWN_PAGE = [GOD_DOWN, GOM_DOWN, BNG_DOWN, YAH_DOWN]
    ARR_DOWN_DF = pd.DataFrame(ARR_DOWN_PAGE)
    ARR_DOWN = ARR_DOWN_DF.sum()[0]

    ARR_EQ_PAGE = [GOD_EQ, GOM_EQ, BNG_EQ, YAH_EQ]
    ARR_EQ_DF = pd.DataFrame(ARR_EQ_PAGE)
    ARR_EQ = ARR_EQ_DF.sum()[0]

    ARR_GL = [ARR_UP, ARR_DOWN]
    ARR_GL_DF = pd.DataFrame(ARR_GL)
    ARR_GLDF = ARR_GL_DF.sum()[0]

    now = datetime.datetime.now()
    report_created = datetime.date(now.year, now.month, 1).strftime('%m/%d/%Y')

    first_day = datetime.date(now.year, now.month, 1) - datetime.timedelta(days=1)
    last_day = datetime.date(now.year, now.month, 1) - datetime.timedelta(days=first_day.day)

    date_range = f"{last_day.strftime('%m/%d/%Y')} through {first_day.strftime('%m/%d/%Y')}"
    head, sep, tail = df['Yahoo! URL Found'][0].replace('https://', "").partition(".com")
    NEW_HEAD = head.replace('www.', "")
   
    report_title = f"Actual SEO Media Report for {NEW_HEAD.upper()} Report for: {NEW_HEAD+sep} Report Date Range: {date_range} Report Section: Summary"

    report = [
    report_title,
    "",
    "SUM A",
    "General Report Statistics",
    "Report Created",
    "Keywords Analyzed",
    "Ranking Check Depth",
    "Engines Analyzed",
    "Geographic Target",
    "Baseline Report Date",
    "Baseline Keyword Count",
    "Services",
    "",
    "SUM B",
    "Visibility Statistics",
    "Listings in the First Position",
    "Listings in the Top 5 Positions",
    "Listings on the First Page",
    "Listings on the First Two Pages",
    "Listings New",
    "Listings Which Moved Up",
    "Listings Which Moved Down",
    "Listings Which Did Not Change",
    "Total Positions Gained/Lost",
    "",
    "GRAPH B",
    "GRAPH C",
    "GOD",
    "GOM",
    "BIN",
    "YAH",
    "",
    "GRAPH D",
    "GOD",
    "GOM",
    "BIN",
    "YAH"
    ]


    DATA_REPORTS = ["","","","",report_created,len(df), "25",'Google, Bing, Yahoo', 'Local', '7/15/2020', '47', 'SEO',"","","", TOP_1, TOP_5, FIRST_PAGE, FIRST_TWO, FIRST_NEW, ARR_UP, ARR_DOWN, ARR_EQ, ARR_GLDF,"",len(df),"",len(GOD_NEW), len(GOM_NEW),len(BNG_NEW), len(YAH_NEW),"","", len(LP_GOD_), len(LP_GOM), len(LP_BNG_), len(LP_YAH_)]

    CLEAN_REPORT = pd.DataFrame(index=report, data=DATA_REPORTS)    

    # tempLink = js.document.createElement('a')
    # tempLink2 = js.document.createElement('a')
    # tempLink3 = js.document.createElement('a')
    # tempLink4 = js.document.createElement('a')
    # tempLink5 = js.document.createElement('a')

    
    # blob = js.Blob.new([CLEAN_REPORT.to_csv(index = report , )], { type: 'text/csv' })
    # blob2 = js.Blob.new([GOD_NEW.to_csv(index = None, )], { type: 'text/csv' })
    # blob3 = js.Blob.new([GOM_NEW.to_csv(index = None, )], { type: 'text/csv' })
    # blob4 = js.Blob.new([BNG_NEW.to_csv(index = None, )], { type: 'text/csv' })
    # blob5 = js.Blob.new([YAH_NEW.to_csv(index = None, )], { type: 'text/csv' })

    # url = js.window.URL.createObjectURL(blob)
    # url2 = js.window.URL.createObjectURL(blob2)
    # url3 = js.window.URL.createObjectURL(blob3)
    # url4 = js.window.URL.createObjectURL(blob4)
    # url5 = js.window.URL.createObjectURL(blob5)


    # tempLink.href = url
    # tempLink2.href = url2
    # tempLink3.href = url3
    # tempLink4.href = url4
    # tempLink5.href = url5

    # js.console.log(tempLink)
    # js.console.log(tempLink2)
    # js.console.log(tempLink3)
    # js.console.log(tempLink4)
    # js.console.log(tempLink5)



    # tempLink.setAttribute('download', "ReportSummary.csv");
    # tempLink2.setAttribute('download', 'ReportSERPPositionsGOD.csv');
    # tempLink3.setAttribute('download', 'ReportSERPPositionsGOM.csv');
    # tempLink4.setAttribute('download', 'ReportSERPPositionsBNG.csv');
    # tempLink5.setAttribute('download', 'ReportSERPPositionsYAH.csv');

    # tempLink.click(); 
    # tempLink2.click();
    # tempLink3.click(); 
    # tempLink4.click(); 
    # tempLink5.click(); 

    
    links = []
    blobs = []
    filenames = [f"{NEW_HEAD.upper()}" + "_SUMMARY.csv", "ReportSERPPositionsGOD.csv", "ReportSERPPositionsGOM.csv", "ReportSERPPositionsBNG.csv", "ReportSERPPositionsYAH.csv"]
    dataframes = [CLEAN_REPORT, GOD_NEW, GOM_NEW, BNG_NEW, YAH_NEW]
    
    
    for i, df in enumerate(dataframes):
        if i == 0:
            blob = js.Blob.new([df.to_csv(index = report, sep='|')], {"type": "text/csv"})
            url = js.window.URL.createObjectURL(blob)
            link = js.document.createElement("a")
            link.href = url
            link.setAttribute("download", filenames[i])
            links.append(link)
            blobs.append(blob)
        else:
            blob = js.Blob.new([df.to_csv(index=None, header=False, sep='|')], {"type": "text/csv"})
            url = js.window.URL.createObjectURL(blob)
            link = js.document.createElement("a")
            link.href = url
            link.setAttribute("download", filenames[i])
            links.append(link)
            blobs.append(blob)
    for i, link in enumerate(links):
        js.console.log(link)
        link.click()
        
    ASM_FTP_UN = str(os.getenv('ASM_UN'))
    ASM_FTP_PW = str(os.getenv('ASM_PW'))





