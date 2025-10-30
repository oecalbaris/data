


from fastapi import FastAPI, File

import pathlib

from starlette.responses import FileResponse

app = FastAPI()

current_file_path = str(pathlib.Path(__file__).parent)

file_path_input = f"{current_file_path}/data/input"
file_path_output = f"{current_file_path}/data/output"

file_name_config = "config.json"

#downloading
@app.get("/download_csv")
def download_csv(upload_file = File(...)):

    with open(file_path_input,mode="wb", encoding="UTF-8") as file:
        file.write(upload_file.file.read())
        file.close()

    return {"message": f"File saved to {file_path_input}"}




#saving choices for cleaning configuration
@app.get("/save_choices")
def save_choices():

    with open(file_path_output, "w") as file:
        file.write(file_name_config)
    return

#uploading
@app.get("/upload_csv")
def upload_csv():

    return FileResponse(path=file_path_output,filename="cleaned.csv")




