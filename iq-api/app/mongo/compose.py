from typing import List

from app.mongo import tag


async def add_additional_tags(db, tags: List[str]):
    existing_tags = await tag.find(db)
    additional_tags = set(tags).difference(x["name"] for x in existing_tags)
    if additional_tags:
        await tag.insert_many(db, [{"name": tag} for tag in additional_tags])
