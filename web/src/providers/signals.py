import cities_light
#('CD', 'AO', 'CF','BI','UG','TZ','RW','SS','ZM','CG')
def filter_city_import(sender, items, **kwargs):
    if items[8] != 'CD':
        raise cities_light.InvalidItems()

cities_light.signals.city_items_pre_import.connect(filter_city_import)