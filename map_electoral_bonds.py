import csv
import pandas as pd
import json
import matplotlib.pyplot as plt
import decimal


bond_to_company_name_map = {}
def reduce_purchasedetails():
    with open('PurchaseDetails.csv', newline='') as csvfile:
        purchase_details = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for purchase in purchase_details:
            bond_number = purchase["BondNumber"]
            buyer_name = purchase["NameOfThePurchaser"]
            bond_to_company_name_map[bond_number] = buyer_name


def get_base_dataframe():
    input_list = []
    party_file = open("PartyShortNames.json")
    party_short_names = json.load(party_file)
    with open('Redeemed.csv', newline='') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            denomination = int(row.get("Denominations").replace(",", ""))/10000000
            
            short_name = party_short_names.get(row.get("NameOfThePoliticalParty"))
            row["Denominations"] = denomination
            row["NameOfThePoliticalParty"] = short_name
            row["BondNumber"] = bond_to_company_name_map.get(row['BondNumber'])
            input_list.append(row)
    df = pd.DataFrame(input_list)
    return df

def total_received_by_parties():
    df = get_base_dataframe()
    df1 = df.groupby(['NameOfThePoliticalParty'])['Denominations'].sum()
    plot = df1.plot(kind='bar', title='TotalReceivedByParties',
                    xlabel='NameOfThePoliticalParty', ylabel='ReceivedInCrores', legend=False)
    plot.bar_label(plot.containers[0], label_type='edge')
    plt.show()



def getCompanyWiseDataFrames():
    df = get_base_dataframe()
    party_file = open("PartyShortNames.json")
    party_short_names = json.load(party_file).values()
    for party in party_short_names:
        final_dict = {}
        if party == "BJP":
            result_df = df.loc[(df["NameOfThePoliticalParty"] == party) &
                               (df["Denominations"] > 100.0),
                               ['NameOfThePoliticalParty', 'Denominations']]
            result_list = result_df.to_dict('index').values()
            json_data = json.dumps(list(result_list))
            f = open("result/"+party+'.json', 'w')
            f.write(json_data)
        else:    
            result_df = df[df["NameOfThePoliticalParty"] == party]
            result_list = result_df.to_dict('index').values()
            json_data = json.dumps(list(result_list))
            f = open("result/"+party+'.json', 'w')
            f.write(json_data)


def draw_partywise_graph(party):
    df = pd.read_json("result/"+ party +".json")
    df1 = df.groupby(['NameOfThePoliticalParty', 'BondNumber'])['Denominations'].sum()
    plot = df1.plot(kind='bar', title='CompaniesDonated',
                    xlabel='CompanyNames', ylabel='AmountDonated', legend=False)
    plot.bar_label(plot.containers[0], label_type='edge')
    plt.show()


if __name__ == "__main__":
    #total_received_by_parties()
    reduce_purchasedetails()
    getCompanyWiseDataFrames()
    draw_partywise_graph("BJP")

