import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select

# Environment variables from Portainer config
DATABASE_URL = os.getenv("DATABASE_URL", "")

engine = create_engine(DATABASE_URL)
app = FastAPI(title="D&D Spell API")

# --- Models ---
class Spell(SQLModel, table=True):
    __tablename__ = "spells"
    slug: str = Field(primary_key=True)
    name: str
    desc: str
    level: int
    school: str
    dnd_class: Optional[str] = None # Some DBs use a junction table, but your JSON showed a string

class SpellClass(SQLModel, table=True):
    __tablename__ = "classes"
    id: int = Field(primary_key=True)
    name: str

# --- DB Dependency ---
def get_session():
    with Session(engine) as session:
        yield session

# --- Endpoints ---
@app.get("/spells", response_model=List[Spell])
def get_spells(limit: int = 10, session: Session = Depends(get_session)):
    return session.exec(select(Spell).limit(limit)).all()

@app.get("/spells/{slug}", response_model=Spell)
def get_spell(slug: str, session: Session = Depends(get_session)):
    spell = session.get(Spell, slug)
    if not spell:
        raise HTTPException(status_code=404, detail="Spell not found")
    return spell

@app.get("/classes", response_model=List[SpellClass])
def get_classes(session: Session = Depends(get_session)):
    return session.exec(select(SpellClass)).all()
