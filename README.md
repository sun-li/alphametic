# Cooler Alphametic Solver - Thoughts On "Dive Into Python 3"

"Dive Into Python 3" is a fantastic book.  For instance, chapter 8 "Advanced Iterators" introduces a smart alphametic puzzle solver.  Unfortunately, it has a crashing bug (Google searching result on 12th Jul. 2012 implies that I'm the first one reporting this bug on Internet ;-).  Meanwhile, it can be even cooler with following improvements.

## Fixing Bug

At the beginning of `solve()`, it converts input string to upper case, which implies it also accepts lower case input string.

    words = re.findall('[A-Z]+', puzzle.upper())

However at the end of `solve()`, it assumes input string must be in upper case.  Otherwise, the following `eval()` would crash because of invalid equation.

    equation = puzzle.translate(dict(zip(characters, guess)))
    if eval(equation):

We can insert `upper()` between `puzzle.` and `translate(` here.  But that seems duplicate.  So, my suggestion is that caller should make sure input string is always in upper case (line 40 in [my revision][0]).

## Removing Confusion

To be honest, I spent 5 minutes to figure out what following codes want to do.

    first_letters = {word[0] for word in words}
    n = len(first_letters)
    sorted_characters = ''.join(first_letters) + \
        ''.join(unique_characters - first_letters)
    characters = tuple(ord(c) for c in sorted_characters)

    ...

    if zero not in guess[:n]:

Finally, those codes just want to make sure the leading digit for each word is not 0.  In my opinion, a regular expression `'(\D|^)0\d*'` is more straight forward (line 23 and 27 in [my revision][0]).

Regular expression is clearer.  But, would it slow down the code significantly?  cProfiler answered no.

![profiler](https://github.com/sun-li/alphametic/raw/master/profile.png)

Surprisingly, the bottle neck actually is `eval()` which accounts for 60% time.  Meanwhile, `translate()` also accounts for 8%.  `re.search()` only accounts for 10%.

## Animating Progress

It takes around 40 seconds to calculate "SEND + MORE == MONEY" on my computer.  That is long enough to make people suspect the code is running into dead loop.  Therefore a command line based animated progress is added.  Probably you want to try [my alphametic.py][0] on your terminal.  That progress animation is cool.

On implementation side, this trick actually is simple.  Just insert `end='\r'` into `print()` (line 26 in [my revision][0]).  Meanwhile, do not forget to overwrite the progress update at the end of the function because `'\r'` only move cursor but do not delete anything.

The trade-off for this progress animation is performance.  It takes extra 20 seconds roughly for "SEND + MORE == MONEY" on my computer. But I believe that is worth in term of overall user experience (slower but more responsive).

## Extending Patterns

Thanks powerful `eval()`.  This alphametic solver actually can support `-, *, /, **` in addition to `+`.  So, you can play with "MONEY - MORE == SEND", too.

If you think about equation input (e.g. "MONEY - MORE == SEND") further, you may realize that essentially is an abstract pattern, which is not necessary in alphabets!  Equation "A * B == C" should be as same as equation "2 * 3 == 6", where both "A" and "2" represent same operand.  With a tiny change (line 13 in [my revision][0]), pattern in digits is supported easily.  So, you could check whether there is any solution for pattern "11 * 11 == 121".



[0]: https://github.com/sun-li/alphametic/blob/master/alphametic.py "alphametic.py"
