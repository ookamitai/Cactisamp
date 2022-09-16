from pathlib import Path

import PySimpleGUI as sg


def guiwindow():
    file_list = [
        [
            sg.Text("Choose a folder:"),
            sg.In(size=(25, 1), enable_events=True, key="-Folder-"),
            sg.FolderBrowse(),
        ],
    ]

    layout = [
        [
            sg.Column(file_list),
        ],
    ]

    window = sg.Window("Folder Browser", layout)

    while True:
        event, Values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-Folder-":
            folder = Values["-Folder-"]
            # Use pathlib.Path instead of os.path to avoid errors with special characters
            path = Path(folder)
            if not path.is_dir():
                # If the path is not a directory, continue
                continue
            fname = []
            for item in path.iterdir():
                # Iterate over the files in the directory
                if Path(item).is_file() and item.suffix.lower() == ".wav":
                    # If the item is a file and has a .wav extension, add it to the list
                    fname.append(item.name)
            window.close()
            return folder, fname
