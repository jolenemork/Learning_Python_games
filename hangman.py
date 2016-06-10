# Problem Set 2
# Name: Anna Jolene Mork
# Collaborators: None
# Time spent: 5 hrs

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"

"""
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
"""
def load_words():
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist


"""
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
"""
def choose_word(wordlist):
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()

'''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), what letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
'''
def is_word_guessed(secret_word, letters_guessed):
    store_booleans = ()   #initialize a tuple 
    for i in range(len(secret_word)): #check all the letters of secret_word to see if they have been guessed
        store_booleans = store_booleans + (secret_word[i] in letters_guessed,) #add booleans to the tuple store_booleans
    if False in store_booleans: # word has not been guessed if there is a single false
        return False
    else:
        return True
        



'''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), what letters have been guessed so far
    returns: string, comprised of letters and asterisks (*) that represents
      what letters in secretWord have been guessed so far.
'''
def get_guessed_word(secret_word, letters_guessed):
    stored_output = [] #initialize a list to store position of letters from letters_guessed that match secret_word
    for i in range(len(secret_word)):
        if secret_word[i] in letters_guessed:
            stored_output.append(secret_word[i])
            # if the secret_word contains a letter from letters_guessed, store it in position i of stored_output
        else:
            stored_output.append('*')
            # if secret_word has a letter that has not been guessed, mark it with a *
        i+=1
    
    joined_list = "'"+"".join(stored_output) + "'"
        
    return joined_list
 

'''
    letters_guessed: list (of letters), what letters have been guessed so far
    returns: string (of letters), comprised of letters that represents what letters have not
      yet been guessed.
'''
def get_available_letters(letters_guessed):
    import string    
    totLetters = list(string.ascii_lowercase)
    
    #remove all the letters from totLetters that have been guessed
    for i in range(len(letters_guessed)):
        totLetters.remove(letters_guessed[i])
        i+=1
    
    return ''.join(totLetters) #return a joined string for totLetters (not a list)
        
        
'''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Ask the user to supply one guess (i.e. letter) per round. 
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
'''
#define a function that knows the previous letters guessed and the secret word, asks the user for a new
#letter, determines if the letter is in the word, changes the number of remaining guesses, and
#appends the new letter to letters_guessed
def turn(guesses_remaining, secret_word, letters_guessed):
    print 'You have', guesses_remaining, 'guesses left'
    print 'Available letters: ', get_available_letters(letters_guessed)
    
    #get user guess for the letter
    guess = raw_input('Please guess a letter: ')
    
    #define vowels for -2 guesses
    vowels = ['a','e','i','o','u']        
    
    linebreak = '--------------------'
    #determine if the guess has been guessed already and whether is in secret_word
    if guess in letters_guessed: #check for a repeated guess
        print 'Oops! You have already guessed that letter: ', get_guessed_word(secret_word,letters_guessed)
        print linebreak            
        guesses_remaining -=1     #decrement guesses by 1 for already guessed letter       
        
    elif guess in secret_word: #check if guess is in the word
        letters_guessed.append(guess)
        print 'Good guess: ', get_guessed_word(secret_word,letters_guessed)
        print linebreak
        # do not decrement guesses if the guess is in the word
        
    else: # if guess is not repeated and not in the secret_word, decrement guesses_remaining
        letters_guessed.append(guess)        
        print 'Oops! That letter is not in my word: ', get_guessed_word(secret_word,letters_guessed)
        print linebreak            
                    
        if guess in vowels:
            guesses_remaining = guesses_remaining - 2
        else:
            guesses_remaining = guesses_remaining - 1
            
    
    return (guesses_remaining, letters_guessed)



def hangman(secret_word):
    #print welcome script
    print 'Welcome to the game Hangman!'
    print 'I am thinking of a word that is', len(secret_word), 'letters long.'
    linebreak = '--------------------'
    print linebreak
    #initialize some variables/strings that will be used in function
    guesses_remaining = 6
    letters_guessed = []

# use a while loop to run the function "turn" until the guesses_remaining = 0
    while guesses_remaining > 0:
        x = turn(guesses_remaining, secret_word, letters_guessed)
        guesses_remaining = x[0]
        letters_guessed = x[1]
 # determine if this guess completes the word to break the while loop
        if is_word_guessed(secret_word,letters_guessed) == True:
            print 'Congratulations, you won!'              
            break        
              
    #if while loop ends and the word is not guessed, print fail message
    if is_word_guessed(secret_word, letters_guessed) == False:
        print 'Sorry, you ran out of guesses. The word was: ', secret_word
    
    




# When you've completed your hangman function, uncomment these two lines
# and run this file to test! (hint: you might want to pick your own
# secret_word while you're testing)

#secret_word = choose_word(wordlist).lower()
#hangman(secret_word)


# -----------------------------------


'''
    my_word: string with * characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        *; and my_word and other_word are of the same length;
        False otherwise: 
'''
def match_with_gaps(my_word, other_word):
    
    if len(my_word) != len(other_word): #check for unequal word lengths
        return False    
    else: #if words are equal lengths, start checking letters
        for i in range(len(my_word)):
            if my_word[i] == other_word[i] or my_word[i] == '*':
                i +=1
            else:
                return False
    return True

'''
    my_word: string with * characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
'''
def show_possible_matches(my_word):
    word_matches = [] #initilize list of matching words
    
    for x in wordlist: #add words to word_matches if they have the right letters and right number of letters
        if match_with_gaps(my_word, x) == True:
            word_matches.append(x)
    
    return " ".join(word_matches) #return a joined list of words
    

'''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Ask the user to supply one guess (i.e. letter) per round.
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      match the current match for the secret word
    
    Follows the other limitations detailed in the problem write-up.
'''
# the function turn_with_hints defines the basic actions of a turn (input letter,
# check if letter is in word, decrement number of guesses remaining if necessary) but
# turn_with_hints also includes an elif statement to address the case when a '*' is guessed
def turn_with_hints(guesses_remaining, secret_word, letters_guessed):
    print 'You have', guesses_remaining, 'guesses left'
    print 'Available letters: ', get_available_letters(letters_guessed)
    
    #get user guess for the letter
    guess = raw_input('Please guess a letter: ')
    
    #define vowels for -2 guesses
    vowels = ['a','e','i','o','u']        
    
    linebreak = '--------------------'
    #determine if the guess has been guessed already and whether is in secret_word
    if guess in letters_guessed: #check for a repeated guess
        print 'Oops! You have already guessed that letter: ', get_guessed_word(secret_word,letters_guessed)
        print linebreak            
        guesses_remaining -=1     #decrement guesses by 1 for already guessed letter       
        
    elif guess in secret_word: #check if guess is in the word
        letters_guessed.append(guess)
        print 'Good guess: ', get_guessed_word(secret_word,letters_guessed)
        print linebreak
        # do not decrement guesses if the guess is in the word
    elif guess == '*':
        x = get_guessed_word(secret_word, letters_guessed)        
        print 'Possible word matches are: \n ', show_possible_matches(x[1:-1])  #have to remove quotes around x to make work  
        print linebreak
        #do not decrement guesses if guess was '*'
        
    else: # if guess is not repeated and not in the secret_word, decrement guesses_remaining
        letters_guessed.append(guess)        
        print 'Oops! That letter is not in my word: ', get_guessed_word(secret_word,letters_guessed)
        print linebreak            
                    
        if guess in vowels:
            guesses_remaining = guesses_remaining - 1
        else:
            guesses_remaining = guesses_remaining - 1
            
    
    return (guesses_remaining, letters_guessed)



def hangman_with_hints(secret_word):
     #print welcome script
    print 'Welcome to the game Hangman!'
    print 'I am thinking of a word that is', len(secret_word), 'letters long.'
    linebreak = '--------------------'
    print linebreak
    #initialize some variables/strings that will be used in function
    guesses_remaining = 6
    letters_guessed = []

    # use a while loop to run the function "turn" until the guesses_remaining = 0
    while guesses_remaining > 0:
        x = turn_with_hints(guesses_remaining, secret_word, letters_guessed)
        guesses_remaining = x[0]
        letters_guessed = x[1]
        # determine if this guess completes the word to break the while loop
        if is_word_guessed(secret_word,letters_guessed) == True:
            print 'Congratulations, you won!'              
            break        
              
    #if while loop ends and the word is not guessed, print fail message
    if is_word_guessed(secret_word, letters_guessed) == False:
        print 'Sorry, you ran out of guesses. The word was: ', secret_word



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.

secret_word = choose_word(wordlist).lower()
hangman_with_hints(secret_word)
