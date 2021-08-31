from sql_handler import SqlContext


def create_species(name):
    """
    Adds a species to the species list with the given name
    Checks if the name is valid and unique
    :param str name: The name of the new species
    """


def read_species():
    """
    Reads the species list
    :param int is_active: Whether the list includes active or inactive rows
    :param dict search_by_column: Search string for given columns
        - str name: The name of the column
    :param int _id: The id of a specific species
    :param list ids: The ids of specific species
    :param str search: Search string for each column
    """


def update_species():
    """
    Updates a species with the given ID
    :param int _id: The id of the species to update
    :param dict new_values: The new values for the species
        - str name: The new name for the species
    """


def deactivate_species():
    """
    Deactivates a species with the given ID
    :param int _id: The id of the species to deactivate
    """


def activate_species():
    """
    Activates a species with the given ID
    :param int _id: The id of the species to activate
    """


def delete_species():
    """
    Deletes a species with the given ID
    :param int _id: The id of the species to delete
    """
