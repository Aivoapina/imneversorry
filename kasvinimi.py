import random
import re
import db


def preCleanKasvinimi(kasvi: str):
    eliRe = r'(.+) eli (.+)'
    parantheseRe = r'(.+) \((.+)\)'
    latinLineRe = r'(.+) \- (.+)'

    strOut = kasvi
    m = re.match(eliRe, strOut)
    if m:
        strOut = m[2]
    
    m = re.match(parantheseRe, strOut)
    if m:
        strOut = m[1]

    m = re.match(latinLineRe, strOut)
    if m:
        strOut = m[2]

    return strOut


def levenshteinDistance(kasvi: str, name: str):
    """Calculate Levenshtein Distance between two strings. Pseudocode from Wikipedia,
    translated into python.

    Added a preprocessing step to increase fun matches by removing latin/alternative names from
    the plant name strings before comparison.
    """


    t = preCleanKasvinimi(kasvi).lower()
    s = name.lower()

    # create two work vectors of integer distances
    n = len(t)
    m = len(s)
    v0 = [0]*(n+1)
    v1 = [0]*(n+1)

    # initialize v0 (the previous row of distances)
    # this row is A[0][i]: edit distance for an empty s
    # the distance is just the number of characters to delete from t
    for i in range(n+1):
        v0[i] = i

    for i in range(m):
        # calculate v1 (current row distances) from the previous row v0

        # first element of v1 is A[i+1][0]
        #   edit distance is delete (i+1) chars from s to match empty t
        v1[0] = i + 1

        # use formula to fill in the rest of the row
        for j in range(n):
            # calculating costs for A[i+1][j+1]
            deletionCost = v0[j + 1] + 1
            insertionCost = v1[j] + 1
            if s[i] == t[j]:
                substitutionCost = v0[j]
            else:
                substitutionCost = v0[j] + 1

            v1[j + 1] = min(deletionCost, insertionCost, substitutionCost)

        # copy v1 (current row) to v0 (previous row) for next iteration
        # since data in v1 is always invalidated, a swap without copy could be more efficient
        v0 = []+v1
    # after the last swap, the results of v1 are now in v0
    return v0[n]


def findKasvinimi(kasvinimet, first_name = "", last_name=""):
    if last_name:
        name = first_name + " " + last_name
    else:
        name = first_name
    sortedNimet = sorted(kasvinimet, key=(lambda a: levenshteinDistance(a[0], name)))
    arvo = sortedNimet[random.randint(0,13)]
    kasviNimi = arvo[0]
    return kasviNimi


if __name__ == '__main__':
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    print(findKasvinimi(db.readKasvinimet(), first_name=first_name, last_name=last_name))