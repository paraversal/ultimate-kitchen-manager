# The Ultimate Kitchen Manager Book

Sketch for the business logic of the Ultimate Kitchen Manager

## Static vs. Event Data

Data in this program lives in two distinct sectors. The *static* sector holds information that isn't specific to one events. It's the general database where our knowledge about the kitchen is stored persistently. It includes ingredients, stores, and recipes (along with some additional information which we will get to later). The *event* sector, on the other hand, holds information about specific events. This includes data about the participation numbers, as well as which recipes are cooked, and when.

## Ingredients

The smallest unit of the program is the *ingredient*. An ingredient is any food product that we buy, be it cereals, flour, orange juice, soy sauce, etc.

## Recipes

The way we specify the foods the kitchen may offer for any event is using *recipes*. "Recipes" can be both recipes in the common sense (like Chili sin Carne, Sweet Potato Curry, Lentil Soup), but they are also how we specify the foods we want to serve that don't need any preparation (like the aforementioned cereals, which are simply bought and laid on the breakfast buffet).


*Example*
```
Normal Bread:

- Rye Bread
```

In order to differentiate different recipes, they are a assigned a *recipe type*:

- Drink
- Helper Snack
- Brunch
- Misc
- Main 
- Null Prep
(maybe we can make this more specific?)

In order to correctly portion the recipes (i.e., buy and prepare the right amount of it), we assign different *plan types* to it: 

- not prepared (the food is not prepared)
- prepared at some point (the food is prepared at the event, without making any statements about when it will be prepared or eaten)
- prepared for Friday Dinner
- prepared for Saturday Dinner
- prepared for Thursday Dinner
- prepared for helpers

Not all plan types are compatible with all recipe types (other than the "not prepared" type); e.g., "Brunch" is not compatible "prepared for Thursday Dinner".

The *recipes*, along with their *plan type*s, *recipe type*s, as well as general information about the event (such as the number of participant and the "hunger modifier" [more on that later]) are then used to calculate the ingredients we need to buy as well as the recipe texts.

### The hunger modifier

The hunger modifier is an upwards corrective scalar applied to the main courses for the Friday dinner. To make a long story short, Friday is travel day; people tend to eat less throughout the day; hence they are hungrier in the evening. In the past, a hunger modifier of $1.3$ has been used, which means that $1.3$ times as much of the main courses was prepared than would be if it was a Saturday main.