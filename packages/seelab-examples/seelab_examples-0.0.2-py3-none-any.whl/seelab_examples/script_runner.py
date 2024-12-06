import os
import sys
import tempfile,importlib
from functools import partial
from PyQt5 import QtWidgets, QtGui, QtCore
try:
    from .syntax import PythonHighlighter
except:
    from syntax import PythonHighlighter

from eyes17.eyes import open as eyes17_open

import importlib.util  # Added import for importlib

class ScriptRunner(QtWidgets.QMainWindow):
    def __init__(self, args):
        super().__init__()
        layouts_path = os.path.join(os.path.dirname(__file__), 'layouts')
        sys.path.append(layouts_path)  # Add layouts directory to sys.path

        self.createFileMenu()
        self.createThemeMenu()
        self.createPipMenu()
        self.device = eyes17_open()
        self.setWindowTitle("SEELab3/ExpEYES Sample Programs")
        self.setGeometry(100, 100, 800, 600)
        self.editMode = True
        self.module = None
        self.ipyConsole = None

        # Create a central widget
        self.central_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a toolbar for script selection
        self.toolbar = QtWidgets.QToolBar("Scripts")
        self.addToolBar(QtCore.Qt.LeftToolBarArea,self.toolbar)

        self.script_selector = QtWidgets.QComboBox(self)
        self.toolbar.addWidget(self.script_selector)

        # Add a button to run/edit the code
        self.run_code_button = QtWidgets.QPushButton("Run Code", self)
        self.run_code_button.setIcon(QtGui.QIcon(os.path.join("icons","play_icon.png")))  # Set play icon
        self.run_code_button.clicked.connect(self.run_code)
        self.toolbar.addWidget(self.run_code_button)

        self.addSubsectionIcons()

        # Store the currently loaded script
        self.current_script = None

        # Add the QTextEdit to the central widget
        self.source_code_edit = QtWidgets.QTextEdit(self)
        self.central_widget.addWidget(self.source_code_edit)
        self.central_widget.setCurrentWidget(self.source_code_edit)  # Show the source code editor

        # Create a button to open the IPython console with a Python logo icon
        self.console_button = QtWidgets.QPushButton("Write Code!",self)
        self.console_button.setIcon(QtGui.QIcon(os.path.join("icons","python_logo.png")))  # Set Python logo icon
        self.console_button.clicked.connect(self.add_ipython_console)
        self.toolbar = QtWidgets.QToolBar("Simple Scripts")
        self.addToolBar(QtCore.Qt.LeftToolBarArea,self.toolbar)

        self.toolbar.addWidget(self.console_button)

        # Remove tmp.py
        tmp_file_path = os.path.join(os.path.dirname(__file__), 'tmp.py')
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)




        # Load available scripts
        self.load_available_scripts()
        default = args.script if args.script else 'oscilloscope'
        self.script_selector.setCurrentText(default)
        self.load_script(default)

        self.script_selector.currentTextChanged.connect(self.load_script)
        self.setTheme("default")

    def addSubsectionIcons(self):
        # Add square icon buttons to the toolbar
        icon_names = ["optics.png", "mechanics.png", "electrical.png", "shock.png", "sensors.png"]
        for icon_name in icon_names:
            button = QtWidgets.QPushButton(self)
            button.setIcon(QtGui.QIcon(os.path.join("icons", icon_name)))  # Set icon
            button.setFixedHeight(60)  # Set fixed height
            button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)  # Allow width to expand
            button.setIconSize(QtCore.QSize(60, 60))
            self.toolbar.addWidget(button)  # Add button to the toolbar


    def createFileMenu(self):
        self.file_menu = self.menuBar().addMenu("File")
        self.options_menu = self.menuBar().addMenu("Options")

        # Add actions to the File menu
        self.open_action = QtWidgets.QAction("Open Script", self)
        self.open_action.triggered.connect(self.open_script)
        self.file_menu.addAction(self.open_action)

        self.save_action = QtWidgets.QAction("Save Script", self)
        self.save_action.triggered.connect(self.save_script)
        self.file_menu.addAction(self.save_action)

        # Add a checkbox to the File menu
        # Create an 'Expert' checkbox in the dropdown file menu

        self.edit_code_first = QtWidgets.QAction("Edit Code First", self, checkable=True)
        self.edit_code_first.setChecked(False)  # Set initial state
        self.edit_code_first.triggered.connect(self.enableCodeEditing)  # Connect to a method
        self.options_menu.addAction(self.edit_code_first)

    def createThemeMenu(self):
        self.theme_menu = self.menuBar().addMenu("Theme")
        theme_files = [f for f in os.listdir('themes') if f.endswith('.qss')]
        for theme_file in theme_files:
            theme_action = QtWidgets.QAction(theme_file, self)
            theme_action.triggered.connect(partial(self.setTheme,theme_file[:-4]))
            self.theme_menu.addAction(theme_action)
            print(theme_file[:-4])

    def createPipMenu(self):
        self.pip_menu = self.menuBar().addMenu("Install Packages")
        for a in [("PyQt5 GUI",'pyqt5'),('NumPy','numpy'),('SciPy','scipy'),('pyqtgraph','pyqtgraph'),('pyserial','pyserial'),('matplotlib','matplotlib'),('qtconsole','qtconsole'),('All of these','numpy scipy pyqtgraph pyqt5 pyserial matplotlib qtconsole')]:
            action = QtWidgets.QAction(a[0], self)
            action.triggered.connect(partial(self.showPipInstaller,a[1] ))
            self.pip_menu.addAction(action)

    def showPipInstaller(self, name):
        from utilities.pipinstaller import PipInstallDialog
        self.pipdialog = PipInstallDialog(name, self)
        self.pipdialog.show()

    def open_script(self):
        """Open a script file and load its content into the editor."""
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Script File", "", "Python Files (*.py);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                self.source_code_edit.setPlainText(file.read())

    def save_script(self):
        """Save the current content of the editor to a script file."""
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Script File", "", "Python Files (*.py);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.source_code_edit.toPlainText())

    def enableCodeEditing(self,s):
        pass
        #self.run_code_button.setVisible(s)

    def load_available_scripts(self):
        """Load Python scripts from the current directory."""
        script_dir = os.path.dirname(__file__)
        scripts = [f[:-3] for f in os.listdir(script_dir) if f.endswith('.py') and f not in ['script_runner.py', 'syntax.py', 'syntax2.py', 'tmp.py', '__main__.py','__init__.py','utils.py','mycode.py','ipy.py']]
        self.script_selector.addItems(scripts)

    def load_available_baremetal_scripts(self):
        """Load Python scripts from the current directory."""
        script_dir = os.path.join(os.path.dirname(__file__),'examples')
        scripts = [f[:-3] for f in os.listdir(script_dir) if f.endswith('.py') and f not in ['__init__.py']]
        self.simple_script_selector.addItems(scripts)

    def load_script(self, opt=None):
        """Load and display the selected script's source code."""
        if opt is None:
            selected_script = self.script_selector.currentText()
            if self.current_script:
                self.current_script.close()  # Close the currently loaded script

        else:
            selected_script = opt

        script_path = os.path.join(os.path.dirname(__file__), f"{selected_script}.py")
        self.setEditMode()


        with open(script_path, 'r') as file:
            source_code = file.read()

        self.central_widget.setCurrentWidget(self.source_code_edit)  # Show the source code editor

        self.source_code_edit.setPlainText(source_code)
        self.source_code_edit.setReadOnly(False)  # Allow editing
        self.highlight = PythonHighlighter(self.source_code_edit.document())  # Syntax highlighting
        if not self.edit_code_first.isChecked() and selected_script != 'tmp':
            self.run_code()

    def load_simple_script(self, opt=None):
        with open(os.path.join( os.path.dirname(__file__), 'examples', opt+'.py'), 'r') as file:
            self.text_editor.setText(file.read())

    def execute_simple_script(self):
        source_code = self.text_editor.toPlainText()
        source_code = '\n'.join([line for line in source_code.split('\n') if 'import eyes17' not in line])
        source_code = '\n'.join([line for line in source_code.split('\n') if 'open()' not in line])

        temp_file_path = os.path.join(os.path.dirname(__file__), 'mycode.py')
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(source_code)  # Save the edited code

        #self.ipyConsole.execute(source_code)
        self.ipyConsole.execute('%run -i mycode.py')


    def run_code(self):
        """Replace the source code editor with the Expt class of the selected script."""
        if self.editMode:
            selected_script = self.script_selector.currentText()
            if selected_script:
                self.editMode = False
                # Save the edited source code to a temporary file
                temp_file_path = os.path.join(os.path.dirname(__file__), 'tmp.py')
                with open(temp_file_path, 'w') as temp_file:
                    temp_file.write(self.source_code_edit.toPlainText())  # Save the edited code
                # Remove tmp* from the __pycache__ directory before import
                pycache_dir = os.path.join(os.path.dirname(__file__), '__pycache__')
                for file in os.listdir(pycache_dir):
                    if file.startswith('tmp'):
                        os.remove(os.path.join(pycache_dir, file))
                importlib.invalidate_caches()
                if self.module:
                    self.module = importlib.reload(self.module)
                if __name__ == '__main__':
                    self.module = importlib.import_module('tmp')  # Import the temporary module with explicit import
                else:
                    self.module = importlib.import_module('.tmp',package='seelab_examples')  

                if self.current_script:
                    self.current_script.close()  # Close the current script if it's open
                self.current_script = self.module.Expt(self.device)  # Create an instance of the Expt class
                self.central_widget.addWidget(self.current_script)  # Add the new script's window to the central widget
                self.central_widget.setCurrentWidget(self.current_script)  # Show the new script's window

                # Change button to "Edit Code" with edit icon
                self.run_code_button.setText("Edit Code")
                self.run_code_button.setIcon(QtGui.QIcon(os.path.join("icons","edit_icon.png")))  # Set edit icon

        else:
            self.load_script('tmp')
            self.setEditMode()

    def add_ipython_console(self):
        """Create and add an IPython console widget to the main window."""
        from qtconsole.rich_jupyter_widget import RichJupyterWidget
        from qtconsole.inprocess import QtInProcessKernelManager

        class myConsole(RichJupyterWidget):
            def __init__(self,customBanner=None):
                """Start a kernel, connect to it, and create a RichJupyterWidget to use it
                """
                super(myConsole, self).__init__()
                if customBanner is not None:
                    self.banner=customBanner
                self.kernel_manager = QtInProcessKernelManager(kernel_name='python3')

                self.kernel_manager.start_kernel()
                self.kernel = self.kernel_manager.kernel

                self.kernel_manager.kernel.gui = 'qt'
                self.font_size = 8

                self.kernel_client = self.kernel_manager.client()
                self.kernel_client.start_channels()

                def stop():
                    self.kernel_client.stop_channels()
                    self.kernel_manager.shutdown_kernel()
                    #guisupport.get_app_qt().exit()

                self.exit_requested.connect(stop)

            def pushVariables(self,variableDict):
                """ Given a dictionary containing name / value pairs, push those variables to the IPython console widget """
                self.kernel.shell.push(variableDict)
            def clearTerminal(self):
                """ Clears the terminal """
                self._control.clear()    

            def printText(self,text):
                """ Prints some plain text to the console """
                self._append_plain_text(text)

            def executeCommand(self,command,hidden=False):
                """ Execute a command in the frame of the console widget """
                self._execute(command,hidden)


        if self.current_script:
            self.current_script.close()  # Close the currently loaded script

        try:
            #--------instantiate the iPython class-------
            if self.ipyConsole is None:
                self.ipyConsole = myConsole("################ Interactive Console ###########\nAccess hardware using the Instance 'p'.  e.g.  p.get_voltage('A1')\n\n")
                self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
                self.text_editor = QtWidgets.QTextEdit()
                self.text_editor_highlighter = PythonHighlighter(self.text_editor.document())  # Syntax highlighting

                self.splitter.addWidget(self.ipyConsole)
                self.splitter.addWidget(self.text_editor)
                self.splitter.setSizes([4,2])

                self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
                self.toolbar.addSeparator()
                self.central_widget.addWidget(self.splitter)
                cmdDict = {}
                #cmdDict = {"analytics":self.analytics}
                if self.device :
                    cmdDict["p"]=self.device
                    import matplotlib.pyplot as plt
                    cmdDict["plt"]=plt
                self.ipyConsole.pushVariables(cmdDict)
                self.console_enabled=True
                self.createPythonCodeOptionsMenu()

                # Create a toolbar for script selection
                #self.toolbar = self.addToolBar("Simple Scripts")
                self.simple_script_selector = QtWidgets.QComboBox(self)
                self.toolbar.addWidget(self.simple_script_selector)
                self.load_available_baremetal_scripts()
                self.simple_script_selector.currentTextChanged.connect(self.load_simple_script)

                self.execute_button = QtWidgets.QPushButton()
                self.execute_button.setIcon(QtGui.QIcon(os.path.join("icons","play_icon.png")))
                self.execute_button.clicked.connect(self.execute_simple_script)
                self.toolbar.addWidget(self.execute_button)
                # Undock toolbar and position top right of window
                self.toolbar.setMovable(True)
                self.toolbar.setFloatable(True)  # Enables floating mode
                #self.toolbar.setParent(None)  
                #self.toolbar.setWindowFlags(QtCore.Qt.Tool)  # Makes it a tool window
                #self.toolbar.show()              # Ensure visibility
                #self.toolbar.move(600, 50)      # Position the floating toolbar window

            self.central_widget.setCurrentWidget(self.splitter)  # Show the source code editor

        except Exception as e:
            print ("failed to launch iPython. Is it installed?", e)
            self.close()
            
    def createPythonCodeOptionsMenu(self):
        self.theme_menu = self.menuBar().addMenu("Code Options")
        self.theme_menu.setIcon(QtGui.QIcon(os.path.join("icons","python_logo.png")))  # Set Python logo icon

        action = QtWidgets.QAction("Inline Plots", self)
        action.triggered.connect(partial(self.ipyConsole.execute,'%matplotlib inline' ))
        self.theme_menu.addAction(action)

        action = QtWidgets.QAction("Import Numpy", self)
        action.triggered.connect(partial(self.ipyConsole.execute,'import numpy as np' ))
        self.theme_menu.addAction(action)

    def setEditMode(self):
        self.run_code_button.setText("Run Code")
        self.run_code_button.setIcon(QtGui.QIcon(os.path.join("icons","play_icon.png")))  # Set play icon
        self.editMode = True
        if self.current_script:
            self.current_script.close()  # Close the current script if it's open

    ##############################
    def setTheme(self, theme):
        print('Change Theme',theme)
        self.setStyleSheet("")
        self.setStyleSheet(open(os.path.join(os.path.dirname(__file__),'themes', theme + ".qss"), "r").read())


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description='Run a specific script from seelab_examples.')
    script_names = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) if f.endswith('.py') and f not in ['script_runner.py', 'syntax.py', 'syntax2.py', 'tmp.py', '__main__.py','__init__.py','utils.py']]
    parser.add_argument('script', nargs='?', choices=script_names, help='The name of the script to run')
    args = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)
    window = ScriptRunner(args)
    window.show()
    sys.exit(app.exec_())