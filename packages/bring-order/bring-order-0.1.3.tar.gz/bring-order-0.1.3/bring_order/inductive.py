"""Class for Inductive analysis"""
from ipywidgets import widgets
from IPython.display import display

class Inductive:
    """Class that guides inductive analysis"""
    def __init__(self, bogui, boutils):
        """Class constructor."""
        self.bogui = bogui
        self.utils = boutils
        self.cell_count = 0
        self.buttons = self.bogui.init_buttons(self.button_list)
        self.add_cells_int = self.bogui.create_int_text()
        self.notes = self.bogui.create_text_area()
        self.cell_operations = self.create_cell_operations()
        self.conclusion = None
        self.empty_notes_error = self.bogui.create_error_message()
        self.observations = []

    @property
    def button_list(self):
        """Buttons for Inductive class.

        Returns:
            list of tuples in format (description: str, command: func, style: str) """
        button_list = [('Open cells', self.open_cells, 'warning'),
                   ('Delete last cell', self.delete_last_cell, 'danger'),
                   ('Clear cells', self.clear_cells, 'danger'),
                   ('Run cells', self.run_cells, 'primary'),
                   ('New analysis', self.start_new_analysis, 'success'),
                   ('Ready', self.execute_ready, 'primary'),
                   ('Submit observation', self.new_observation, 'warning'),
                   ('Prepare new data', self.prepare_new_data_pressed, 'success')
                   ]

        return button_list

    def open_cells(self, _=None):
        """Open cells button function that opens the selected
        number of code cells"""
        self.cell_count += self.add_cells_int.value + 1
        self.utils.create_code_cells_above(self.add_cells_int.value)


    def delete_last_cell(self, _=None):
        """Delete last cell-button function"""
        if self.cell_count > 0:
            self.utils.delete_cell_above()
            self.cell_count -= 1

    def clear_cells(self, _=None):
        """Clears all code cells above."""
        self.utils.clear_code_cells_above(self.cell_count)

    def run_cells(self, _=None):
        """Executes cells above and displays text area for observations of analysis."""
        self.utils.run_cells_above(self.cell_count)
        if self.conclusion:
            self.conclusion.close()

        notes_label = self.bogui.create_label(value='Explain what you observed:')
        self.conclusion = widgets.VBox([widgets.HBox(
                [notes_label, self.notes]),
                self.buttons['Submit observation'],
                self.buttons['Ready'], self.empty_notes_error
                ])

        display(self.conclusion)

    def new_observation(self, _=None):
        '''Checks new observation'''
        if self.check_notes():
            self.conclusion.close()
        else:
            self.empty_notes_error.value = 'Observation field can not be empty'

    def start_new_analysis(self, _=None):
        """Starts new bringorder object with old data"""
        command = 'BringOrder(data_import=False)'
        self.utils.create_and_execute_code_cell(command)

    def prepare_new_data_pressed(self, _=None):
        '''Starts new analysis with importing new data'''
        command = 'BringOrder(data_import=True)'
        self.utils.create_and_execute_code_cell(command)

    def execute_ready(self, _=None):
        """Executes code cells after Get summary button is clicked."""
        if self.check_notes():
            self.display_summary()
            self.new_analysis()
        else:
            self.empty_notes_error.value = 'Observation field can not be empty'

    def display_summary(self):
        """Prints all observations"""
        observation_string = ''.join((f"Observation {i+1}: {observation}\n") for i, observation
                 in enumerate(self.observations))
        text = f'''All your observations from the data:\n {observation_string}'''
        print(text)

        self.cell_operations.close()
        self.conclusion.close()

    def check_notes(self):
        '''Checks that text field was filled'''
        if self.notes.value == '':
            return False

        self.observations.append(self.notes.value)
        return True

    def create_cell_operations(self):
        """Displays buttons for operations in inductive analysis"""
        cell_number_label = self.bogui.create_label('Add code cells for your analysis:')

        grid = widgets.AppLayout(
            left_sidebar=widgets.HBox([cell_number_label, self.add_cells_int]),
            right_sidebar=widgets.TwoByTwoLayout(top_left=self.buttons['Open cells'],
                                                 bottom_left=self.buttons['Run cells'],
                                                 top_right=self.buttons['Delete last cell'],
                                                 bottom_right=self.buttons['Clear cells']),
            height='auto', width='70%')
        return grid

    def start_inductive_analysis(self):
        """Starts inductive analysis"""
        display(self.cell_operations)

    def new_analysis(self):
        '''Display buttons to start a new analysis or prepare new data for analysis'''
        display(widgets.HBox([self.buttons['New analysis'], self.buttons['Prepare new data']]))

    def __repr__(self):
        return ''
