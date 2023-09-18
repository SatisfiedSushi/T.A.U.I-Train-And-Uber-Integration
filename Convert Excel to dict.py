from pandas import *
import pprint
xls = ExcelFile('CTA train stpids.xlsx')
df = xls.parse(xls.sheet_names[0])
pprint.pprint(df.to_dict())