class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise ValueError("количество должно быть числом")

        if value <= 0:
            raise ValueError("количество должно быть положительным")

        self._quantity = value

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, value):
        if not isinstance(value, Ingredient):
            return False

        return self.name == value.name and self.unit == value.unit


class Recipe:
    def __init__(self, title: str, ingredients: list[Ingredient]):
        self.title = title
        self.ingredients = ingredients

    def add_ingredient(self, ingredient: Ingredient):
        if ingredient in self.ingredients:
            self.ingredients[self.ingredients.index(ingredient)].quantity += ingredient.quantity
        else:
            self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        try:
            return float(ratio) > 0
        except (ValueError, TypeError):
            return False

    def scale(self, ratio: float):
        if not Recipe.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным числом")

        ratio = float(ratio)
        return Recipe(
            self.title,
            [Ingredient(i.name, i.quantity * ratio, i.unit) for i in self.ingredients],
        )

    def __len__(self):
        uniq = set((i.name, i.unit) for i in self.ingredients)
        return len(uniq)

    def __str__(self):
        list_ingredients = "\n".join([str(i) for i in self.ingredients])
        return f"{self.title}:\n {list_ingredients}"


class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        if ingredients is None:
            ingredients = []

        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float):
        scaled = super().scale(ratio)
        return DietaryRecipe(self.title, self.diet_type, scaled.ingredients)

    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"


class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")

        scaled = recipe.scale(portions)
        for ing in scaled.ingredients:
            self._items.append((ing, recipe.title))

    def remove_recipe(self, title: str):
        self._items = [item for item in self._items if item[1] != title]

    def get_list(self):
        d = {}

        for ing, _ in self._items:
            key = (ing.name, ing.unit)
            d[key] = d.get(key, 0) + ing.quantity

        result = [Ingredient(name, qty, unit) for (name, unit), qty in d.items()]
        result.sort(key=lambda x: x.name)
        return result

    def __add__(self, other: "ShoppingList"):
        new = ShoppingList()
        new._items = self._items + other._items
        return new
