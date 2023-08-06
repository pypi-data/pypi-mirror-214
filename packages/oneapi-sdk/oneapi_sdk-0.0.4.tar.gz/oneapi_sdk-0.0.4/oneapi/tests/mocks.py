MOVIES = [
    {
        '_id': '5cd95395de30eff6ebccde5c',
        'name': 'The Fellowship of the Ring',
        'runtimeInMinutes': 201,
        'budgetInMillions': 93,
        'boxOfficeRevenueInMillions': 377.85,
        'academyAwardNominations': 13,
        'academyAwardWins': 4,
        'rottenTomatoesScore': 93,
    },
    {
        '_id': '5cd95395de30eff6ebccde5d',
        'name': 'The Two Towers',
        'runtimeInMinutes': 179,
        'budgetInMillions': 94,
        'boxOfficeRevenueInMillions': 340.48,
        'academyAwardNominations': 6,
        'academyAwardWins': 2,
        'rottenTomatoesScore': 95,
    },
    {
        '_id': '5cd95395de30eff6ebccde5e',
        'name': 'The Return of the King',
        'runtimeInMinutes': 201,
        'budgetInMillions': 94,
        'boxOfficeRevenueInMillions': 1119.93,
        'academyAwardNominations': 11,
        'academyAwardWins': 11,
        'rottenTomatoesScore': 95,
    }
]

QUOTES = [
    {
        'id': '5cd95395de30eff6ebccde5f',
        '_id': '5cd95395de30eff6ebccde5f',
        'dialog': 'Gandalf! Bilbo!',
        'movie': '5cd95395de30eff6ebccde5c',
        'character': '5cd95395de30eff6ebccde5c',
    },
    {
        'id': '5cd95395de30eff6ebccde60',
        '_id': '5cd95395de30eff6ebccde60',
        'dialog': 'I am Gandalf the White.',
        'movie': '5cd95395de30eff6ebccde5c',
        'character': '5cd95395de30eff6ebccde5c',
    },
    {
        'id': '5cd95395de30eff6ebccde61',
        '_id': '5cd95395de30eff6ebccde61',
        'dialog': 'I am Saruman the White.',
        'movie': '5cd95395de30eff6ebccde5c',
        'character': '5cd95395de30eff6ebccde5c',
    }
]

def create_response(data, total=None):
    return {
        "docs": data,
        "total": total if total else len(data),
        "limit": len(data),
        "offset": 0,
    }