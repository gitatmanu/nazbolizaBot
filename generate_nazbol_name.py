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
"hoxhista"
]
flags = ["🇪🇸", "🇮🇷", "🇵🇸", "🇱🇦", "🇰🇵", "🇻🇳", "🇨🇺"]
symbols = ["⚒️","☭", "#SPEXIT"]

def generate_nazbol_name():    
    import random

    first_position_symbol = random.randint(0, 1)
    active_symbol = random.randint(0, 1)
    flag_number = random.randint(1, len(flags) - 1)
    first_name = names[random.randint(0, len(names) - 1)]
    second_name = names[random.randint(0, len(names) - 1)]

    while first_name == second_name:
        first_name = names[random.randint(0, len(names) - 1)]
        second_name = names[random.randint(0, len(names) - 1)]

    flag_string = ""
    for i in range(flag_number):
        flag = flags[random.randint(0, len(flags) - 1)]

        if flag not in flag_string:
            flag_string += flag

    message = first_name.capitalize() + second_name.capitalize() + " "

    if active_symbol:
        if first_position_symbol:
            message += symbols[random.randint(0, len(symbols) - 1)]
            message += flag_string
        else:
            message += flag_string
            message += symbols[random.randint(0, len(symbols) - 1)]
    else:
        message += flag_string

    return message