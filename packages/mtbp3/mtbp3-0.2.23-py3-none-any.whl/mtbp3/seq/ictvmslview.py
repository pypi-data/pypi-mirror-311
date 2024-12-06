#  Copyright (C) 2023-2024 Y Hsu <yh202109@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public license as published by
#  the Free software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details
#
#  You should have received a copy of the GNU General Public license
#  along with this program. If not, see <https://www.gnu.org/license/>

import pandas as pd
import os
from mtbp3 import util
import warnings
import requests

warnings.simplefilter(action='ignore', category=FutureWarning)
    
class ictvmsl:
    """
    A class to handle ICTV Master Species List (MSL) data.
    Attributes:
    -----------
    msl_file_path : str
        Path to the MSL file.
    msl_file_fullpath : str
        Full path to the MSL file.
    msl_version : str
        Version of the MSL.
    msl_column_names : list
        List of column names in the MSL.
    msl : DataFrame
        The MSL data loaded into a pandas DataFrame.
    Methods:
    --------
    update_msl(self, version="current")
        Updates the MSL data by downloading the specified version from the ICTV website.
    make_narrow(msl)
        Converts the MSL DataFrame to a narrower format by combining certain columns.
    find_rows_given_str(self, search_str="", search_rank="Species", color="", narrow=False, outfmt="simple", exact=False, search_within_subset=None)
        Finds rows in the MSL DataFrame that contain the given search string.
    """

    def __init__(self, msl_file_path = ""):
        if not isinstance(msl_file_path, str):
            raise TypeError("msl_file_path must be a string")

        if msl_file_path:
            self.msl_file_path = msl_file_path
            self.msl_file_fullpath = msl_file_path
        else:
            self.msl_file_path = f'supp_seq/ICTV_MSL39v4_example.csv'
            self.msl_file_fullpath = util.get_data(self.msl_file_path)

        self.msl_version = ""
        self.msl_column_names = []
        self.msl = self.__load_list()

        if self.msl is not None:
            self.msl_column_names = self.msl.columns.tolist()
            print(f"File {self.msl_file_path} has been loaded")
            print("Column names:", self.msl_column_names)
            print("Total number of rows:", len(self.msl))

    def update_msl(self, version="current"):
        all_url = {
            "current": "https://ictv.global/msl/current",
            "39.v4": "https://ictv.global/sites/default/files/MSL/ICTV_Master_Species_List_2023_MSL39.v4.xlsx",
            "39.v3": "https://ictv.global/sites/default/files/MSL/ICTV_Master_Species_List_2023_MSL39.v3.xlsx"
        }
        if version in all_url:
            url = all_url[version]
        else:
            raise ValueError(f"Version {version} is not supported. Supported versions are: {', '.join(all_url.keys())}")

        response = requests.get(url)
        if response.status_code == 200:
            with open("temp.xlsx", "wb") as f:
                f.write(response.content)
            self.msl = pd.read_excel("temp.xlsx", sheet_name="MSL")
            os.remove("temp.xlsx")
            self.msl_column_names = self.msl.columns.tolist()
            print(f"File of version {version} has been loaded")
            print("Column names:", self.msl_column_names)
            print("Total number of rows:", len(self.msl))
        else:
            raise Exception(f"Failed to download file from {url}. Status code: {response.status_code}")


    @staticmethod
    def make_narrow(msl):
        if 'Realm' in msl.columns and 'Subrealm' in msl.columns:
            index1 = msl.columns.get_loc('Realm')
            index2 = msl.columns.get_loc('Subrealm')
            msl.iloc[:, index1] = msl.apply(lambda row: f"{row[index1]}(Subrealm:{row[index2]})" if pd.notna(row[index1]) else row[index1], axis=1)
            #msl['Realm'] = msl.apply(lambda row: f"{row['Realm']}(Subrealm:{row['Subrealm']})" if pd.notna(row['Subrealm']) else row['Realm'], axis=1)
        if 'Kingdom' in msl.columns and 'Subkingdom' in msl.columns:
            index1 = msl.columns.get_loc('Kingdom')
            index2 = msl.columns.get_loc('Subkingdom')
            msl.iloc[:, index1] = msl.apply(lambda row: f"{row[index1]}(Subkingdom:{row[index2]})" if pd.notna(row[index2]) else row[index1], axis=1)
            #msl['Kingdom'] = msl.apply(lambda row: f"{row['Kingdom']}(Subkingdom:{row['Subkingdom']})" if pd.notna(row['Subkingdom']) else row['Kingdom'], axis=1)
        if 'Phylum' in msl.columns and 'Subphylum' in msl.columns:
            index1 = msl.columns.get_loc('Phylum')
            index2 = msl.columns.get_loc('Subphylum')
            msl.iloc[:, index1] = msl.apply(lambda row: f"{row[index1]}(Subphylum:{row[index2]})" if pd.notna(row[index2]) else row[index1], axis=1)
            #msl['Phylum'] = msl.apply(lambda row: f"{row['Phylum']}(Subphylum:{row['Subphylum']})" if pd.notna(row['Subphylum']) else row['Phylum'], axis=1)
        if 'Class' in msl.columns and 'Subclass' in msl.columns:
            index1 = msl.columns.get_loc('Class')
            index2 = msl.columns.get_loc('Subclass')
            msl.iloc[:, index1] = msl.apply(lambda row: f"{row[index1]}(Subclass:{row[index2]})" if pd.notna(row[index2]) else row[index1], axis=1)
            #msl['Class'] = msl.apply(lambda row: f"{row['Class']}(Subclass:{row['Subclass']})" if pd.notna(row['Subclass']) else row['Class'], axis=1)
        if 'Order' in msl.columns and 'Suborder' in msl.columns:
            index1 = msl.columns.get_loc('Order')
            index2 = msl.columns.get_loc('Suborder')
            msl.iloc[:, index1] = msl.apply(lambda row: f"{row[index1]}(Suborder:{row[index2]})" if pd.notna(row[index2]) else row[index1], axis=1)
            #msl['Order'] = msl.apply(lambda row: f"{row['Order']}(Suborder:{row['Suborder']})" if pd.notna(row['Suborder']) else row['Order'], axis=1)
        if 'Family' in msl.columns and 'Subfamily' in msl.columns:
            index1 = msl.columns.get_loc('Family')
            index2 = msl.columns.get_loc('Subfamily')
            msl.iloc[:, index1] = msl.apply(lambda row: f"{row[index1]}(Subfamily:{row[index2]})" if pd.notna(row[index2]) else row[index1], axis=1)
            #msl['Family'] = msl.apply(lambda row: f"{row['Family']}(Subfamily:{row['Subfamily']})" if pd.notna(row['Subfamily']) else row['Family'], axis=1)
        if 'Genus' in msl.columns and 'Subgenus' in msl.columns:
            index1 = msl.columns.get_loc('Genus')
            index2 = msl.columns.get_loc('Subgenus')
            msl.iloc[:, index1] = msl.apply(lambda row: f"{row[index1]}(Subgenus:{row[index2]})" if pd.notna(row[index2]) else row[index1], axis=1)
            #msl['Genus'] = msl.apply(lambda row: f"{row['Genus']}(Subgenus:{row['Subgenus']})" if pd.notna(row['Subgenus']) else row['Genus'], axis=1)
        msl = msl.iloc[:, :-4]
        msl2 = msl.drop(columns=[col for col in msl.columns if col.lower().startswith('sub')])
        return msl2

    def __load_list(self):
        #file_path = f'./mtbp3/data/supp_seq/ICTV_MSL39v4_example.csv'
        file_path = self.msl_file_fullpath
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path)
            return df
        else:
            raise FileNotFoundError(f"File not found: {file_path}")

    def find_rows_given_str(self, search_str="", search_rank="Species", color="", narrow=False, outfmt="simple", exact=False, search_within_subset=None):
        """
        Find rows in the MSL dataframe that match a given search string.
        Parameters:
        search_str (str): The string to search for. Must be a nonempty string.
        search_rank (str): The rank to search within (e.g., "Species"). Must be 'all' or one of the column names in the MSL dataframe.
        color (str): The color to highlight the search string in the results.
        narrow (bool): Whether to narrow the results to a specific format.
        outfmt (str): The output format. Must be 'simple' or 'tree'.
        exact (bool): Whether to search for an exact match.
        search_within_subset (dict): A dictionary specifying a subset of the MSL dataframe to search within.
        Returns:
        pandas.DataFrame or str: The filtered dataframe if outfmt is 'simple', or a tree representation of the results if outfmt is 'tree'.
        Raises:
        TypeError: If search_str is not a string or if search_within_subset is not a dictionary or None.
        ValueError: If search_str is empty, if search_rank is invalid, or if outfmt is invalid.
        """

        if not isinstance(search_str, str):
            raise TypeError("search_str must be a string")
        if not search_str:
            raise ValueError("search_str must be a nonempty string")
        if search_rank and search_rank != "all" and search_rank not in self.msl_column_names:
            raise ValueError(f"search_rank must be 'all' or one of the following: {', '.join(self.msl_column_names)}")
        if outfmt not in ["simple", "tree"]:
            raise ValueError("outfmt must be 'simple' or 'tree'")
        if search_within_subset is not None and not isinstance(search_within_subset, dict):
            raise TypeError("search_subset must be a dictionary or None")

        msl2 = self.msl
        if search_within_subset is not None:
            for key, value in search_within_subset.items():
                if key in msl2.columns and isinstance(value, str) and value:
                    index = msl2.columns.get_loc(key)
                    msl2 = msl2[msl2.iloc[:, index].str.lower() == value.lower()]

        if search_rank == "all":
            if exact:
                filtered_df = msl2[msl2.iloc[:, 1:16].apply(lambda row: search_str.lower() == row.astype(str).str.lower().values, axis=1)]
                if color:
                    for col in filtered_df[1:16]:
                        filtered_df[col] = filtered_df[col].apply(lambda row: util.cdt.color_str(row, words=search_str, colors=color, exact=exact) if pd.notna(row) else row)
            else:
                filtered_df = msl2[msl2.iloc[:, 1:16].apply(lambda row: search_str.lower() in row.astype(str).str.lower().values, axis=1)]
                if color:
                    for col in filtered_df[1:16]:
                        filtered_df[col] = filtered_df[col].apply(lambda row: util.cdt.color_str(row, words=search_str, colors=color, exact=exact) if pd.notna(row) else row)
            if narrow:
                filtered_df = self.make_narrow(filtered_df)
        else:
            if exact:
                filtered_df = msl2[msl2[search_rank].str.lower() == search_str.lower()]
            else:
                filtered_df = msl2[msl2[search_rank].str.contains(search_str, case=False, na=False)]

            if color:
                index = msl2.columns.get_loc(search_rank)
                filtered_df.iloc[:, index] = filtered_df.iloc[:, index].apply(lambda row: util.cdt.color_str(row, words=search_str, colors=color, exact=exact))
                #filtered_df[search_rank] = filtered_df[search_rank].apply(lambda row: util.cdt.color_str(row, words=search_str, colors=color, exact=exact))

            if narrow:
                filtered_df = self.make_narrow(filtered_df)

        if outfmt == "simple":
            return filtered_df
        elif outfmt == "tree" and not narrow:
            filtered_df = self.make_narrow(filtered_df)

            tree_list = filtered_df['Realm'].unique().tolist()
            tree_list = [f"/[Realm] {item}/" for item in tree_list]
            tmp = filtered_df[['Realm', 'Kingdom']].drop_duplicates()
            tmp['string'] = tmp.apply(lambda row: f"/[Realm] {row['Realm']}/[Kingdom] {row['Kingdom']}/", axis=1)
            tree_list = tree_list + tmp['string'].unique().tolist()
            tmp = filtered_df[['Realm', 'Kingdom', 'Phylum']].drop_duplicates()
            tmp['string'] = tmp.apply(lambda row: f"/[Realm] {row['Realm']}/[Kingdom] {row['Kingdom']}/[Phylum] {row['Phylum']}/", axis=1)
            tree_list = tree_list + tmp['string'].unique().tolist()
            tmp = filtered_df[['Realm', 'Kingdom', 'Phylum', 'Class']].drop_duplicates()
            tmp['string'] = tmp.apply(lambda row: f"/[Realm] {row['Realm']}/[Kingdom] {row['Kingdom']}/[Phylum] {row['Phylum']}/[Class] {row['Class']}/", axis=1)
            tree_list = tree_list + tmp['string'].unique().tolist()
            tmp = filtered_df[['Realm', 'Kingdom', 'Phylum', 'Class', 'Order']].drop_duplicates()
            tmp['string'] = tmp.apply(lambda row: f"/[Realm] {row['Realm']}/[Kingdom] {row['Kingdom']}/[Phylum] {row['Phylum']}/[Class] {row['Class']}/[Order] {row['Order']}/", axis=1)
            tree_list = tree_list + tmp['string'].unique().tolist()
            tmp = filtered_df[['Realm', 'Kingdom', 'Phylum', 'Class', 'Order', 'Family']].drop_duplicates()
            tmp['string'] = tmp.apply(lambda row: f"/[Realm] {row['Realm']}/[Kingdom] {row['Kingdom']}/[Phylum] {row['Phylum']}/[Class] {row['Class']}/[Order] {row['Order']}/[Family] {row['Family']}/", axis=1)
            tree_list = tree_list + tmp['string'].unique().tolist()
            tmp = filtered_df[['Realm', 'Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus']].drop_duplicates()
            tmp['string'] = tmp.apply(lambda row: f"/[Realm] {row['Realm']}/[Kingdom] {row['Kingdom']}/[Phylum] {row['Phylum']}/[Class] {row['Class']}/[Order] {row['Order']}/[Family] {row['Family']}/[Genus] {row['Genus']}/", axis=1)
            tree_list = tree_list + tmp['string'].unique().tolist()
            tmp = filtered_df[['Realm', 'Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']].drop_duplicates()
            tmp['string'] = tmp.apply(lambda row: f"/[Realm] {row['Realm']}/[Kingdom] {row['Kingdom']}/[Phylum] {row['Phylum']}/[Class] {row['Class']}/[Order] {row['Order']}/[Family] {row['Family']}/[Genus] {row['Genus']}/[Species] {row['Species']}", axis=1)
            tree_list = tree_list + tmp['string'].unique().tolist()
            out_tree = util.cdt.ListTree(lst=tree_list)
            return out_tree.list_tree()
        else:
            return

if __name__ == "__main__":
    pass
