from os import listdir
from os.path import isfile, join
import adagenes as ag


def recognize_column_types(list):
    column_type = None
    consistent_type = None

    for value in list:

        if value is None:
            continue
        elif value == "":
            continue

        try:
            val = int(value)
            column_type = 'integer'
            continue
        except:
            pass

        try:
            val = float(value)
            column_type = 'float'
            continue
        except:
            pass

        column_type = 'string'

        if column_type is not None:
            if column_type != consistent_type:
                if (column_type=="integer") and (consistent_type == "float"):
                    column_type = "float"
                elif ((column_type == "integer") or (column_type == "float")) and (consistent_type == "string"):
                    column_type = "string"

        consistent_type = column_type

    return column_type

def load_file(qid, data_dir, start_row=None, end_row=None):
    """

    :param qid:
    :param data_dir:
    :return:
    """
    data_dir = data_dir + "/" + qid


    files = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]
    infile = data_dir + "/" + files[0]
    print(infile)

    bframe = ag.read_file(infile, start_row=start_row, end_row=end_row)
    print(bframe.data)

    return bframe


def get_column_defs(output_format):
    pass


def analyze_uploaded_file(qid, data_dir = None, start_row=None, end_row=None, genome_version="hg38",
                          output_format="vcf"):
    """

    :param qid:
    :param data_dir:
    :param genome_version:
    :param output_format:
    :return:
    """

    # load saved file

    bframe = load_file(qid, data_dir, start_row=start_row, end_row=end_row)
    max_rows = bframe.max_variants

    column_defs = []
    table_data = []

    if output_format == "vcf":
        table_data = []

        for var in bframe.data.keys():
            # base VCF columns
            dc = {
                'chrom': bframe.data[var]["variant_data"]["CHROM"],
                'pos': bframe.data[var]["variant_data"]["POS"],
                'ref': bframe.data[var]["variant_data"]["REF"],
                'alt': bframe.data[var]["variant_data"]["ALT"],
            }
            column_defs = [
                {'headerName': 'CHROM', 'field': 'chrom', 'filter': "agTextColumnFilter", 'floatingFilter': 'true'},
                {'headerName': 'POS', 'field': 'pos', 'filter': "agNumberColumnFilter", 'floatingFilter': 'true'},
                {'headerName': 'REF', 'field': 'ref', 'filter': "agTextColumnFilter", 'floatingFilter': 'true'},
                {'headerName': 'ALT', 'field': 'alt', 'filter': "agTextColumnFilter", 'floatingFilter': 'true'},
            ]

            # Preexisting features
            #print(bframe.data)
            info_features = bframe.data[var]["info_features"].keys()
            #print(bframe.data[var]["info_features"])
            for inf in info_features:
                column_type = recognize_column_types([bframe.data[var]["info_features"][inf]])
                if column_type == "float":
                    filter_type = "agNumberColumnFilter"
                elif column_type == "integer":
                    filter_type = "agNumberColumnFilter"
                else:
                    filter_type = "agTextColumnFilter"

                dc[inf.lower()] = bframe.data[var]["info_features"][inf]

                inf_column = { 'headerName': inf, 'field': inf.lower(), 'filter': filter_type, 'floatingFilter': 'true' }
                column_defs.append(inf_column)

            table_data.append(dc)


    else:

        table_data = [
            {'id': 1, 'name': 'John Doe', 'age': 28, 'country': 'USA'},
            {'id': 2, 'name': 'Jane Smith', 'age': 34, 'country': 'Canada'},
            {'id': 3, 'name': 'Sam Green', 'age': 45, 'country': 'UK'},
        ]

        column_defs = [
            {'headerName': 'ID', 'field': 'id'},
            {'headerName': 'Name', 'field': 'name'},
            {'headerName': 'Age', 'field': 'age'},
            {'headerName': 'Country', 'field': 'country'},
        ]


    return column_defs, table_data, max_rows

def analyze_search():

    column_defs = []
    table_data = []

    return column_defs, table_data

