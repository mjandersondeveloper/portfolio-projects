class Criminal:
    def __init__(self, juv_fel_count: int, juv_misd_count: int, juv_other_count: int, priors_count: int, v_decile_score: int):
        self.juv_fel_count = juv_fel_count
        self.juv_misd_count = juv_misd_count
        self.juv_other_count = juv_other_count
        self.priors_count = priors_count
        self.v_decile_score = v_decile_score

# The weight rating from a criminal's juv_fel_count are as follows:
# If the input equals 0, the weight rating will be 0
# If the input is 1 > juv_fel_count <= 6, the weight rating will be 0.5
# Any input over 6 will return a rating of 1
def juv_fel_count_weight(jfc: int) -> int:
    if (jfc == 0):
        return 0
    elif (jfc > 1 and jfc <= 6):
        return 0.5
    else:
        return 1

# The weight rating from a criminal's juv_misd_count are as follows:
# If the input equals 0, the weight rating will be 0
# If the input is 1 > juv_misd_count <= 6, the weight rating will be 0.5
# Any input over 6 will return a rating of 1
def juv_misd_count_weight(jmc: int) -> int:
    if (jmc == 0):
        return 0
    elif (jmc > 1 and jmc <= 6):
        return 0.5
    else:
        return 1

# The weight rating from a criminal's juv_other_count are as follows:
# If the input equals 0, the weight rating will be 0
# If the input is 1 > juv_other_count <= 6, the weight rating will be 0.5
# Any input over 6 will return a rating of 1
def juv_other_count_weight(joc: int) -> int:
    if (joc == 0):
        return 0
    elif (joc > 1 and joc <= 6):
        return 0.5
    else:
        return 1

# The weight rating from a criminal's priors_count are as follows:
# If the input equals 0, the weight rating will be 0
# If the input is 1 > priors_count <= 12, the weight rating will be 0.25
# If the input is 12 > priors_count <= 24, the weight rating will be 0.5
# Any input over 24 will return a rating of 1
def priors_count_weight(pc: int) -> int:
    if (pc == 0):
        return 0
    elif (pc > 1 and pc <= 12):
        return 0.25
    elif(pc > 12 and pc <= 24):
        return 0.5
    else:
        return 1

# Because the violent score is a big part of the risk score, the weight values are as follows:
# If the input is 1 or 2, the weight rating will be 1
# If the input is 3 or 4, the weight rating will be 2
# If the input is 5 or 6, the weight rating will be 3
# If the input is 7 or 8, the weight rating will be 4
# If the input is 9 or 10, the weight rating will be 5
def v_decile_score(vdc: int) -> int:
    if (vdc == 1 or vdc == 2):
        return 1
    elif(vdc == 3 or vdc == 4):
        return 2
    elif(vdc == 5 or vdc == 6):
        return 3
    elif(vdc == 7 or vdc == 8):
        return 4
    else:
        return 5

# This where the new decile_score value will be stored
# Based on the sum of the five methods that return a weight value, the new, and more fairly assessed risk value will be assigned to the criminal
decile_score = 0

# This object holds the values assigned to the respective columns in the raw data
# These will be used as inputs for the five methods that return a respective weight value
criminal = Criminal(0,12,2,28,5)

decile_score += juv_fel_count_weight(criminal.juv_fel_count)
decile_score += juv_misd_count_weight(criminal.juv_misd_count)
decile_score += juv_other_count_weight(criminal.juv_other_count)
decile_score += priors_count_weight(criminal.priors_count)
decile_score += v_decile_score(criminal.v_decile_score)

# Final decile_score based on the sum of all calculated weights
print(decile_score)
