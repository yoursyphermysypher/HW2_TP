import pytest

from recipes import Ingredient, Recipe, ShoppingList


def test_ingredient_init():
    ingredient = Ingredient("Мука", 500, "г")

    assert ingredient.name == "Мука"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == "г"


def test_ingredient_str():
    ingredient = Ingredient("Мука", 500, "г")

    assert str(ingredient) == "Мука: 500.0 г"


def test_ingredient_eq_same_name_and_unit():
    ingredient_1 = Ingredient("Мука", 500, "г")
    ingredient_2 = Ingredient("Мука", 300, "г")

    assert ingredient_1 == ingredient_2


def test_ingredient_eq_different_name():
    ingredient_1 = Ingredient("Мука", 500, "г")
    ingredient_2 = Ingredient("Сахар", 500, "г")

    assert ingredient_1 != ingredient_2


def test_ingredient_eq_different_unit():
    ingredient_1 = Ingredient("Мука", 500, "г")
    ingredient_2 = Ingredient("Мука", 1, "кг")

    assert ingredient_1 != ingredient_2


def test_recipe_create():
    recipe = Recipe("pasta", [Ingredient("Мука", 500, "г")])

    assert recipe.title == "pasta"
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].name == "Мука"
    assert recipe.ingredients[0].quantity == 500.0
    assert recipe.ingredients[0].unit == "г"


def test_recipe_add_ingredient():
    recipe = Recipe("pasta", [Ingredient("Мука", 500, "г")])

    recipe.add_ingredient(Ingredient("Сахар", 500, "г"))
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))

    assert [(i.name, i.quantity, i.unit) for i in recipe.ingredients] == [
        ("Мука", 800.0, "г"),
        ("Сахар", 500.0, "г"),
    ]


def test_recipe_scale():
    recipe = Recipe("pasta", [Ingredient("Мука", 500, "г"), Ingredient("Сахар", 200, "г")])
    scaled = recipe.scale(2)

    assert scaled is not recipe
    assert [(i.name, i.quantity, i.unit) for i in scaled.ingredients] == [
        ("Мука", 1000.0, "г"),
        ("Сахар", 400.0, "г"),
    ]
    assert [(i.name, i.quantity, i.unit) for i in recipe.ingredients] == [
        ("Мука", 500.0, "г"),
        ("Сахар", 200.0, "г"),
    ]


def test_recipe_scale_invalid_ratio():
    recipe = Recipe("pasta", [Ingredient("Мука", 500, "г")])

    with pytest.raises(ValueError):
        recipe.scale(0)

    with pytest.raises(ValueError):
        recipe.scale(-1)


def test_recipe_len():
    recipe = Recipe(
        "salad",
        [
            Ingredient("Огурец", 2, "кг"),
            Ingredient("Помидор", 3, "кг"),
            Ingredient("Огурец", 1, "кг"),
            Ingredient("Соль", 5, "г"),
            Ingredient("Соль", 2, "г"),
        ],
    )

    assert len(recipe) == 3
    assert len(Recipe("empty", [])) == 0


def test_shopping_list_add_recipe():
    shopping_list = ShoppingList()
    recipe = Recipe("pasta", [Ingredient("Мука", 500, "г"), Ingredient("Сахар", 200, "г")])

    shopping_list.add_recipe(recipe, 2)

    assert [(i.name, i.quantity, i.unit, title) for i, title in shopping_list._items] == [
        ("Мука", 1000.0, "г", "pasta"),
        ("Сахар", 400.0, "г", "pasta"),
    ]


def test_shopping_list_add_recipe_invalid_portions():
    shopping_list = ShoppingList()
    recipe = Recipe("pasta", [Ingredient("Мука", 500, "г")])

    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, 0)

    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, -1)


def test_shopping_list_remove_recipe():
    shopping_list = ShoppingList()
    recipe_1 = Recipe("pasta", [Ingredient("Мука", 500, "г")])
    recipe_2 = Recipe("salad", [Ingredient("Огурец", 2, "шт")])

    shopping_list.add_recipe(recipe_1, 1)
    shopping_list.add_recipe(recipe_2, 1)
    shopping_list.remove_recipe("pasta")
    shopping_list.remove_recipe("pizza")

    assert [(i.name, i.quantity, i.unit, title) for i, title in shopping_list._items] == [
        ("Огурец", 2.0, "шт", "salad"),
    ]


def test_shopping_list_get_list():
    shopping_list = ShoppingList()
    recipe_1 = Recipe("pasta", [Ingredient("Мука", 500, "г"), Ingredient("Сахар", 200, "г")])
    recipe_2 = Recipe("cake", [Ingredient("Мука", 300, "г"), Ingredient("Яйцо", 2, "шт")])

    shopping_list.add_recipe(recipe_1, 1)
    shopping_list.add_recipe(recipe_2, 2)

    result = shopping_list.get_list()

    assert [(i.name, i.quantity, i.unit) for i in result] == [
        ("Мука", 1100.0, "г"),
        ("Сахар", 200.0, "г"),
        ("Яйцо", 4.0, "шт"),
    ]


def test_shopping_list_add():
    shopping_list_1 = ShoppingList()
    shopping_list_2 = ShoppingList()
    recipe_1 = Recipe("pasta", [Ingredient("Мука", 500, "г")])
    recipe_2 = Recipe("cake", [Ingredient("Сахар", 200, "г")])

    shopping_list_1.add_recipe(recipe_1, 1)
    shopping_list_2.add_recipe(recipe_2, 1)
    result = shopping_list_1 + shopping_list_2

    assert result is not shopping_list_1
    assert result is not shopping_list_2
    assert [(i.name, i.quantity, i.unit, title) for i, title in result._items] == [
        ("Мука", 500.0, "г", "pasta"),
        ("Сахар", 200.0, "г", "cake"),
    ]
    assert [(i.name, i.quantity, i.unit, title) for i, title in shopping_list_1._items] == [
        ("Мука", 500.0, "г", "pasta"),
    ]
    assert [(i.name, i.quantity, i.unit, title) for i, title in shopping_list_2._items] == [
        ("Сахар", 200.0, "г", "cake"),
    ]
