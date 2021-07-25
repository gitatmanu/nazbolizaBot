import random

names = [
"stalin",
"patriota",
"ibero",
"camarada",
"rojo",
"proletario",
"octubre",
"bolchevique",
"tankie",
"basado",
"soldado",
"1917",
"obrero",
"socialismo",
"1953",
"jacobino",
"hoxhaista"
]
flags = ["🇪🇸", "🇮🇷", "🇵🇸", "🇱🇦", "🇰🇵", "🇻🇳", "🇨🇺"]
symbols = ["⚒️","☭", "#SPEXIT"]


def generate_nazbol_name():    
    name = get_name()
    flags = get_flags()

    full_name = name + " "

    active_symbol = random.randint(0, 1)
    if active_symbol:
        first_position_symbol = random.randint(0, 1)
        if first_position_symbol:
            full_name += symbols[random.randint(0, len(symbols) - 1)]
            full_name += flags
        else:
            full_name += flags
            full_name += symbols[random.randint(0, len(symbols) - 1)]
    else:
        full_name += flags

    return full_name



def get_name():
    first_name = names[random.randint(0, len(names) - 1)]
    second_name = names[random.randint(0, len(names) - 1)]

    while first_name == second_name:
        first_name = names[random.randint(0, len(names) - 1)]
        second_name = names[random.randint(0, len(names) - 1)]

    return first_name.capitalize() + second_name.capitalize()


def get_flags():
    flag_string = ""

    for i in range(random.randint(1, len(flags) - 1)):
        flag = flags[random.randint(0, len(flags) - 1)]

        if flag not in flag_string:
            flag_string += flag

    return flag_string