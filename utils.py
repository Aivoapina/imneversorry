def oppisWithSameText(definitions, text):
    sameDefs = []
    for defin in definitions:
        if defin[0].lower() == text.lower():
            sameDefs.append(defin[1].lower())
    result = (text, sameDefs)
    return result
