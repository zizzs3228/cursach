import rarfile
import zipfile
import os

async def rar_preparation(user_id: str) -> str:
    path = f"./accs/{user_id}"
    if not os.path.exists(path):
        print("Папка пользователя не существует, создаем...")
        os.mkdir(path)

    return path


async def archive_extract(user_id: str, path_to_archive:str) ->list[str]:
    name = path_to_archive.split('/')[-1].split('.')
    if len(name)==2:
        if name[1]=='rar':
            with rarfile.RarFile(path_to_archive) as rar:
                print("in foo")
                path = await rar_preparation(user_id)
                for file in rar.namelist():
                    print(file)
                    if (".session" in file) or (".json" in file):
                        rar.extract(file, path)
        elif name[1]=='zip':
            with zipfile.ZipFile(path_to_archive) as zip:
                print("in foo")
                path = await rar_preparation(user_id)
                for file in zip.namelist():
                    print(file)
                    if (".session" in file) or (".json" in file):
                        zip.extract(file, path)
        else:
            print('Расширеие неправильное, нужно zip или rar')
    else:
        print('НАЗВАНИЕ ФАЙЛА ДОЛЖНО БЫТЬ что-тотам.zip или что-тотам.rar')
    