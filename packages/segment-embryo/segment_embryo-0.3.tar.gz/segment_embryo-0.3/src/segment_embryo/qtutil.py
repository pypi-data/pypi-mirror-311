from qtpy.QtWidgets import QLabel, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QAction

class WidgetTool:
    """
    Utility methods for working with qt-widgets.
    """

    @staticmethod
    def getLineInput(parent, labelText, defaultValue, fieldWidth, callback=None):
        """Returns a label displaying the given text and an input field
        with the given default value.

        :param parent: The parent widget of the label and the input field
        :param labelText: The text of the label
        :param defaultValue: The value initially displayed in the input field
        :param fieldWidth: The width of the input field
        :param callback: A callback function with a parameter text. The function
                         is called with the new text when the content of the
                         input field changes
        :return: A tupel of the label and the input field
        :rtype: (QLabel, QLineEdit)
        """
        label = QLabel(parent)
        label.setText(labelText)
        input = QLineEdit(parent)
        input.setText(str(defaultValue))
        if callback:
            input.textChanged.connect(callback)
        input.setMaximumWidth(fieldWidth)
        return label, input


    @staticmethod
    def getComboInput(parent, labelText, values):
        """Returns a label displaying the given text and a combo-box
        with the given values.

        :param parent: The parent widget of the label and the input field
        :param labelText: The text of the label
        :param values: The values in the list of the combo-box
        :return: A tupel of the label and the input field
        :rtype: (QLabel, QComboBox)
        """
        label = QLabel(parent)
        label.setText(labelText)
        input = QComboBox(parent)
        input.addItems(values)
        return label, input


    @staticmethod
    def replaceItemsInComboBox(comboBox, newItems):
        """Replace the items in the combo-box with newItems

        :param comboBox: The combo-box in which the items will be replaced
        :param newItems: The new items that will replace the current items
                         in the combo-box.
        """
        selectedText = comboBox.currentText()
        comboBox.clear()
        comboBox.addItems(newItems)
        index = -1
        try:
            index = newItems.index(selectedText)
        except ValueError:
            index = -1
        if index > -1:
            comboBox.setCurrentIndex(index)



