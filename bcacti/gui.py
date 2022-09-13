import PySimpleGUI as sg
import os


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
            try:
                file_list_data = os.listdir(folder)
            except:
                file_list_data = []
            fname = []
            for item in file_list_data:
                if os.path.isfile(os.path.join(folder, item)) and item.lower().endswith(
                    ".wav"
                ):
                    fname.append(item)
            window.close()
            return folder, fname
