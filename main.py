# Crée une fonction qui prend deux nombres en entrée et retourne leur addition
def addition(a, b):
    return a + b
# Exemple d'utilisation
resultat = addition(3, 5)
print("Le résultat de l'addition est :", resultat)  # Affiche : Le résultat de l'addition est : 8
# Crée une fonction qui prend une liste de nombres et retourne la somme de ces nombres
def somme_liste(nombres):
    return sum(nombres)     
# Exemple d'utilisation
liste = [1, 2, 3, 4, 5]
resultat_somme = somme_liste(liste)
print("Le résultat de la somme est :", resultat_somme)  # Affiche : Le résultat de la somme est : 15    
# Crée une fonction qui prend une chaîne de caractères et retourne cette chaîne en majuscules
def en_majuscules(chaine):
    return chaine.upper()     
# Exemple d'utilisation
texte = "bonjour"   
texte_majuscules = en_majuscules(texte) 
print("Le texte en majuscules est :", texte_majuscules)  # Affiche : Le texte en majuscules est : BONJOUR

