def calculate_percent_change(area):
    percent_change = ((area['first_year_sum_events']['sum_events'] - area['last_year_sum_events']['sum_events']) /
                             area['first_year_sum_events']['sum_events']) * 100
    return round(percent_change, 2)