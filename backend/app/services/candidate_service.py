from app.database.mongodb import candidates_collection


def create_candidate(candidate_data: dict):
    data_to_insert = candidate_data.copy()

    result = candidates_collection.insert_one(
        data_to_insert
    )

    return result.inserted_id