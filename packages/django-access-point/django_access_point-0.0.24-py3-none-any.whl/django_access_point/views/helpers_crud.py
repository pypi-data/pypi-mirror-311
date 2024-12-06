import json

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Prefetch, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django_access_point.models.custom_field import CUSTOM_FIELD_STATUS, CUSTOM_FIELD_TYPE

custom_field_values_related_name = "custom_field_values"


def _validate_custom_fields_attributes(custom_field_model, custom_field_value_model):
    """
    Validates that if `custom_field_model` is defined, `custom_field_value_model` must also be defined.

    :param custom_field_model - Custom Field model name
    :param custom_field_value_model - Custom Field Value model name
    """
    if custom_field_model and not custom_field_value_model:
        raise ImproperlyConfigured(
            "Django Access Point: 'custom_field_value_model' must be defined if 'custom_field_model' is set."
        )
    elif custom_field_value_model and not custom_field_model:
        raise ImproperlyConfigured(
            "Django Access Point: 'custom_field_model' must be defined if 'custom_field_value_model' is set."
        )


def _get_custom_field_queryset(custom_field_model):
    """
    Get active custom fields queryset.

    :param custom_field_model - Custom Field model name
    """
    return custom_field_model.objects.filter(status=CUSTOM_FIELD_STATUS[1][0]).order_by("field_order")


def _prefetch_custom_field_values(
    queryset,
    custom_field_queryset,
    custom_field_value_model,
):
    """
    Prefetch related custom field values for the given queryset.

    :param queryset - CRUD queryset
    :param custom_field_queryset - Custom Field queryset
    :param custom_field_value_model - Custom Field Value model name
    """
    active_custom_fields = custom_field_queryset

    return queryset.prefetch_related(
        Prefetch(
            custom_field_values_related_name,
            queryset=custom_field_value_model.objects.filter(
                custom_field__in=active_custom_fields
            ).only("id", "custom_field", "text_field"),
        )
    )


def _get_ordering_params(request):
    """
    Get ordering parameters from request.

    :param request - The request object, typically containing data sent by the client, including query parameters, body content, and other metadata
    """
    order_by = request.query_params.get("order_by", "created_at")
    direction = request.query_params.get("direction", "desc")

    # Validate order_by field
    if order_by not in ["created_at", "updated_at"]:
        raise ValueError(
            "Invalid 'order_by' field. Only 'created_at' or 'updated_at' are allowed."
        )

    # Validate direction
    if direction not in ["asc", "desc"]:
        raise ValueError("Invalid 'direction'. Only 'asc' or 'desc' are allowed.")

    # Apply ordering direction
    return f"-{order_by}" if direction == "desc" else order_by


def _get_search_filter(request, list_search_fields, custom_field_value_model = None, is_custom_field_enabled = False):
    """
    Generate search filter based on query parameters.

    :param request - The request object, typically containing data sent by the client, including query parameters, body content, and other metadata
    :param list_search_fields - A list of CRUD model field names that should be used for search filtering
    :param custom_field_value_model - Custom Field Value model name
    :param is_custom_field_enabled
    """
    search_term = request.query_params.get("search", "")
    filter_term = request.query_params.get("filter", "{}")

    if not search_term and not filter_term:
        return Q()  # Empty filter if no search & filter term is provided

    search_filter = Q()

    if search_term:
        # Search
        search_filter = apply_search(search_filter,
                                     search_term,
                                     list_search_fields,
                                     is_custom_field_enabled,
                                     custom_field_value_model)

    # if filter_term:
    #     # Filter
    #     search_filter = apply_filter(search_filter,
    #                                  request,
    #                                  is_custom_field_enabled,
    #                                  custom_field_value_model)

    return search_filter

def apply_search(search_filter_queryset, search_term, list_search_fields, is_custom_field_enabled, custom_field_value_model ):
    """
    Apply Search

    :param search_filter_queryset
    :param search_term
    :param list_search_fields
    :param is_custom_field_enabled
    :param custom_field_value_model
    """
    for field in list_search_fields:
        # Regular model field search
        search_filter_queryset |= Q(**{f"{field}__icontains": search_term})

    if is_custom_field_enabled:
        custom_field_value_subquery = (custom_field_value_model.objects.
                                       filter(text_field__icontains=search_term).values('submission'))

        search_filter_queryset |= Q(id__in=custom_field_value_subquery)

    return search_filter_queryset


def apply_filter(search_filter_queryset, request, is_custom_field_enabled,
                 custom_field_value_model):
    """
    Apply Filter

    :param search_filter_queryset
    :param request
    :param is_custom_field_enabled
    :param custom_field_value_model
    """
    filters = {}

    # Retrieve filters from headers
    for header, value in request.headers.items():
        # On headers should pass like,
            # Filter-Name: john, Filter-Custom_Field_12: test
            # Combined-Filter-12&13|14|15&16: alpha
        if header.startswith("Filter-"):
            # Remove the "Filter-" prefix from the header to get the field name
            field = header.replace("Filter-", "").lower()
            filters[field] = value

        if header.startswith("Combined-Filter-"):
            field_combination = header.replace("Combined-Filter-", "").lower() # On headers should pass like, Combined-Filter-Name: john
            combined_filters = parse_combined_filter(field_combination, value)
            # Apply combined filters to the queryset
            search_filter_queryset &= combined_filters


    if filters:
        for field, value in filters.items():
            if is_custom_field_enabled and field.startswith("custom_field_"):
                # Filter based on custom field values
                custom_field_id = field.replace("custom_field_", "")  # Extract the custom field ID
                search_filter_queryset &= Q(
                    id__in=custom_field_value_model.objects.filter(
                        custom_field_id=custom_field_id, text_field__icontains=value
                    ).values("submission")
                )
            else:
                # Regular model field filtering
                search_filter_queryset &= Q(**{f"{field}__icontains": value})

    return search_filter_queryset


def parse_combined_filter(field_combination, value):
    """
    Parse the combined filter and return the corresponding Q object for query filtering.

    :param field_combination: The field names involved in the combined filter.
    :param value: The filter value to compare with.
    :return: Q object representing the combined condition.
    """
    # Split the field_combination into segments, handling both `|` and `&`
    or_segments = field_combination.split('|')

    q_objects = []

    for segment in or_segments:
        # Split segment by `&` for AND logic
        and_conditions = segment.split('&')
        and_q_objects = []

        for field in and_conditions:
            # Create a Q object for each field with the given value
            and_q_objects.append(Q(**{f"{field}__icontains": value}))

        # Combine all fields in this AND segment
        combined_and_q = and_q_objects.pop(0)
        for q in and_q_objects:
            combined_and_q &= q

        q_objects.append(combined_and_q)

    # Combine all AND segments using OR logic
    final_q = q_objects.pop(0)
    for q in q_objects:
        final_q |= q

    return final_q

def _get_pagination(request, queryset):
    """
    Handle pagination logic and return paginated data.

    :param request - The request object
    :param queryset - The queryset to be paginated
    """
    page = request.query_params.get("page", 1)
    page_size = request.query_params.get("page_size", 10)

    try:
        page = int(page)
        page_size = int(page_size)
    except ValueError:
        raise ValueError("Invalid 'page' or 'page_size'. They must be integers.")

    paginator = Paginator(queryset, page_size)
    try:
        return paginator.get_page(page)
    except (EmptyPage, PageNotAnInteger):
        raise ValueError("Invalid page number or page size. Ensure the page is valid.")


def _format_custom_fields(custom_field_queryset):
    """
    Format custom fields.

    :param custom_field_queryset - Custom Field queryset
    """
    formatted_custom_fields = {}

    if custom_field_queryset:
        for custom_field in custom_field_queryset:
            formatted_custom_fields[custom_field.id] = custom_field.label

    return formatted_custom_fields


def _prepare_data_rows(page_obj, list_fields_to_use, active_custom_fields):
    """
    Prepare the data rows for the list view response.

    :param page_obj
    :param list_fields_to_use - A list of CRUD model field names that should be used on list response.
    :param active_custom_fields - Active Custom Fields
    """
    data = []
    for obj in page_obj.object_list:
        formatted_custom_field_submitted_values = {}
        if active_custom_fields:
            if hasattr(obj, custom_field_values_related_name):
                custom_field_submitted_values = getattr(obj, custom_field_values_related_name).all()
                formatted_custom_field_submitted_values = _format_custom_field_submitted_values(custom_field_submitted_values)

        # CRUD submitted data
        row = [getattr(obj, field, "") for field in list_fields_to_use]

        # Custom Field submitted data
        if active_custom_fields:
            for custom_field in active_custom_fields:
                row.append(formatted_custom_field_submitted_values.get(custom_field, ""))

        data.append(row)

    return data


def _format_custom_field_submitted_values(custom_field_submitted_values):
    """
    Format custom field values based on field type.

    :param custom_field_submitted_values
    """
    formatted_values = {}
    for submitted_value in custom_field_submitted_values:
        field_type = submitted_value.custom_field.field_type
        if field_type == CUSTOM_FIELD_TYPE[0][0]:  # Text field
            formatted_values[submitted_value.custom_field.id] = submitted_value.text_field
        elif field_type == CUSTOM_FIELD_TYPE[1][0]:  # Date field
            formatted_values[submitted_value.custom_field.id] = submitted_value.text_field.strftime("%Y-%m-%d")
        else:
            # Other field types
            formatted_values[submitted_value.custom_field.id] = submitted_value.text_field

    return formatted_values
