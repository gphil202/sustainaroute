import json
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

list_of_files = ["data_2.json", "data_2_incomplete.json", "data_3.json", "data_3.json", "data_4.json",
                 "data_run1_may_be_incomplete.json", "data_5.json", "data_6.json", "data_7.json", "data_8.json"]


def extract_members() -> set:
    merged_dict = dict()
    members_set = set()

    for in_dict in list_of_files:
        with open(in_dict, "r") as dict_file:
            data = json.load(dict_file)

        merged_dict = {**merged_dict, **data}

    regexp_users = re.compile(r"@\w+[^/?@]")
    for url in merged_dict.keys():
        mo = re.findall(regexp_users, url)
        for elem in mo:
            if elem is not None:
                to_add = elem
                # len_gr = len(mo.groups())
                if to_add.endswith("cdn-"):
                    to_add = to_add[:-len("cdn-")]
                members_set.add(to_add)

    print(f"Extracted {len(members_set)} members")
    return members_set


def download_profile_data(members_set: set):
    website = "https://nomadlist.com/"
    df = pd.DataFrame()
    for member in tqdm(members_set):
        html_data = requests.get(website + member).text
        soup = BeautifulSoup(html_data, "html.parser")

        cities_visited = []
        countries_visited = []
        # for heading in soup.find_all(re.compile('^h[1-6]$')):  # grab headings
        for td_class in soup.find_all('td'):
            if len(td_class.attrs) > 0:
                try:
                    if td_class.attrs["class"][0] == "name":
                        cities_visited.append(td_class.contents[1].text.lstrip("\n").rstrip("\n "))
                    if td_class.attrs["class"][0] == "country":
                        countries_visited.append(td_class.contents[0].text.lstrip("\n").rstrip("\n "))
                except (IndexError, KeyError):
                    pass

        if len(cities_visited) <= 0 or len(countries_visited) <= 0:
            continue

        # extract recommendations from reduced block
        recommended_city = []
        recommended_country = []
        html_data = html_data[
                    html_data.find("Recommended destinations they haven't been"):html_data.find("Regions collected")]
        regex_recommended_city = re.compile(r'title="(\w+\s)(\w+\s)*for\sDigital\sNomads')
        regex_recommended_country = re.compile(r'<a\shref="/country/\w+"\stitle="\w+\sfor\sa\sDigital\sNomad')

        for match in re.findall(regex_recommended_city, html_data):
            city_str = ""
            for item in match:
                city_str += " " + item
            recommended_city.append(city_str.lstrip(" ").rstrip(" "))

        for elem in re.findall(regex_recommended_country, html_data):
            recommended_country.append(elem[elem.find("title=") + len("title=") + 1:-len(" for a Digital Nomad")])

        arg_visited = [city + ", " + country for (city, country) in zip(cities_visited, countries_visited)]
        #arg_visited = list(cities_visited)
        arg_nomadlist_recommends = [city + ", " + country for (city, country) in
                                    zip(recommended_city, recommended_country)]
        # arg_nomadlist_recommends = list(recommended_city)
        arg_dict = {"username": member, "visited": arg_visited, "nomadlist_recommends": arg_nomadlist_recommends}
        new_df = pd.DataFrame.from_dict(arg_dict, orient="index")
        print(f"\nadding entry to dataframe: {arg_dict}")
        df = pd.concat([df, new_df.transpose()])

    df.to_csv("travel_info_profiles.csv", encoding='utf-8', index=False)
    print(f"Exported {len(df)} entries to csv")


if __name__ == "__main__":
    print("Parsing Crawler output to retrieve members...")
    members_suburl_set = extract_members()
    print("Building dataset...")
    download_profile_data(members_suburl_set)
    print("Finished building dataset, saved results to csv file")
