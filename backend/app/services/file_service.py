from app.database.mongodb import grid_fs


def save_file(
    file_data: bytes,
    filename: str,
    content_type: str
):
    file_id = grid_fs.put(
        file_data,
        filename=filename,
        content_type=content_type
    )

    return file_id