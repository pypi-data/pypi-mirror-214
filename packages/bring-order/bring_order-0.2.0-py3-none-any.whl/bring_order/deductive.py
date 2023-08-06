"""Deductive class"""
from ipywidgets import widgets
from IPython.display import display

class Deductive:
    """Class that guides deductive analysis"""
    def __init__(self, bogui, boutils, start_new):
        """Class constructor
        
        Args:
            bogui (BOGui)
            boutils (BOUtils)
            start_new (function): Function to start new analysis with same data
        """
        self.cell_count = 0
        self.start_new = start_new
        self.bogui = bogui
        self.boutils = boutils
        self.buttons = self.bogui.init_buttons(self.button_list)
        #List of hypotheses: 0 = hypothesis, 1 = null hypothesis
        self.hypotheses = [self.bogui.create_input_field(), self.bogui.create_input_field()]
        self.empty_hypo_error = self.bogui.create_error_message()
        self.empty_null_error = self.bogui.create_error_message()
        self.hypotheses_grid = self.create_hypotheses_grid()
        self.add_cells_int = self.bogui.create_int_text()
        self.confirmed_grid = None
        self.conclusion = None
        self.data_limitations = ['Data limitations missing']
        self.limitation_prompt = None

    @property
    def button_list(self):
        """Buttons for deductive class.

        Returns:
            list of tuples in format (description: str, command: func, style: str)"""
        button_list = [('Open cells', self.open_cells, 'warning'),
                       ('Delete last cell', self.delete_last_cell, 'danger'),
                       ('Save', self.check_data_limitations, 'success'),
                       ('Clear', self.clear_hypotheses, 'primary'),
                       ('Yes', self.valid_hypotheses, 'success'),
                       ('No', self.bad_hypotheses, 'warning'),
                       ('Run cells', self.run_cells, 'primary'),
                       ('Clear cells', self.clear_cells, 'danger'),
                       ('New analysis', self.start_new_analysis, 'success'),
                       ('Prepare new data', self.start_analysis_with_new_data, 'success'),
                       ('All done', self.all_done, 'success')]
        return button_list

    def create_hypotheses_grid(self):
        """Creates widgets"""
        hypothesis_label = self.bogui.create_label('Hypothesis:')
        null_label = self.bogui.create_label('Null hypothesis:')
        empty = self.bogui.create_placeholder()

        grid = self.bogui.create_grid(5, 2,
            [empty, self.empty_hypo_error,
             hypothesis_label, self.hypotheses[0],
             null_label, self.hypotheses[1],
             empty, self.empty_null_error,
             empty, widgets.HBox([self.buttons['Save'], self.buttons['Clear']])
            ])
        return grid

    def start_deductive_analysis(self, _=None):
        """Button function for deductive analysis"""
        display(self.hypotheses_grid)
        self.hypotheses[0].focus()

    def check_data_limitations(self, _=None):
        """Displays the prompt for the check against data limitations"""
        #print('checking limits: ' + self.data_limitations) #This is for debugging
        if self.check_hypotheses():
            limitations = ''.join(f"Limitation {count}: {item.value} <br>" for count, item in enumerate(self.data_limitations, start=1))

            limitation_prompt_text = widgets.HTML(
                'Do the hypotheses fit within the limitations of the data set?' 
                + '<br>' + limitations)

            self.limitation_prompt = widgets.VBox([limitation_prompt_text,
                widgets.HBox([self.buttons['Yes'], self.buttons['No']])
                ])
            display(self.limitation_prompt)

    def valid_hypotheses(self, _=None):
        """Closes the data limitation check prompt and calls save_hypotheses()"""
        self.limitation_prompt.close()
        self.save_hypotheses()

    def bad_hypotheses(self, _=None):
        """Closes the data limitation check prompt and calls clear_hypotheses()"""
        # TODO: set some error message for a hypothesis that doesn't fit
        # data limitations and ask the user for a better one
        self.limitation_prompt.close()
        self.clear_hypotheses()

    def check_hypotheses(self):
        """Checks that hypothesis and null hypothesis are not empty.

        Returns:
            True/False
        """
        if len(self.hypotheses[0].value) > 0 and len(self.hypotheses[1].value) > 0:
            return True

        if self.hypotheses[0].value == '':
            self.empty_hypo_error.value = 'Hypothesis missing'
        else:
            self.empty_hypo_error.value = ''

        if self.hypotheses[1].value == '':
            self.empty_null_error.value = 'Null hypothesis missing'
        else:
            self.empty_null_error.value = ''

        return False

    def save_hypotheses(self, _=None):
        """Saves hypotheses and displays buttons for running code"""
        hypotheses = f'- Hypothesis: {self.hypotheses[0].value}\
        \\n- Null hypothesis: {self.hypotheses[1].value}'
        text = f'# Deductive analysis\\n## Hypotheses\\n{hypotheses}\\n## Data analysis'
        if self.check_hypotheses():
            self.boutils.create_markdown_cells_above(1, text=text)
            self.confirmed_grid = self.create_confirmed_grid()
            self.hypotheses_grid.close()
            display(self.confirmed_grid)

    def clear_hypotheses(self, _=None):
        """Button function for resetting hypothesis and null hypothesis inputs"""
        self.hypotheses[0].value = ''
        self.hypotheses[1].value = ''
        self.empty_hypo_error.value = ''
        self.empty_null_error.value = ''
        self.hypotheses[0].focus()

    def open_cells(self, _=None):
        """Button function for opening new code cells"""
        if self.add_cells_int.value > 0:
            self.cell_count += self.add_cells_int.value
            self.boutils.create_code_cells_above(self.add_cells_int.value)

    def delete_last_cell(self, _=None):
        """Button function for deleting the last code cell"""
        if self.cell_count > 0:
            self.boutils.delete_cell_above()
            self.cell_count -= 1

    def deactivate_cell_operations(self):
        """Deactivates buttons after runnig code block"""
        self.buttons['Open cells'].disabled = True
        self.buttons['Clear cells'].disabled = True
        self.buttons['Delete last cell'].disabled = True

    def run_cells(self, _=None):
        """Button function"""
        self.boutils.run_cells_above(
            self.cell_count)
        self.deactivate_cell_operations()

        if self.conclusion:
            self.conclusion.close()

        question = self.bogui.create_message(value='What happened?')
        conclusion_label = self.bogui.create_message(value='Accepted hypothesis:')
        conclusion = self.bogui.create_radiobuttons(
            options=[f'Hypothesis: {self.hypotheses[0].value}',
                     f'Null hypothesis: {self.hypotheses[1].value}'])

        self.conclusion = widgets.AppLayout(
            header=question,
            left_sidebar=conclusion_label,
            center=conclusion,
            footer=widgets.HBox([
                self.buttons['New analysis'],
                self.buttons['Prepare new data'],
                self.buttons['All done']])
        )
        display(self.conclusion)

    def clear_cells(self, _=None):
        """Clear button function to clear cells above"""
        self.boutils.clear_code_cells_above(self.cell_count)

    def create_confirmed_grid(self):
        """Creates widget grid"""
        cell_number_label = self.bogui.create_label('Add code cells for your analysis:')

        grid = widgets.GridspecLayout(2, 2, justify_items='center', width='70%', align_items='top')
        grid[1, 0] = widgets.HBox([cell_number_label, self.add_cells_int])
        grid[1, 1] = widgets.TwoByTwoLayout(
            top_left=self.buttons['Open cells'],
            bottom_left=self.buttons['Run cells'],
            top_right=self.buttons['Delete last cell'],
            bottom_right=self.buttons['Clear cells'])

        return grid

    def save_results(self):
        """Prints results and hides widgets"""
        text = f'## Accepted hypothesis\\n{self.conclusion.center.value}'
        self.boutils.create_markdown_cells_above(1, text=text)
        self.confirmed_grid.close()
        self.conclusion.close()

    def start_new_analysis(self, _=None):
        """Button function to save results and star new analysis"""
        self.save_results()
        self.start_new()

    def start_analysis_with_new_data(self, _=None):
        """Button function to start over with new data"""
        self.save_results()
        self.boutils.execute_cell_from_current(1, 'BringOrder()')


    def all_done(self, _=None):
        """Button function to save results when ready."""
        self.save_results()
        self.boutils.delete_cell_from_current(1)

    def __repr__(self):
        return ''
