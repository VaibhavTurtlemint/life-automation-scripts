import csv

# Below script is for interdependency import

f1 = open('./interdependency_rider_mashreq.java', 'w+')

with open('/Users/vaibhavsawant/Downloads/Import_Data/Life Rider Masters_Rules - Mashreq - RiderInterdependency.csv',
          mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    s8 = ' ' * 8
    s12 = ' ' * 12

    ruleNameText = 'rule "Mashreq Rider Interdependency - {0}, {1}, {2}"\n'

    whenRuleText = """    when
        riderRequest:RiderRequest(
            riderRequest.getRiderCode() == "{0}" &&
            riderRequest.getProductCode() == "{1}" &&
            riderRequest.getOptionCode() == "{2}" &&
            riderRequest.getRuleId() == "interDependentRiders" &&
            riderRequest.getBroker() == "mashreq"
        )
"""

    thenResponseText = """    then
        InterDependendRiderResponse response = new InterDependendRiderResponse();
        response.setRiderCode(riderRequest.getRiderCode());
        response.setProductCode(riderRequest.getProductCode());
        response.setOptionCode(riderRequest.getOptionCode());
        ArrayList<String> includedRiders = new ArrayList<>();
        ArrayList<String> excludedRiders = new ArrayList<>();{}
        response.setIncludedRiders(includedRiders);
        response.setExcludedRiders(excludedRiders);
        rulesResponse.setRuleResponse(response);
end
"""

    for row in csv_reader:
        row = {k: v.strip() for k, v in row.items()}
        ruleName = ruleNameText.format(row["riderCode"], row["productCode"], row["optionCode"])
        whenRule = whenRuleText.format(row["riderCode"], row["productCode"], row["optionCode"])

        includedRiderString = row["includedRiders"]
        excludedRiderString = row["excludedRiders"]

        thenResponseRidersData = ""
        if includedRiderString is not None and len(includedRiderString) != 0:
            includedRiders = [x.strip() for x in includedRiderString.split(',')]
            for includedRider in includedRiders:
                thenResponseRidersData += '\n' + s8 + 'includedRiders.add("' + includedRider + '");'

        if excludedRiderString is not None and len(excludedRiderString) != 0:
            excludedRiders = [x.strip() for x in excludedRiderString.split(',')]
            for excludedRider in excludedRiders:
                thenResponseRidersData += '\n' + s8 + 'excludedRiders.add("' + excludedRider + '");'

        thenResponse = thenResponseText.format(thenResponseRidersData)
        print >> f1, (ruleName + whenRule + thenResponse)

f1.close()
