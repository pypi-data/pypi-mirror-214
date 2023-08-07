class DataProcessor:
    def filter_data(self, data, condition):
        filtered_data = [item for item in data if condition(item)]
        return filtered_data

    def sort_data(self, data, key):
        sorted_data = sorted(data, key=key)
        return sorted_data

    def transform_data(self, data, transformation):
        transformed_data = [transformation(item) for item in data]
        return transformed_data
