from pprint import pprint

all_in_one_laptops_url_t = "https://www.insight.com/api/product-search/search?country=US&q=*%3A*&instockOnly=false&searchType=category&start={start_offset}&salesOrg=2400&lang=en_US&category=hardware%2Fcomputers%2Fdesktops%2Fall_in_one_computers&rows=100&userSegment=CES&tabType=products"
laser_drums_url_t = "https://www.insight.com/api/product-search/search?country=US&q=*%3A*&instockOnly=false&start={start_offset}&salesOrg=2400&lang=en_US&category=hardware%2Fprinters%2Fprinter_supplies_and_accessories%2Flaser_drums&rows=100&userSegment=CES&tabType=products"
printer_ribbons_url_t = "https://www.insight.com/api/product-search/search?country=US&q=*%3A*&instockOnly=false&start={start_offset}&salesOrg=2400&lang=en_US&category=hardware%2Fprinters%2Fprinter_supplies_and_accessories%2Fprinter_ribbons&rows=100&userSegment=CES%2CCES%2CCES&tabType=products"
barcode_printer_url_t = "https://www.insight.com/api/product-search/search?country=US&q=barcode+printer&instockOnly=false&start={start_offset}&salesOrg=2400&lang=en_US&rows=100&userSegment=CES&tabType=products"
barcode_scanner_url_t = "https://www.insight.com/api/product-search/search?country=US&q=barcode+scanner&instockOnly=false&selectedFacet=CategoryPath_en_US_ss_lowest_s%3A%22Barcode+Scanners%22&start={start_offset}&salesOrg=2400&lang=en_US&rows=100&userSegment=CES%2CCES%2CCES%2CCES%2CCES&tabType=products"

listings_meta = [
    {"category_url": all_in_one_laptops_url_t, "filepath": "All-in-One Computers_1.csv",
     "Project Category": "All in One – PC", "Product Category": "Desktop",
     "Insight Category": "All-in-One Computers"},

    {"category_url": laser_drums_url_t, "filepath": "Laser Drums_2.csv", "Project Category": "Alternative inks",
     "Product Category": "Alternative inks", "Insight Category": "Laser Drums"},

    {"category_url": printer_ribbons_url_t, "filepath": "Printer Ribbons_3.csv",
    "Project Category": "Alternative inks", "Product Category": "Alternative inks",
    "Insight Category": "Printer Ribbons"},

    {"category_url": barcode_printer_url_t, "filepath": "Barcode Printer_4.csv",
     "Project Category": "Barcode Printer", "Product Category": "Barcode Printer",
     "Insight Category": "Barcode Printer"},

    {"category_url": barcode_printer_url_t, "filepath": "Barcode Scanner_5.csv",
     "Project Category": "Barcode Scanner", "Product Category": "Barcode Scanner",
     "Insight Category": "Barcode Scanner"},
]
