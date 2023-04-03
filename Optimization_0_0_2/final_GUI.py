import PySimpleGUI as sg

class GUI:
    def __init__(self):
        sg.theme('Black')
        self.k = 0
        self.layout = [
        [sg.Text('MINDRONE', font=('Helvetica', 40))],
        [sg.Text(self.k, font=('Helvetica', 20), key='-PERC-')],
        [sg.Text('', font=('Helvetica', 20), key='-DESC-')]
        ]
        self.window = sg.Window('Mindrone GUI', self.layout, element_justification='center', size=(400, 200))
        
    def run(self):
        while True:
            event, values = self.window.read(timeout=10)
            self.k+=1
            self.window['-PERC-'].update('Battery: ' + str(self.k) + '%')
            self.window.refresh()
            if event == "Quit" or event == sg.WIN_CLOSED:
                break
        self.window.close()

    def updateDescription(self, value):
        self.window['-DESC-'].update(value)
        self.window.refresh()
