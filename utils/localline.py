import pandas as pd

NAME_KEY = 'Customer Name'

EVIDENCE_OF_BOX_DELIVERY_NEEDED = {
    'regexes': [
        r'\$\d+\sbox',
        r'\$\d+\smembership'
    ],
    'string': [
        "$40 box", "$100/month", "$40 membership", "Box"
    ]
}

LOCALLINE_HEADER = "_,Order,Date,Order Status,Payment Status,Payment Method,Product,Internal Product ID,Quantity,Package Name,Product Subtotal,Product Sales Tax,Order Discount,Store Credit Applied,Fulfillment Fee,Fulfillment Tax,Total,Fulfillment Date,Fulfillment Type,Fulfillment Name,Fulfillment Address,Order Placed Time,Order Note,Backoffice Product Tags,Fulfillment Street Address,Fulfillment City,Fulfillment State,Fulfillment ZIP Code,Fulfillment Country".split(',')


# I really wish I could make custom pyjanitor functions :(
def _load_csv(args):
    return pd.read_csv(**args)

def _transform_data(df, args):
    return df.dropna(**args)

def load_csv(file_path):
    args = {
        'filepath_or_buffer': file_path,
        'header': None
    }
    return _load_csv(args)

def transform_data(df):
    args = {
        'axis': 'index',
        'how':'all'
    }
    return _transform_data(df, args)
    
def _extract_customers(df):
    # Create a helper column
    df['helper'] = (df[0] == 'Grand Total').shift().fillna(0).cumsum()

    # Each 'group_id' represents a different customer, so we can now group by this
    groups = df.groupby('helper')

    # Create an empty list to store our group dataframes
    group_dfs = []

    # Loop through the groups
    for name, group in groups:
        # Ignore the 'Grand Total' rows
        if group[0].iloc[0] != 'Grand Total':
            # Append the group (minus our helper column) to our list
            group_dfs.append(group.drop('helper', axis=1))

    return group_dfs
    
def extract_customers(df):
    return _extract_customers(df)

def delivery_products(a_customer):
    # I should probably use nested style instead of peer hierarchry
    # with underscore (_) to better make obvious the relationships 
    # and support nearby modifications of code
    def _delivery_products(a_customer, key='Product', key_index=6):
        product_series = a_customer.iloc[:,key_index]
        matched_rows = product_series == None # initialized with no matches

        for regex in EVIDENCE_OF_BOX_DELIVERY_NEEDED['regexes']:
            matched_rows = matched_rows | product_series.str.contains(
                regex,
                na=False, 
                regex=True)
        for a_string in EVIDENCE_OF_BOX_DELIVERY_NEEDED['string']:
            matched_rows = matched_rows | product_series.str.contains(
                a_string,
                na=False, 
                regex=False)

        return a_customer[matched_rows]
    
    key_index = LOCALLINE_HEADER.index('Product')
    
    return _delivery_products(a_customer, key_index=key_index)

def delivery_report(file_path):
    def _their_name(a_customer):
        first_possible = a_customer.iloc[0,0]
        second_possible = a_customer.iloc[1,0]

        if pd.isnull(first_possible) and second_possible:
            return second_possible
        elif not pd.isnull(first_possible) and first_possible:
            return first_possible
        else:
            raise ValueError

    def _delivery_report(their_name, products):
        products.loc[:, NAME_KEY] = their_name
        return products

    RENAME_COLUMNS = dict(
        zip(
            range(len(LOCALLINE_HEADER)),
            LOCALLINE_HEADER)
    )
    df = load_csv(file_path)
    customers = extract_customers(df=df)

    for a_customer in customers:
        their_name = _their_name(a_customer)
        products = delivery_products(a_customer)

        if not products.empty:
            products = products.copy()
            products.rename(columns=RENAME_COLUMNS, inplace=True)
            yield _delivery_report(their_name, products)
