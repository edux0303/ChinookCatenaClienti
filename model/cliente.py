from dataclasses import dataclass,field

@dataclass
class Cliente:
    id: int
    name: str
    cognome: str
    paese: str
    spesa : float

    album: set = field(default_factory=set)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"{self.name} {self.cognome}"

