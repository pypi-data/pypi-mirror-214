'''Bring Order Data Import (and preparation). 
Creates code cells for importing and cleaning data and markdown cell to describe the limitations
and requirements of data. After code cells displays "ready to analyse" button. After button is 
pressed displays text field and "ready" button. Empty text field is not accepted.'''
from ipywidgets import widgets
from IPython.display import display


class Bodi:
    '''Creates code cells for importing data and markdown cell(s) to describe data limitations'''
    def __init__(self, boutils, bogui, start_analysis):
        """Class constructor
        """
        self.start_analysis = start_analysis
        self.boutils = boutils
        self.bogui = bogui
        self.cell_count = 0
        self.prepare_data_button = self.create_prepare_data_button()
        self.add_cells_int = self.bogui.create_int_text()
        self.import_grid = self.data_import_grid()
        self.data_limitations = self.bogui.create_text_area()
        self.limitation_grid = None
        self.empty_limitations_error = self.bogui.create_error_message()

    def data_import_grid(self):
        """Creates widget grid"""
        cell_number_label = self.bogui.create_label(
            'Add code cells for data preparation:')

        open_cells_button = self.create_open_cells_button()
        delete_cell_button = self.create_delete_button()
        run_cells_button = self.create_run_button()

        grid = widgets.HBox([
            cell_number_label,
            self.add_cells_int,
            open_cells_button,
            run_cells_button,
            delete_cell_button
        ])

        return grid

    def create_open_cells_button(self):
        """Creates button for opening new code cells for analysis.

        Returns:
            button
        """
        def open_cells(_=None):
            """Button function"""
            self.cell_count += self.add_cells_int.value
            self.boutils.create_code_cells_above(self.add_cells_int.value)

        button = self.bogui.create_button(
            desc='Open cells',
            command=open_cells,
            style='warning')

        return button

    def create_delete_button(self):
        """Creates button for deleting the last code cell

        Returns:
            button
        """
        def delete_last_cell(_=None):
            """Button function"""
            if self.cell_count > 1:
                self.boutils.delete_cell_above()
                self.cell_count -= 1

        button = self.bogui.create_button(
            desc='Delete last cell',
            command=delete_last_cell,
            style='danger')

        return button

    def create_run_button(self):
        """Creates button"""
        def run_cells(_=None):
            """Button function"""
            self.boutils.run_cells_above(
                self.cell_count)

            if self.limitation_grid:
                self.limitation_grid.close()

            limitations_label = self.bogui.create_message(
                value='Data limitations:')
            analyze_button = self.create_analysis_button()
            self.limitation_grid = widgets.AppLayout(
                left_sidebar=limitations_label,
                center=self.data_limitations,
                footer=widgets.HBox([analyze_button, self.empty_limitations_error])
            )

            display(self.limitation_grid)

        button = self.bogui.create_button(
            desc='Run cells',
            command=run_cells,
            style='primary')

        return button

    def check_limitations(self):
        '''Checks that limitations have been given or commented'''
        if self.data_limitations.value == '':
            return False
        return True

    def create_analysis_button(self):
        """Creates button"""
        def start_analysis(_=None):
            """Button function"""
            if self.check_limitations():
                limitations = self.data_limitations.value.replace('\n', '\\n')
                text = f'## Data limitations\\n{limitations}'
                self.boutils.create_markdown_cells_above(1, text=text)
                self.import_grid.close()
                self.limitation_grid.close()
                self.start_analysis()

            else:
                self.empty_limitations_error.value = 'Data limitations cannot be empty'

        button = self.bogui.create_button(
            'Start analysis',
            start_analysis
        )

        return button

    def create_prepare_data_button(self):
        """Creates button"""
        button = self.bogui.create_button(
            desc='Prepare your data',
            command=self.start_data_import,
            style='success'
        )

        return button

    def start_data_import(self, _=None):
        """Creates markdown for data description and shows buttons for data import"""
        self.boutils.hide_current_input()
        text = '# Data preparation\\n## Data description\\nDescribe your data here\\n## Data import and cleaning'
        self.boutils.create_markdown_cells_above(1, text=text)
        self.cell_count += 1
        self.prepare_data_button.close()
        display(self.import_grid)

    def bodi(self):
        '''Main function'''
        display(self.prepare_data_button)
