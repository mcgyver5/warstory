from burp import IBurpExtender
from burp import ITab
from javax.swing import JButton
from javax.swing import JTabbedPane
from javax.swing import JSplitPane
from javax.swing import JFileChooser
from javax.swing import JLabel
from javax.swing import JPanel
from javax.swing import JScrollPane
from javax.swing import JTable
from javax.swing.table import AbstractTableModel
from javax.swing.table import TableColumnModel
from javax.swing.filechooser import FileFilter
from javax.swing.filechooser import FileNameExtensionFilter
from java.io import PrintWriter
from java.lang import RuntimeException

class BurpExtender(IBurpExtender, ITab,AbstractTableModel):
    
    
    #
    # implement IBurpExtender
    #
    
    def	registerExtenderCallbacks(self, callbacks):
    
        # set our extension name
        callbacks.setExtensionName("Hello world extension")
        
        # obtain our output and error streams
        stdout = PrintWriter(callbacks.getStdout(), True)
        stderr = PrintWriter(callbacks.getStderr(), True)
        
        # write a message to our output stream
        stdout.println("Loading WarStory")
        
        # write a message to our error stream
        stderr.println("Hello errors")
        
        # write a message to the Burp alerts tab
        callbacks.issueAlert("Hello alerts")
        label = JLabel("INFO PANEL") 
        infoPanel = JPanel() 
        footerPanel = JPanel()
        footerPanel.add(JLabel("by Tim mcgyver5 McGuire"))
        self._chooseFileButton = JButton("OPEN WAR FILE", actionPerformed=self.fileButtonClick)
        infoPanel.add(JLabel("THIS IS INFORMATION PANE"))
        infoPanel.add(self._chooseFileButton)
        
        self._chooseFileButton.setEnabled(True)
        fileTable = JTable(self)
        scrollpane = JScrollPane(fileTable)
        
        ## this is a split inside the top component
        topPane = JSplitPane(JSplitPane.VERTICAL_SPLIT)
        
        topPane.setTopComponent(infoPanel)
        topPane.setBottomComponent(scrollpane)

        # split the top panel into a Panel and a JScrollPane

        self._splitpane = JSplitPane(JSplitPane.VERTICAL_SPLIT)
        self._splitpane.setTopComponent(topPane)
        self._splitpane.setBottomComponent(footerPanel)

        callbacks.addSuiteTab(self)
        
    def fileButtonClick(self, e):
        
        fileTypeList = ["war","ear","zip"]
        warFilter = FileNameExtensionFilter("war", fileTypeList)
        fileChooser = JFileChooser()
        fileChooser.addChoosableFileFilter(warFilter)
        result = fileChooser.showOpenDialog(self._splitpane)
        if result == JFileChooser.APPROVE_OPTION:
             f = fileChooser.getSelectedFile()
             fileName = f.getPath()
		
    # Implement ITab
    def getTabCaption(self):
        return "War Story"
        
    def getUiComponent(self):
        return self._splitpane
        
    def getRowCount(self):
        try:
            return 5
        except:
            return 0
    
    def getColumnCount(self):
        return 5
        
    def getValueAt(self, rowIndex, columnIndex):
        return "_"
        
    #Implement AbstractTableModel
    # _	_	_	_	_
    def getColumnName(self, columnIndex):
        if columnIndex == 0:
            return "file name"
        if columnIndex == 1:
            return "path"
        if columnIndex == 2:
            return "servlet"
        if columnIndex == 3:
            return "parameter"
        if columnIndex == 4:
            return "new?"
