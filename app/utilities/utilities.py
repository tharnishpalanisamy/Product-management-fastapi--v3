from exceptions import InvalidCategoryException

MARGIN = {
    'electronics' : 25 , 
    'stationary' : 20 , 
    'gift' : 24 , 
    'food' : 20 , 
    'clothes' : 35 , 
    'wearables' : 30
}

ALLOWED_COLS = {
    'product_id' , 'product_name' , 'cost_price' , 'margin' ,
    'selling_price' , 'sale_value' , 'profit_per_item' , 'expected_profit' , 
    'quantity' , 'stock_value' , 'category'
}

ALLOWED_SORT = {
    'ASC' , 'DESC'
}

def create_filters(filters:dict) : 
    new_filters = {} 

    for key in filters : 
        if filters[key] : 
            if key == 'category' and filters[key] not in MARGIN  :
                continue 
            if key == 'order_by' and filters[key] not in ALLOWED_COLS :
                raise InvalidCategoryException(
                            f"Invalid category. Choose from: {list(ALLOWED_COLS)}"
                        ) 
            if key == 'sort_by' and filters[key].upper() not in ALLOWED_SORT :
                 raise InvalidCategoryException(
                        f"Invalid category. Choose from: {list(ALLOWED_SORT)}"
                    ) 
            new_filters[key] = filters[key]   
        if filters['offset']  == 0 :
            new_filters['offset'] = 0 
    return new_filters
