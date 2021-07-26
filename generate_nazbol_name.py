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
"hoxhaista",
"socialista",
"nacional",
"patriotismo",
"guardia",
]
flags = ["🇪🇸", "🇮🇷", "🇵🇸", "🇱🇦", "🇰🇵", "🇻🇳", "🇨🇺"]
symbols = ["⚒️","☭", "#SPEXIT", "FO", "(RC)"]


def generate_nazbol_name():    
    full_name = get_name() + ' ' + get_decorators()

    return full_name


def get_name():
    first_name = names[random.randint(0, len(names) - 1)]
    second_name = names[random.randint(0, len(names) - 1)]

    while first_name == second_name:
        first_name = names[random.randint(0, len(names) - 1)]
        second_name = names[random.randint(0, len(names) - 1)]

    return first_name.capitalize() + second_name.capitalize() 


def get_flags():
    flag_str = ""

    for i in range(random.randint(1, len(flags) - 1)):
        flag = flags[random.randint(0, len(flags) - 1)]

        if flag not in flag_str:
            flag_str += flag

    return flag_str


def get_decorators():
    decorators = ''
    decorator = symbols[random.randint(0, len(symbols) - 1)]
    flags_str = get_flags()

    active_symbol = random.randint(0, 1)
    if active_symbol:
        first_position_symbol = random.randint(0, 1)
        if first_position_symbol:
            decorators += flags_str + decorator
        else:
            decorators += decorator + flags_str
    else:
        decorators += flags_str

    return decorators