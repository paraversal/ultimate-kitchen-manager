# The Ultimate Kitchen Manager Book

Sketch for the business logic of the Ultimate Kitchen Manager (UKM)

## Static vs. Event Data

Data in the UKM lives in two distinct sectors. The *static* sector holds information that isn't specific to one events. It's the general database where our knowledge about the kitchen is stored persistently. It includes ingredients, stores, and recipes (along with some additional information which we will get to later). The *event* sector, on the other hand, holds information about specific events. This includes data about the participation numbers, as well as which recipes are cooked, and when.

> ## Technical Note: Table namespaces
> *All data, both static data as well as data about every event, is stored in a single monolithic SQLite database. To achieve separation between different concerns, all tables are namespaced. Static tables start with `STATIC_` and event-specific tables start with `EVENT_[event name]`, where `event name` is the namespace for the respective event. To get all event namespace, query the `STATIC_event_namespaces` table.*


## Ingredients

The smallest unit inside the UKM is the *ingredient*. An ingredient is any food product that we buy, be it cereals, flour, orange juice, soy sauce, etc.

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

The hunger modifier is an upwards corrective scalar applied to the main courses for the Friday dinner. To make a long story short, Friday is travel day; people tend to eat less throughout travel days; hence they are hungrier in the evening. In the past, a hunger modifier of $1.3$ has been used, which means that $1.3$ times as much of the main courses was prepared than would be if it was a Saturday main.

# Warehousing & Procurement

Another feature of the UKM is the ability to track the foods we have in our possession. There are two types of warehousing processes:

- **Stockstaking** (Inventur)
    - Stocktaking essentially start with a blank slate; each item is scanned in; after each item has been scanned a summary is shown of how the inventory compares to the inventory before
    - The array of items scanned during stocktaking **replaces** the items in the database; the database state before the process is deleted after confirmation
- **Goods in/goods out** (Wareneingang, -ausgang)
    - Goods in/goods out is the process of adding/removing a single item or an array of items to/from the database without affecting the rest of the database

One crucial limitation of the UKM is that it **does not** track best-before-dates; therefore it is crucial to check BBD on possibly perishable foods (this should not be a big deal since usually, perishable foods should be distributed at the end of each event and only non-perishables like dry pasta and canned goods are put into storage)

# Recipe Hierarchy & Prioritisation

The procurement section in the UKM faces a central problem: any ingredient in our possession might be used for multiple recipes (e.g., cucumber might be laid out for breakfast but also used in a spread and a main dish). In order to show the procurement status for each recipe (i.e., "what ingredients are still missing for recipe x"), the UKM therefore applies a kind of hierarchichal reservation of ingredients. 

The hierarchy is as follows: 

**Main dishes > Helper Snacks > Spreads > Breakfast**

> # Example
> Say we have Tzatziki as a spread (for which we need 2 cucumber), Cucumber salad as a main (for which we need 2 cucumbers), and then also cucumber as a breakfast item (3 cucumbers); and say we have 3 cucumbers
>
> The UKM would then show: 
> - Cucumber salad: 2/2 cucumbers
> - Tzatziki: 1/2 cucumbers
> - Breakfast: 0/3 cucumbers
> 
> If we were then to enter another receipt of goods for 2 cucumbers, it would accordingly show:
> 
> - Cucumber salad: 2/2 cucumbers
> - Tzatziki: 2/2 cucumbers
> - Breakfast: 1/3 cucumbers

So for any ingredient, each recipe group successively gets the chance to resereve ingredients. This ensures that the most important recipes are successfully procured first

For two recipes of the same priority level, for now: UNDOCUMENTED (for later: either recipe with higher amount gets filled first, or vice versa)


