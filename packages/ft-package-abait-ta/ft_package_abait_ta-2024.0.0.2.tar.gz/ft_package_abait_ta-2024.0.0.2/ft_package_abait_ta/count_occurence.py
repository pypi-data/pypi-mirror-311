def count_occurence_in_list(input_list: list, search_for: any) -> int:
    """
    This Function is used to count
    how many Occurence of each elemnts on a list
    * Function only accept list ==> type(input_list) == <class 'list'>
    @return
        - Python dictionary where each element containe
         symbole : the caractere
         occur   : how mush occurence for this caractere
    """
    try:
        occurence_asDict = [{
            'symbole': elem,
            'occur': input_list.count(elem)
            } for elem in input_list]

        return occurence_asDict
    except Exception as e:
        print(f'raised  : {e}')
