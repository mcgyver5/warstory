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

class BurpExtender(IBurpExtender, ITab):
    
    #
    # implement IBurpExtender
    #
    
    def	registerExtenderCallbacks(self, callbacks):
    
        # set our extension name
        callbacks.setExtensionName("Hello world extension")
        
        # obtain our output and error streams
        
        # obtain our output stream
        self._stdout = PrintWriter(callbacks.getStdout(), True)
        stdout = PrintWriter(callbacks.getStdout(), True)
        stderr = PrintWriter(callbacks.getStderr(), True)
        
        # write a message to our output stream
        stdout.println("Loading WarStory")
        
        # write a message to our error stream
        stderr.println("Hello errors")
        
        # write a message to the Burp alerts tab
        callbacks.issueAlert("Hello alerts")
        label = JLabel("INFO PANEL") 
        self.infoPanel = JPanel() 
        footerPanel = JPanel()
        footerPanel.add(JLabel("by Tim mcgyver5 McGuire"))
        self._chooseFileButton = JButton("OPEN WAR FILE", actionPerformed=self.fileButtonClick)
        self.infoPanel.add(JLabel("THIS IS INFORMATION PANE"))
        self.infoPanel.add(self._chooseFileButton)
        
        self._chooseFileButton.setEnabled(True)
        initial_row = ['a','bb','ccc','ddd','eeee']
        self.fileTable = JTable(ResourceTableModel(initial_row))
        scrollpane = JScrollPane(self.fileTable)
        
        ## this is a split inside the top component
        topPane = JSplitPane(JSplitPane.VERTICAL_SPLIT)
        
        topPane.setTopComponent(self.infoPanel)
        topPane.setBottomComponent(scrollpane)

        # split the top panel into a Panel and a JScrollPane

        self._splitpane = JSplitPane(JSplitPane.VERTICAL_SPLIT)
        self._splitpane.setTopComponent(topPane)
        self._splitpane.setBottomComponent(footerPanel)

        callbacks.addSuiteTab(self)
    
    def populateJTable(self, f):
        filename = f.getPath()
        tableModel = self.fileTable.getModel()
        test_row = ["a","b","doo","dah","dob"]
        re = Resource("Servlet", "bingServlet", "bingservlet.do", [], [], "GET")
        self._stdout.println("populatin table model")
        tableModel.addRow(test_row)
        
    
    def fileButtonClick(self, e):
        
        fileTypeList = ["war","ear","zip"]
        warFilter = FileNameExtensionFilter("war", fileTypeList)
        fileChooser = JFileChooser()
        fileChooser.addChoosableFileFilter(warFilter)
        result = fileChooser.showOpenDialog(self._splitpane)
        self._stdout.println("HERE IS result: " + str(result))
        self._stdout.println("HERE IS expectedResult: " + str(JFileChooser.APPROVE_OPTION))
        
        if result == JFileChooser.APPROVE_OPTION:
            self._stdout.println("APPROVE_OPTION DETECTED: " + str(JFileChooser.APPROVE_OPTION))
            f = fileChooser.getSelectedFile()
            fileName = f.getPath()
            self._stdout.println("File name is " + fileName)
            self.populateJTable(f)
        
      
		
    # Implement ITab
    def getTabCaption(self):
        return "War Story"
        
    def getUiComponent(self):
        return self._splitpane
        


class ResourceTableModel(AbstractTableModel):
    COLUMN_NAMES = ('File Name', 'path', 'servlet', 'parameter', 'header')
    ## *rows is one or more sets of data that each represent a resource found by this extension 
    def __init__(self, *rows):
        ## turn the data into a python list
        self.data = list(rows)
    def getValueAt(self, rowIndex, columnIndex):
        row_values = self.data[rowIndex-1]
        return row_values[columnIndex-1]
    def getRowCount(self):
        #self._stdout.println("rowcount is " + len(self.data))
        return len(self.data)
    def getColumnCount(self):
        return 5
        
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
    def addRow(self, row=None):
        #self._stdout.println("adding row")
        self.data.append(row or ['place','place','place','place','place'])
        self.fireTableRowsInserted(len(self.data) - 1, len(self.data) - 1)
class Resource:
    def __init__(self, resource_type, resource_name, file_path, param_list, header_list, http_method):
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.file_path = file_path
        self.param_list = param_list
        self.header_list = header_list
        self.http_method = http_method
        
