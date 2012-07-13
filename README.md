# Cooler Alphametic Solver - Thoughts On "Dive Into Python 3"

"Dive Into Python 3" is a fantastic book.  For instance, chapter 8 "Advanced Iterators" introduces a smart alphametic puzzle solver.  Unfortunately, it has a crashing bug (Google searching result on 13th Jul. 2012 implies that I'm the first one reporting this bug on Internet ;-).  Meanwhile, it can be cooler with following small improvements.

## Fixing Bug

At the beginning of solve(), it converts input string to upper case, which implies it also accepts lower case input string.

    words = re.findall('[A-Z]+', puzzle.upper())

However at the end of solve(), it assumes input string must be in upper case.  Otherwise, the following eval() would crash because of invalid equation.

    equation = puzzle.translate(dict(zip(characters, guess)))
    if eval(equation):

We can insert 'upper()' between 'puzzle' and 'translate' here.  But that seems duplicate.  So, my suggestion is that caller should make sure input string is always in upper case (line 40 in my revision).

## Removing Confusion

To be honest, I spent 5 minutes to figure out what following codes want to do.

    first_letters = {word[0] for word in words}
    n = len(first_letters)
    sorted_characters = ''.join(first_letters) + \
        ''.join(unique_characters - first_letters)
    characters = tuple(ord(c) for c in sorted_characters)

    ...

    zero = digits[0]

    ...

    if zero not in guess[:n]:

Eventually, those codes just want to make sure the leading digit for each word is not 0.  In my opinion, regular expression '(\D|^)0\d*' is more straight forward (line 23 and 27 in my revision).
