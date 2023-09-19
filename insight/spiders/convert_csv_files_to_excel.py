import os

import pandas
import pandas as pd

from convert_jl_to_csv_script import ConvertJlToCsvScript


class ConvertCsvFilesToExcel:
    files_directory = '../output'

    def __init__(self):
        ConvertJlToCsvScript()

        self.excel_file_path = f'{self.files_directory}/Insight Products.xlsx'
        self.convert_csv_files_to_excel()

    def convert_csv_files_to_excel(self):
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(self.excel_file_path, engine='xlsxwriter')

        for filepath in self.get_sorted_files(self.get_files()):
            df = pandas.read_csv(filepath, encoding='utf-8')

            sheet_name = filepath.split('/')[-1].replace('.csv', '')
            # Convert the data frame to an XlsxWriter Excel object.
            df.to_excel(writer, index=False, sheet_name=sheet_name)
            print(f"{sheet_name} sheet written into excel file")

        # # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        print(f"{self.excel_file_path} Excel File Has Been Generated Successfully..!!")

    def get_output_dir_abs_path(self):
        return "/".join(os.getcwd().split('/')[:-1] + ['output'])

    def get_files(self):
        files = []

        for file_path in os.listdir(self.files_directory):
            if '.csv' not in file_path:
                continue
            file_path = self.files_directory + '/' + file_path
            files.append(file_path)

        return files

    def get_sorted_files(self, files):
        sheets = {int(f.split('.csv')[0].split('_')[-1]): f for f in files}
        return [sheets[k] for k in sorted(sheets)]


if __name__ == "__main__":
    ConvertCsvFilesToExcel()
