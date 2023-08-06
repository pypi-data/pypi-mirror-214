from dataclasses import dataclass


@dataclass
class Sort(object):
    field: str
    order: str

    @staticmethod
    def asc(field):
        return Sort(field, "asc")

    @staticmethod
    def desc(field):
        return Sort(field, "desc")

    @staticmethod
    def parse(sort: str):
        if sort.startswith("-"):
            return Sort.desc(sort[1:])
        else:
            return Sort.asc(sort)

    def __str__(self):
        return f"{self.field}:{self.order}"


class UrlQueryFromFilters(object):
    @staticmethod
    def parse(filters: dict):
        exists_or_not_params = []
        params = {}
        for field_to_filter, operator_value_tuple in filters.items():
            operator = operator_value_tuple[0]
            filter_value = operator_value_tuple[1] if len(operator_value_tuple) > 1 else None
            if operator in ["=", "!=", "<", ">", ">="]:
                params[field_to_filter] = (operator, filter_value)
            elif operator == "exists":
                exists_or_not_params.append(field_to_filter)
            elif operator == "not_exists":
                exists_or_not_params.append(f"!{field_to_filter}")
            else:
                raise ValueError(f"Unsupported operator: {operator}")

        # Return the query string
        return "&".join([
            *[f"{key}{operator}{value}" for key, (operator, value) in params.items()]
            + exists_or_not_params
        ])
