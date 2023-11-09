classification = IN[0]

OUT = []

for cls in classification:
    # Safe Zone
    if cls == 1:
        hardhat = True
        vest = True
        safe = "Safe Zone"
        R01 = 1
        R02 = 0
        R03 = 3
        R04 = 3
        R05 = 2
        overall_risk = R01 + R02 + R03 + R04 + R05
        category = "Low Risk"
        OUT.append([hardhat, vest, safe, R01, R02, R03, R04, R05, overall_risk, category])
      
    elif cls == 2:
        hardhat = True
        vest = False
        safe = "Safe Zone"
        R01 = 1
        R02 = 0
        R03 = 6
        R04 = 3
        R05 = 2
        overall_risk = R01 + R02 + R03 + R04 + R05
        category = "Moderate Risk"
        OUT.append([hardhat, vest, safe, R01, R02, R03, R04, R05, overall_risk, category])
      
    elif cls == 3:
        hardhat = False
        vest = True
        safe = "Safe Zone"
        R01 = 1
        R02 = 0
        R03 = 3
        R04 = 6
        R05 = 4
        overall_risk = R01 + R02 + R03 + R04 + R05
        category = "Moderate Risk"
        OUT.append([hardhat, vest, safe, R01, R02, R03, R04, R05, overall_risk, category])
      
    else:
        hardhat = False
        vest = False
        safe = "Safe Zone"
        R01 = 1
        R02 = 0
        R03 = 6
        R04 = 6
        R05 = 4
        overall_risk = R01 + R02 + R03 + R04 + R05
        category = "Significant Risk"
        OUT.append([hardhat, vest, safe, R01, R02, R03, R04, R05, overall_risk, category])
