import os
from csv import DictReader

from utils import get_jl_records


class ConvertJlToCsvScript:
    files_directory = "../output"
    output_file_dir = "../output"

    def __init__(self):
        self.convert_jl_files_to_csv()

    def convert_jl_files_to_csv(self):
        for filepath in self.get_sorted_files(self.get_files()):
            headers = self.get_file_headers(filepath)

            records = []

            for r in get_jl_records(filepath):
                r['meta']['csv_headers'] = headers

                listings_details = r.pop('listings_details')
                listings_details.pop('insightPrice', '')
                listings_details.pop('listPrice', '')
                listings_details.pop('manufacturerName', '')
                listings_details.pop('manufacturerPartNumber', '')
                listings_details.pop('availabilityMessage', '')

                r.update(listings_details)
                r.update(r['meta'])

                records.append(r)

            self.write_bulk_to_csv(records)

            print(f"{filepath}.jl file Converted to CSV file!")

    def write_bulk_to_csv(self, records):
        csv_writer = None
        file_headers = None

        for item in records:
            item.pop('listings_details', {})

            if not csv_writer or not file_headers:
                meta = item.pop('meta')
                file_headers = meta['csv_headers']
                filepath = f"{self.output_file_dir.rstrip('/')}/{meta['filepath']}"
                csv_writer = self.get_csv_writer(filepath, file_headers)

            row = ','.join('"{}"'.format(str(item.get(h, '')).replace('"', '')) for h in file_headers) + '\n'
            csv_writer.write(row)

            print(item)

        csv_writer.close()

    def write_to_csv(self, item):
        item.pop('listings_details', {})
        meta = item.pop('meta')
        file_headers = meta['csv_headers']
        filepath = f"{self.output_file_dir.rstrip('/')}/{meta['filepath']}"

        row = ','.join('"{}"'.format(str(item.get(h, '')).replace('"', '')) for h in file_headers) + '\n'

        csv_writer = self.get_csv_writer(filepath, file_headers)
        csv_writer.write(row)
        csv_writer.close()
        return item

    def get_csv_writer(self, filepath, file_headers):
        # file = open(self.output_csv_file_name, mode='w', encoding='utf-8')
        # file.write(','.join(h for h in file_headers) + '\n')
        # return file

        if not os.path.exists(filepath) or len(self.has_records(filepath)) < 1:
            file = open(filepath, mode='w', encoding='utf-8')
            file.write(','.join(h for h in file_headers) + '\n')
            return file

        return open(filepath, mode='a', encoding='utf-8')

    def has_records(self, filepath):
        if not os.path.exists(filepath):
            return []
        return [r['Link'] for r in
                DictReader(open(filepath, encoding='utf-8')) if r and r['Link']]

    def get_output_dir_abs_path(self):
        return "/".join(os.getcwd().split('/')[:-1] + ['output_new'])

    def get_files(self):
        files = []

        for file_path in os.listdir(self.files_directory):
            if '.jl' not in file_path:
                continue
            file_path = self.files_directory + '/' + file_path
            files.append(file_path)

        return files

    def get_sorted_files(self, files):
        sheets = {}

        for f in files:
            sheets[int(f.split('.jl')[0].split('_')[-1])] = f

        return [sheets[k] for k in sorted(sheets)]

    def get_file_headers(self, filepath):
        headers = []

        for r in get_jl_records(filepath):
            listings_details = r.pop('listings_details')
            listings_details.pop('insightPrice', '')
            listings_details.pop('listPrice', '')
            listings_details.pop('manufacturerName', '')
            listings_details.pop('manufacturerPartNumber', '')
            listings_details.pop('availabilityMessage', '')

            meta = r.pop('meta')
            meta.pop('category_url')
            meta.pop('csv_headers', '')
            meta.pop('filepath')

            hd = []

            hd += list(meta.keys())
            hd += [h for h in list(r.keys()) if 'Specs ' not in h]
            hd += [h for h in list(r.keys()) if 'Specs ' in h]
            hd += list(listings_details.keys())

            for h in hd:
                if h and h not in headers:
                    headers.append(h)

        return headers


# if __name__ == "__main__":
#     ConvertJlToCsvScript()
