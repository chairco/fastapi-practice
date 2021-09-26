from app.api.models import NoteSchema
from app.db import notes, database


async def post(payload: NoteSchema):
    query = notes.insert().values(title=payload.title, description=payload.description)
    return await database.execute(query=query)


async def get(id: int):
    query = notes.select().where(id == notes.c.id)
    return await database.fetch_one(query=query)


async def put(id: int, payload: NoteSchema):
    query = (
        notes
        .update()
        .where(id == notes.c.id)
        .values(title=payload.title, description=payload.description)
        .returning(notes.c.id)
    )
    return await database.execute(query=query)


@router.delete("/{id}/", response_model=NoteDB)
async def delete_note(id: int = Path(..., gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    await crud.delete(id)

    return note