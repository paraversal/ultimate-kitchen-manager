from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from db.management import engine

Base = declarative_base()

class Store(Base):
    __tablename__ = "STATIC_stores"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    items = relationship("Ingredient", back_populates="ingredient")

# Represents which recipe types support which recipe plan type 
# (e.g., the "helper dishes saturday" recipe plan can only be applied to recipes with the "helper dish" type)
recipe_supported_plan_types = Table(
    "STATIC_recipe_supported_plan_types",
    Base.metadata,
    Column("recipe_instance_plan_type_id", ForeignKey("STATIC_recipe_plan_types.id"), primary_key=True),
    Column("recipe_type_id", ForeignKey("recipe_types.id"), primary_key=True),

)

# Represents the different types of recipe planing
# (e.g., cook only on saturday, cook only on friday but for 50% of the people, cook only for orga, etc)
class RecipePlanType(Base):
    __tablename__ = "STATIC_recipe_plan_types"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    recipe_types = relationship("RecipeType", secondary=recipe_supported_plan_types, back_populates="recipe_plan_types")

class RecipeType(Base):
    __tablename__ = "recipe_types"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    recipes = relationship("Recipe")
    recipe_plan_types = relationship("RecipePlanType", secondary=recipe_supported_plan_types, back_populates="recipe_types")

ingredients_recipes = Table(
    "STATIC_ingredient_recipes",
    Base.metadata,
    Column("ingredient_id", ForeignKey("ingredients.id"), primary_key=True),
    Column("recipe_id", ForeignKey("recipes.id"), primary_key=True),
)

class Ingredient(Base):
    __tablename__ = "STATIC_ingredients"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    store = Column(Integer, ForeignKey('stores.id'))
    unit = Column(String, nullable=False)
    price_per_unit = Column(Float)
    store = relationship("Store", back_populates="items")
    recipes = relationship(
        "Recipe", secondary=ingredients_recipes, back_populates="ingredients"
    )

class Recipe(Base):
    __tablename__ = "STATIC_recipes"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    steps = Column(String, nullable=False)
    additional_info = Column(String)
    type = Column(Integer, ForeignKey("recipe_types.id"))
    #result_amount_pp_g = Column(Integer, nullable=False)
    ingredients = relationship(
        "Ingredient", secondary=ingredients_recipes, back_populates="recipes"
    )

Base.metadata.create_all(bind=engine)
