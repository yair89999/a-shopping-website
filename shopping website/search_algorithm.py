
def split_list(lst, n):
    # split a list into _ lists
    new_list = []
    for i in range(0, len(lst), n):
        new_list.append(lst[i:i + n])
    return new_list

def get_results_algorithm(dict2,searched): # movies=dict, searched=string
    using_list = sorted([name for name in dict2]) # putting every movie_name in a list because its easier to search like this
    resume = True
    while resume == True:
        print("start list:",using_list)
        index = (len(using_list)-1)//2
        center = using_list[index]
        if center < searched: # del left
            quarter = using_list[len(using_list)//4]
            if searched in quarter:
                done = True
            else:
                using_list = using_list[index:]
        elif center > searched: # del right
            quarter = using_list[len(using_list)//4*3]
            if searched in quarter:
                done = True
            else:
                using_list = using_list[:index+1]

        if len(using_list) <= 200 or done == True:
            num = 0
            while num < 5:
                for option in using_list:
                    if not searched in option:
                        using_list.remove(option)
                num += 1
            break

    final_list = split_list(using_list,4) # split the final list into multiplay lists in the size of 4
    return final_list