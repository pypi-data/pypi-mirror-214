us2gb = {
    "aerograms": "aerogrammes", "aging": "ageing", "amortizations": "amortisations", "biased": "biassed",
    "caliber": "calibre", "calisthenics": "callisthenics", "cannibalized": "cannibalised", "cataloged": "catalogued",
    "cataloging": "cataloguing", "caviling": "cavilling", "centimeter": "centimetre", "connection": "connexion",
    "contextualized": "contextualised", "councilor": "councillor", "cudgeling": "cudgelling", "customizes": "customises",
    "decriminalize": "decriminalise", "democratized": "democratised", "democratizing": "democratising", "deodorizing": "deodorising",
    "dialed": "dialled", "discolor": "discolour", "pedestrianized": "pedestrianised",
    "personalizes": "personalises", "practices": "practises", "pulverization": "pulverisation",
    "remolded": "remoulded", "rumor": "rumour", "scandalizes": "scandalises", "sheik": "sheikh",
    "siphoning": "syphoning", "splendor": "splendour", "stabilized": "stabilised", "standardizing": "standardising",
    "stigmatize": "stigmatise", "sulfate": "sulphate",
    "cookie": "biscuit",
    "cookies": "biscuits",
    "fries": "chips",
    "apartment": "flat",
}

def britishize(text):
    """
    Returns the British English version of the passed-in American
    English text.
    """
    words = text.split()
    brand_new_words = []
    for i in range(len(words)):
        if words[i] in us2gb:
            brand_new_words.append(us2gb[words[i]])
        else:
            brand_new_words.append(words[i])

    return " ".join(brand_new_words)

import typer

app = typer.Typer()

@app.command()
def translate(american_english: str):
    print(britishize(american_english))

def main():
    app()
