def count_by_occurence(log, metric, data_dict):
    my_metric = log[metric]
    my_metric_in_data_dict = data_dict.get(my_metric)

    is_my_metric_in_data_dict = bool(my_metric_in_data_dict)

    if is_my_metric_in_data_dict:
        updated_my_metric = my_metric_in_data_dict + 1
        data_dict.update(
            {my_metric: updated_my_metric}
        )
    else:
        data_dict.update({
            my_metric: 1
        })
        
def show_top_metrics(message, dict_items):
    print(message)
    print("-----------------------")


    def get_second_value(item):
        return item[1]
    
    sorted_dict_items = sorted(dict_items.items(), key=get_second_value, reverse=True)

    for i,entry in enumerate(sorted_dict_items, start=1):
        if i <= 10:
            print(f'{i}. {entry[0]:<16} | {entry[1]}')

