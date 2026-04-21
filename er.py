from src.db.models import Base
from eralchemy2 import render_er

output_file = "er_diagram.png"
render_er(Base, output_file)

print(f"ER diagram written to {output_file}")