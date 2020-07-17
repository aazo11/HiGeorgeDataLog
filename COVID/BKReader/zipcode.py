import pandas as pd


def process_data(zipc):
    finalzip = pd.DataFrame()
    finalzip['Total COVID Cases'] = zipc['COVID_CASE_COUNT']
    finalzip['Total COVID Deaths'] = zipc['COVID_DEATH_COUNT']
    finalzip['Positive test rate'] = zipc['PERCENT_POSITIVE']
    finalzip['Neighborhood'] = zipc['NEIGHBORHOOD_NAME']
    finalzip.index = zipc['MODIFIED_ZCTA']

    return finalzip


def get_updated_data(bk, di):
    ix = bk["Total COVID Cases"].idxmax()
    max_cases = bk.loc[ix]
    return {
        "smart_tiles": [
            {
                "figure": str(max_cases["Total COVID Cases"]),
                "subheader": "{} - {}".format(max_cases["Neighborhood"].split('/')[0], ix)
            }
        ]
    }
