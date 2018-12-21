def count_letters(word_string):
    """ See question description """

    word_list = word_string.split(" ")

    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    char = []
    for word in word_list:
        char = char + list(word)
        
    print('char list:', char)
    letter_count = {}
    for letter in ALPHABET:
        letter_count[letter] = char.count(letter)
    print('dict of letter count:',letter_count)
    
    max_count = 0
    for key in letter_count:
        if letter_count[key] > max_count:
            max_char, max_count = key, letter_count[key]

    return max_char, max_count



monty_quote = "listen strange women lying in ponds distributing swords is no basis for a system of government supreme executive power derives from a mandate from the masses not from some farcical aquatic ceremony"
    
print(count_letters(monty_quote))
