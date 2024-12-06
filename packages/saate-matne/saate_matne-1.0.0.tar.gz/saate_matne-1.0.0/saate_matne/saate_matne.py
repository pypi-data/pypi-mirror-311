from datetime import datetime
from colorama import Fore, Back, Style, init

# Reserved for the nex Version:
# GOYA_TABLE_FA = [
#     "یک", "دو", "سه", "چهار", "پنج", "شش", "هفت", "هشت", "نه", "ده", 
#     "یازده", "دوازده", "سیزده", "چهارده", "پانزده", "شانزده", "هفده", "هجده", "نوزده", 
#     "بیست", "بیست و یک", "بیست و دو", "بیست و سه", "بیست و چهار", "بیست و پنج", "بیست و شش", 
#     "بیست و هفت", "بیست و هشت", "بیست و نه", "سی", "سی و یک", "سی و دو", "سی و سه", 
#     "سی و چهار", "سی و پنج", "سی و شش", "سی و هفت", "سی و هشت", "سی و نه", "چهل", 
#     "چهل و یک", "چهل و دو", "چهل و سه", "چهل و چهار", "چهل و پنج", "چهل و شش", "چهل و هفت", 
#     "چهل و هشت", "چهل و نه", "پنجاه", "پنجاه و یک", "پنجاه و دو", "پنجاه و سه", 
#     "پنجاه و چهار", "پنجاه و پنج", "پنجاه و شش", "پنجاه و هفت", "پنجاه و هشت", "پنجاه و نه"
# ]

GOYA_TABLE_EN = [
    "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
    "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen",
    "Twenty", "Twenty-One", "Twenty-Two", "Twenty-Three", "Twenty-Four", "Twenty-Five", "Twenty-Six",
    "Twenty-Seven", "Twenty-Eight", "Twenty-Nine", "Thirty", "Thirty-One", "Thirty-Two", "Thirty-Three",
    "Thirty-Four", "Thirty-Five", "Thirty-Six", "Thirty-Seven", "Thirty-Eight", "Thirty-Nine", "Forty",
    "Forty-One", "Forty-Two", "Forty-Three", "Forty-Four", "Forty-Five", "Forty-Six", "Forty-Seven",
    "Forty-Eight", "Forty-Nine", "Fifty", "Fifty-One", "Fifty-Two", "Fifty-Three", "Fifty-Four",
    "Fifty-Five", "Fifty-Six", "Fifty-Seven", "Fifty-Eight", "Fifty-Nine", "and", "Hour", "Minute", "Before noon", "After noon"
]

GOYA_TABLE_FA = [
    "Yak", "Do", "Si", "Chahar", "Panj", "Shash", "Haft", "Hasht", "Noh", "Dah", 
    "Yazdah", "Dovazdah", "Sizdah", "Chahardah", "Panzdah", "Shanzdah", "Havdah", 
    "Hezhdah", "Noozdah", "Best", "Best-o-Yek", "Best-o-Do", "Best-o-Si", "Best-o-Chahar", 
    "Best-o-Panj", "Best-o-Shash", "Best-o-Haft", "Best-o-Hasht", "Best-o-Noh", "See", 
    "Se-o-Yek", "Se-o-Do", "Se-o-Si", "Se-o-Chahar", "Se-o-Panj", "Se-o-Shash", 
    "Se-o-Haft", "Se-o-Hasht", "Se-o-Noh", "Chehel", "Chehel-o-Yek", "Chehel-o-Do", 
    "Chehel-o-Si", "Chehel-o-Chahar", "Chehel-o-Panj", "Chehel-o-Shash", "Chehel-o-Haft", 
    "Chehel-o-Hasht", "Chehel-o-Noh", "Panjah", "Panjah-o-Yek", "Panjah-o-Do", "Panjah-o-Si", 
    "Panjah-o-Chahar", "Panjah-o-Panj", "Panjah-o-Shash", "Panjah-o-Haft", "Panjah-o-Hasht", 
    "Panjah-o-Noh", "wa", "Bajah", "Daqeqa", "Pish Az Chasht", "Bad Az Chasht"
    ]



def matn(lang, theme):

    """
    Display the current time in a formatted way based on language and theme.

    Parameters:
    lang (str): The language for numbers ("en" or "fa").
    theme (str): The theme of the output ("day" or "night").

    Returns:
    str: Formatted time string.
    """
    
    try:
        now = datetime.now()
        init()

        am_pm = ''
        tbl = ''
        
        if lang == 'en':
            tbl = GOYA_TABLE_EN
            am_pm = tbl[62] if now.hour < 12 else tbl[63]
        elif lang == 'fa':
            tbl = GOYA_TABLE_FA
            am_pm = tbl[62] if now.hour < 12 else tbl[63]
        else:
            tbl = []
        
        

        hr = now.hour % 12
        min = now.minute
        sec = now.second

        time = ''

        if theme == "day":
            if lang == 'en':
                time = Fore.WHITE + 'Time is: ' + Back.BLUE + tbl[hr -1] + " " + tbl[60]  + Back.RESET + " " + tbl[59] + " " + Back.BLUE + tbl[min -1] + " " + tbl[61] + Back.RESET + " " + am_pm + Fore.RESET
            elif lang == 'fa':
                time = Fore.WHITE + 'Zamaan Ast: ' + Back.BLUE + tbl[hr -1] + " " + tbl[60]  + Back.RESET + " " + tbl[59] + " " + Back.BLUE + tbl[min -1] + " " + tbl[61] + Back.RESET + " " + am_pm + Fore.RESET

        elif theme == "night":
            if lang == 'en':
                time = Fore.YELLOW + 'Time is: ' + Back.RED + tbl[hr -1] + " " + tbl[60]  + Back.RESET + " " + tbl[59] + " " + Back.RED + tbl[min -1] + " " + tbl[61] + Back.RESET + " " + am_pm + Fore.RESET
            elif lang == 'fa':
                time = Fore.YELLOW + 'Zamaan Ast: ' + Back.RED + tbl[hr -1] + " " + tbl[60]  + Back.RESET + " " + tbl[59] + " " + Back.RED + tbl[min -1] + " " + tbl[61] + Back.RESET + " " + am_pm + Fore.RESET
        else:
            return Fore.RED + "Please Provide a correct Theme as " + Back.LIGHTWHITE_EX + "DAY" + Back.RESET + " or " + Back.LIGHTWHITE_EX + "NIGHT" + Back.RESET + Fore.RESET
        return time
    
    
    except IndexError as e:
        if "list index out of range" in str(e):
            return "No Language Found"
        elif "string index out of range" in str(e):
            return "The Selected Language Data is Empty"
        # print(e)

# print(goya('fa', 'night'))