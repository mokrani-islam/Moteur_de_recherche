# Correction de G. Poux-Médard, 2021-2022

from Classes import Author
import pandas as pd
import re
from collections import Counter
import csv 
# =============== 2.7 : CLASSE CORPUS ===============

class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
        self.full_text = ""

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc
        self.full_text += doc.texte

# =============== 2.8 : REPRESENTATION ===============
    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))
    
    def show_authors(self):
        for author_id, author in self.authors.items():
            print(f"Auteur {author_id}: {author.name}")
            print(f"Nombre de documents: {author.ndoc}")
            print(f"Production: {', '.join(author.production)}\n")
    
    def generate_concordance_df(cls,text, keyword, context_words=10):
        # Utilisation de re pour trouver les occurrences du mot clé
        matches = re.finditer(r'\b' + re.escape(keyword) + r'\b', text)
        print(matches)
        # Création d'une liste pour stocker les résultats
        results = []

        # Construction du DataFrame
        for match in matches:
       
          start = max(0, match.start() - context_words)
          end = min(len(text), match.end() + context_words + 1)
          context_left = text[start:match.start()].strip()
          print(context_left)
          context_right = text[match.end():end].strip()
          keyword_found = match.group()

          results.append({
            "Contexte_Gauche": context_left,
            "Motif_Trouve": keyword_found,
            "Contexte_Droit": context_right
        })

        # Création du DataFrame
        df = pd.DataFrame(results)
        return df
    
    def nettoyer_texte(self, texte):
        # Implémentation de la fonction de nettoyage du texte
        # (mise en minuscules, remplacement des passages à la ligne, etc.)
        text_netoye = texte.lower().replace('\n', ' ').replace('\r', '')
        text_netoye = re.sub(r'[^a-zA-Z\s]', '', text_netoye)  # Remplacer tout ce qui n'est pas une lettre ou un espace par une chaîne vide
        return text_netoye

    # Exemple d'utilisation

    def construire_vocabulaire(self):
        # Initialisation du vocabulaire comme un ensemble
        vocabulaire = set()

        # Boucler sur les documents du corpus
        for doc_id, document in self.id2doc.items():
            # Nettoyer le texte de chaque document 
            texte_nettoye = self.nettoyer_texte(document.texte)

            # Split du texte en mots en utilisant différents délimiteurs (espace, tabulation, ponctuation, etc.)
            mots = re.split(r'\s+|[.,;\'"!?]', texte_nettoye)

            # le fait d'avoir mis vocabulaire ici permettra de compter le nombre 
            # d'occurence directement et plus facilement 
            # c'est à dire pour chaque document On élimine ses doublons afin de créer son vocabulaire
            # en bref on crée pour chaque document son vocabulaire :)
            vocabulaire.update(mots)

        # Retourne le vocabulaire construit
        return vocabulaire
    
    def stats(self, n_mots_frequents=10):
        # Construction du vocabulaire
        vocabulaire = self.construire_vocabulaire()

        # Initialisation du tableau freq avec la librairie pandas
        freq = pd.DataFrame(columns=['Mot', 'Occurrences', 'Documents'])

        # Initialisation du compteur total d'occurrences
        total_occurrences = Counter()

        # Initialisation du dictionnaire de document frequency
        doc_frequency = Counter()

        # Boucle sur les documents du corpus
        for doc_id, document in self.id2doc.items():
            # Nettoyage du texte
            texte_nettoye = self.nettoyer_texte(document.texte)

            # Comptage des occurrences des mots dans le document
            occurrences = Counter(re.split(r'\s+|[.,;\'"!?]', texte_nettoye))

            # Mise à jour du compteur total d'occurrences
            total_occurrences.update(occurrences)

            # Mise à jour du dictionnaire de document frequency
            doc_frequency.update(set(occurrences.keys()))

        # Remplissage du tableau freq
        freq['Mot'] = total_occurrences.keys()
        freq['Occurrences'] = total_occurrences.values()
        freq['Documents'] = freq['Mot'].apply(lambda mot: doc_frequency[mot])

        # Tri par occurrences décroissantes
        freq = freq.sort_values(by='Occurrences', ascending=False)

        # Affichage du nombre de mots différents dans le corpus
        print(f"Nombre de mots différents dans le corpus: {len(vocabulaire)}")

        # Affichage des n mots les plus fréquents
        print(freq.head(n_mots_frequents))
    

