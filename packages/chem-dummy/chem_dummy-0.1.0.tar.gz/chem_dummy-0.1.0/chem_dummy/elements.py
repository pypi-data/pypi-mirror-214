import json
import pandas as pd
import importlib.resources


class Properties:
    def __init__(self):
        with importlib.resources.open_text("chem_dummy", "properties_of_elements.json") as file:
            data = json.load(file)
        big_ls = []
        for ele in data:
            big_ls.append(data[ele])
        df = pd.DataFrame(big_ls)
        df.fillna('Information Not Available', inplace=True)

        self.df = df


class Functions(Properties):
    def __init__(self):
        super().__init__()

    def get_element_details_based_on_atomic_number(self, atomic_number):
        """
            get_element_details_based_on_atomic_number: Get Element details based on atomic number

            Params:
            ------
            atomic_number: int: This should be a number between 1 and 118

            Usage:
            -----
            >> > from periodic_element_properties import Functions
            >> > f = Functions()
            >> > element_info = f.get_element_details_based_on_atomic_number(3)
            >> > print(element_info)
        """
        if atomic_number <= 0 or atomic_number > 118:
            return "Element doesn't exist"
        raw_data = self.df[self.df['AtomicNumber'] == atomic_number].to_dict('records')[
            0]
        return raw_data

    def get_elements_belonging_to_a_particular_group(self, group):
        """
            get_elements_belonging_to_a_particular_group: This function lists down the elements which belong to a particuar group

            Params:
            ------
            group: int: This should be a number between 1 and 18

            Usage:
            -----
            >> > from periodic_element_properties import Functions
            >> > f = Functions()
            >> > group_info = f.get_elements_belonging_to_a_particular_group(18)
            >> > print(group_info)
        """
        if group <= 0 or group > 18:
            return "Group doesn't exist"
        raw_data = self.df[self.df['Group'] == group].to_dict('records')
        return raw_data

    def get_elements_belonging_to_a_particular_period(self, period):
        """
            get_elements_belonging_to_a_particular_period: This function lists down the elements which belong to a particuar period

            Params:
            ------
            group: int: This should be a number between 1 and 7

            Usage:
            -----
            >> > from periodic_element_properties import Functions
            >> > f = Functions()
            >> > period_info = f.get_elements_belonging_to_a_particular_period(1)
            >> > print(period_info)
        """
        if period <= 0 or period > 7:
            return "Period doesn't exist"
        raw_data = self.df[self.df['Period'] == period].to_dict('records')
        return raw_data
