from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, mapped_column, Mapped
from src.db.management import engine

Base = declarative_base()

class Store(Base):
    __tablename__ = "STATIC_stores"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    items: Mapped[list["Ingredient"]] = relationship(back_populates="store")

# TODO: is this unnecessary complexity? Do we really need to enforce this? Or would it be better to leave open the flexibility?
# Represents which recipe types support which recipe plan type 
# (e.g., the "helper dishes saturday" recipe plan can only be applied to recipes with the "helper dish" type)
# recipe_supported_plan_types = Table(
#     "STATIC_recipe_supported_plan_types",
#     Base.metadata,
#     Column("recipe_instance_plan_type_id", ForeignKey("STATIC_recipe_plan_types.id"), primary_key=True),
#     Column("recipe_type_id", ForeignKey("STATIC_recipe_types.id"), primary_key=True),

# )

# Represents the different types of recipe planing
# (e.g., cook only on saturday, cook only on friday but for 50% of the people, cook only for orga, etc)
class RecipePlanType(Base):
    __tablename__ = "STATIC_recipe_plan_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    #recipe_types: Mapped[list[RecipeType]] = relationship(secondary=recipe_supported_plan_types)

class RecipeType(Base):
    __tablename__ = "STATIC_recipe_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    recipes: Mapped[list[Recipe]] = relationship("Recipe")
    # recipe_plan_types = relationship("RecipePlanType", secondary=recipe_supported_plan_types, back_populates="recipe_types")

ingredients_recipes = Table(
    "STATIC_ingredient_recipes",
    Base.metadata,
    Column("ingredient_id", ForeignKey("STATIC_ingredients.id"), primary_key=True),
    Column("recipe_id", ForeignKey("STATIC_recipes.id"), primary_key=True),
    Column("amount", Float)
)

class Ingredient(Base):
    __tablename__ = "STATIC_ingredients"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    unit: Mapped[str] = mapped_column(nullable=False)
    price_per_unit: Mapped[float] = mapped_column()
    store_id: Mapped[int] = mapped_column(ForeignKey('STATIC_stores.id'))
    store: Mapped[Store] = relationship(back_populates="items")
    recipes = relationship(
        "Recipe", secondary=ingredients_recipes, back_populates="ingredients"
    )
    eans: Mapped[list[EAN]] = relationship()

class EAN(Base):
    __tablename__ = "STATIC_EANs"
    id: Mapped[int] = mapped_column(primary_key=True)
    ean: Mapped[int] = mapped_column()
    product_id: Mapped[int] = mapped_column(ForeignKey("STATIC_ingredients.id"))
    product: Mapped[Ingredient] = relationship(back_populates="eans")

class Recipe(Base):
    __tablename__ = "STATIC_recipes"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    steps: Mapped[str] = mapped_column(nullable=False)
    additional_info: Mapped[str] = mapped_column()
    type: Mapped[int] = mapped_column(ForeignKey("STATIC_recipe_types.id"))
    result_amount_pp_g: Mapped[float] = mapped_column(nullable=False)
    ingredients = relationship(
        "Ingredient", secondary=ingredients_recipes, back_populates="recipes"
    )

# EVENT PLANING

class EventNamespace(Base):
    __tablename__ = "STATIC_event_namespaces"
    id: Mapped[int] = mapped_column(primary_key=True)
    namespace: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()

class Event(Base):
    __tablename__ = "EVENT_NebuSummer2026_Outline"
    id: Mapped[int] = mapped_column(primary_key=True)
    namespace: Mapped[int] = mapped_column(ForeignKey("STATIC_event_namespaces.id"))
    participants: Mapped[int] = mapped_column()
    thursday_stays: Mapped[int] = mapped_column()
    additional_hunger_modifier: Mapped[float] = mapped_column()
    helper_food_modifier: Mapped[float] = mapped_column()

class RecipePlan(Base):
    __tablename__ = "EVENT_NebuSummer2026_RecipePlans"
    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column()
    plan_type: Mapped[int] = mapped_column()

Base.metadata.create_all(bind=engine)
