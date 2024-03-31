from app.models import Recipe
from motor.motor_asyncio import (
    AsyncIOMotorClient,
)


import os
from dotenv import load_dotenv


load_dotenv()

recipe_id_counter = 0


def connectToDB():
    MONGO_URL = os.getenv("MONGO_URL")
    client = AsyncIOMotorClient(MONGO_URL)
    database = client.RecipeList
    recipes_db = database.recipes
    print("Successfully connected")
    return recipes_db


recipes_db = connectToDB()


# Fetch all recipes
async def fetch_all_recipes():
    # cursor = recipes_db.find({})
    # recipes = [recipe async for recipe in cursor]
    # return recipes

    recipes = []
    cursor = recipes_db.find({})

    async for document in cursor:
        recipes.append(Recipe(**document))

    return recipes


# Fetch a single recipe based on the id
async def fetch_one_recipe(recipe_id):
    document = await recipes_db.find_one({"id": recipe_id})
    return document


# Create a new recipe
async def create_new_recipe(new_recipe_data):
    global recipe_id_counter
    # Increment the counter for the new recipe
    recipe_id_counter += 1
    # Assign the counter value as the ID for the new recipe
    new_recipe_data["id"] = recipe_id_counter

    result = await recipes_db.insert_one(new_recipe_data)
    if result.inserted_id:
        return await recipes_db.find_one({"id": recipe_id_counter})
    else:
        return None


# Update an existing recipe based on the title
async def update_existing_recipe(recipe_id: int, updated_recipe_data: dict):
    # Convert the Pydantic model to a dictionary
    updated_recipe_data_dict = updated_recipe_data.dict()
    # Remove the 'id' field from the data as we don't want to update it
    updated_recipe_data_dict.pop("id", None)

    await recipes_db.update_one({"id": recipe_id}, {"$set": updated_recipe_data_dict})
    document = await recipes_db.find_one({"id": recipe_id})
    print(document, "here")
    return document


async def remove_recipe(recipe_id):
    result = await recipes_db.delete_one({"id": recipe_id})
    if result.deleted_count == 1:
        return True  # Recipe successfully deleted
    else:
        return False  # Recipe not found or deletion unsuccessful
