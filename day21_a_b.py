import utils
import subprocess

DAY = 21
subprocess.run(["fetch_my_input_once.bat", str(DAY)])

# utils.getRawInput(f"day{DAY:02}")
myInput = utils.getLinesInput(f"day{DAY:02}")
# utils.getCellsInput(f"day{DAY:02}")


class Food:
    def __init__(self, ingredients, allergens):
        assert all(len(i) > 0 for i in ingredients)
        self.ingredients = ingredients
        self.allergens = allergens


foods = []
allAllergens = set()
allIngredients = set()
for line in myInput:
    if "(contains" in line:
        allergens = line.split("(contains ")[1][:-1].split(", ")
        ingredients = line.split("(contains ")[0].strip().split(" ")
    else:
        allergens = []
        ingredients = line.strip().split(" ")
    allAllergens.update(allergens)
    allIngredients.update(ingredients)
    foods.append(Food(ingredients, allergens))

print("Allergens:", allAllergens)

ingredientsToPossibleAllergens = {ing: set() for ing in allIngredients}

# An ingredient is a candidate for an allergen if it appears in the ingredrient
# list of all foods which contains this allergen

for allerg in allAllergens:
    foodCandidates = [f for f in foods if allerg in f.allergens]
    ingredientsCandidates = [set(f.ingredients) for f in foodCandidates]

    # Filter by set intersection
    acc = set(allIngredients)
    for ic in ingredientsCandidates:
        acc &= ic

    # Add the allergen to the list
    for ingr in acc:
        ingredientsToPossibleAllergens[ingr].add(allerg)

# Find the ingredients which have no possibility left
noPossibilityIngredients = [
    ing for ing, allerg in ingredientsToPossibleAllergens.items() if len(allerg) == 0
]

accum = 0
for food in foods:
    for ing in food.ingredients:
        accum += 1 if ing in noPossibilityIngredients else 0

print("Part 1", accum)

inertIngredients = [
    ing for ing, allerg in ingredientsToPossibleAllergens.items() if len(allerg) > 0
]

# Confirm ingredients which have only one possibility
# and remove that possibility from others
# repeat until all are confirmed
CONFIRMED_INGREDIENTS = {}
while len(CONFIRMED_INGREDIENTS) < len(inertIngredients):
    for ing in inertIngredients:
        if ing in CONFIRMED_INGREDIENTS:
            continue
        if len(ingredientsToPossibleAllergens[ing]) == 1:
            allerg = list(ingredientsToPossibleAllergens[ing])[0]
            for ing2 in inertIngredients:
                if ing2 == ing:
                    continue
                ingredientsToPossibleAllergens[ing2].discard(allerg)
            CONFIRMED_INGREDIENTS[ing] = allerg

# Format as required by spec
canonicalList = [(ingr, allerg) for ingr, allerg in CONFIRMED_INGREDIENTS.items()]
canonicalList = sorted([(allerg, ingr) for ingr, allerg in canonicalList])
canonicalList = [ingr for (allerg, ingr) in canonicalList]

print("Part2", ",".join(canonicalList))