"""Functions for the generation of pseudo-random names."""

import random
import string

VOWELS = ['a','e','i','o','u']
CONSONENTS = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']

GREEK = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa", "lambda",
         "mu", "nu", "xi", "omicron", "pi", "rho", "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega"  ]

PHONECIAN = ["aleph", "beth", "gimel", "daleth", "he", "zayin", "heth", "teth", "yodh", "kaph", "lamedh",
             "mem", "nun", "samekh", "ayin", "pe", "resh", "sin", "taw", "waw"]

"""def syllable():
    string = ""
    for i in range (0,random.choice([0,1]) ):
        string += random.choice(CONSONENTS)
    string += random.choice(VOWELS)
    for i in range (0, random.choice([1,2]) ):
        string += random.choice(CONSONENTS)
    return string

def root(syllables):
    string = ""
    for i in range(syllables):
        string += syllable()
    return string"""

def name():
    string_ = random.choice(PHONECIAN) + random.choice(PHONECIAN) + " " + random.choice(GREEK) + " " + str(random.randint(1,9) )
    string_ = string.capwords(string_)
    return string_

if __name__ == '__main__':
    print name()