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
        self.hypothesis_input = self.bogui.create_input_field()
        self.empty_hypo_error = self.bogui.create_error_message()
        self.null_input = self.bogui.create_input_field()
        self.empty_null_error = self.bogui.create_error_message()
        self.hypotheses_grid = self.create_hypotheses_grid()
        self.add_cells_int = self.bogui.create_int_text()
        self.confirmed_grid = None
        self.conclusion = None
        self.data_limitations = 'Data limitations missing'
        self.limitation_prompt = None

    def create_hypotheses_grid(self):
        """Creates widgets"""
        hypothesis_label = self.bogui.create_label('Hypothesis:')
        null_label = self.bogui.create_label('Null hypothesis:')
        save_button = self.bogui.create_button(
            desc='Save',
            command=self.check_data_limitations)
        clear_button = self.bogui.create_button(
            desc='Clear',
            command=self.clear_hypotheses,
            style='primary')
        empty = self.bogui.create_placeholder()

        grid = self.bogui.create_grid(
            5,
            2,
            [empty,
             self.empty_hypo_error,
             hypothesis_label,
             self.hypothesis_input,
             null_label,
             self.null_input,
             empty,
             self.empty_null_error,
             empty,
             widgets.HBox(
                [save_button, clear_button])
            ])

        return grid

    def start_deductive_analysis(self, _=None):
        """Button function for deductive analysis"""
        display(self.hypotheses_grid)
        self.hypothesis_input.focus()

    def check_data_limitations(self, _=None):
        """Displays the prompt for the check against data limitations"""
        #print('checking limits: ' + self.data_limitations) #This is for debugging
        self.limitation_prompt_text = widgets.HTML(
            'Do the hypotheses fit within the limitations of the data set?' 
            + '<br>'
            + self.data_limitations)
        valid_hypotheses_button = self.bogui.create_button(
            desc='Yes',
            command=self.valid_hypotheses
        )
        bad_hypotheses_button = self.bogui.create_button(
            desc='No',
            command=self.bad_hypotheses,
            style='warning'
        )
        self.limitation_prompt = widgets.VBox(
            [
            self.limitation_prompt_text,
            widgets.HBox([
                valid_hypotheses_button, bad_hypotheses_button
                ])
            ]
        )
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
        if len(self.hypothesis_input.value) > 0 and len(self.null_input.value) > 0:
            return True

        if self.hypothesis_input.value == '':
            self.empty_hypo_error.value = 'Hypothesis missing'
        else:
            self.empty_hypo_error.value = ''

        if self.null_input.value == '':
            self.empty_null_error.value = 'Null hypothesis missing'
        else:
            self.empty_null_error.value = ''

        return False

    def save_hypotheses(self, _=None):
        """Saves hypotheses and displays buttons for running code"""
        hypotheses = f'- Hypothesis: {self.hypothesis_input.value}\\n- Null hypothesis: {self.null_input.value}'
        text = f'# Deductive analysis\\n## Hypotheses\\n{hypotheses}\\n## Data analysis'
        if self.check_hypotheses():
            self.boutils.create_markdown_cells_above(1, text=text)
            confirmed_hypothesis = self.bogui.create_message(
                value=f'Hypothesis: {self.hypothesis_input.value}')
            confirmed_null = self.bogui.create_message(
                value=f'Null hypothesis: {self.null_input.value}')
            self.confirmed_grid = self.create_confirmed_grid(
                confirmed_hypothesis,
                confirmed_null)
            self.hypotheses_grid.close()
            display(self.confirmed_grid)

    def clear_hypotheses(self, _=None):
        """Button function for resetting hypothesis and null hypothesis inputs"""
        self.hypothesis_input.value = ''
        self.null_input.value = ''
        self.empty_hypo_error.value = ''
        self.empty_null_error.value = ''
        self.hypothesis_input.focus()

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
            if self.cell_count > 0:
                self.boutils.delete_cell_above()
                self.cell_count -= 1

        button = self.bogui.create_button(
            desc='Delete last cell',
            command=delete_last_cell,
            style='danger')

        return button

    def create_run_button(self, hypothesis, null_hypothesis):
        """Creates button"""
        def run_cells(_=None):
            """Button function"""
            self.boutils.run_cells_above(
                self.cell_count)

            if self.conclusion:
                self.conclusion.close()

            conclusion_label = self.bogui.create_message(
                value='Accepted hypothesis:')
            conclusion = self.bogui.create_radiobuttons(
                options=[hypothesis.value, null_hypothesis.value])
            new_analysis_button = self.create_new_analysis_button(
                conclusion)
            new_data_button = self.create_new_data_button(conclusion)
            all_done_button = self.create_all_done_button(conclusion)
            self.conclusion = widgets.AppLayout(
                left_sidebar=conclusion_label,
                center=conclusion,
                footer=widgets.HBox([new_analysis_button, new_data_button, all_done_button])
            )

            display(self.conclusion)

        button = self.bogui.create_button(
            desc='Run cells',
            command=run_cells,
            style='primary')

        return button

    def create_clear_button(self):
        """Creates button"""
        def clear_cells(_=None):
            """Button function"""
            self.boutils.clear_code_cells_above(
                self.cell_count)

        button = self.bogui.create_button(
            desc='Clear cells',
            command=clear_cells,
            style='danger')
        return button

    def create_confirmed_grid(self, hypothesis, null_hypothesis):
        """Creates widget grid"""
        cell_number_label = self.bogui.create_label(
            'Add code cells for your analysis:')

        open_cells_button = self.create_open_cells_button()
        delete_cell_button = self.create_delete_button()
        run_cells_button = self.create_run_button(hypothesis, null_hypothesis)
        clear_cells_button = self.create_clear_button()

        grid = widgets.GridspecLayout(
            2,
            2,
            justify_items='center',
            width='70%',
            align_items='top')
        grid[1, 0] = widgets.HBox(
            [cell_number_label, self.add_cells_int])
        grid[1, 1] = widgets.TwoByTwoLayout(
            top_left=open_cells_button,
            bottom_left=run_cells_button,
            top_right=delete_cell_button,
            bottom_right=clear_cells_button)

        return grid

    def save_results(self, confirmed):
        """Prints results and hides widgets"""
        text = f'## Conclusion\\nAccepted: {confirmed.value}'
        self.boutils.create_markdown_cells_above(1, text=text)
        self.confirmed_grid.close()
        self.conclusion.close()

    def create_new_analysis_button(self, radio):
        """Creates button
        
        Args:
            radio (radiobutton): the hypothesis radiobutton widget
        """
        def start_new_analysis(_=None):
            """Button function"""
            self.save_results(radio)
            self.start_new()

        button = self.bogui.create_button(
            desc='New analysis',
            command=start_new_analysis)

        return button

    def create_new_data_button(self, radio):
        """Creates button
        
        Args:
            radio (radiobutton): the hypothesis radiobutton widget
        """

        def start_analysis_with_new_data(_=None):
            """Button function"""
            self.save_results(radio)
            self.boutils.execute_cell_from_current(1, 'BringOrder()')

        button = self.bogui.create_button(
            desc='Prepare new data',
            command=start_analysis_with_new_data
        )

        return button

    def create_all_done_button(self, radio):
        """Creates button
        
        Args:
            radio (radiobutton): the hypothesis radiobutton widget
        """

        def all_done(_=None):
            self.save_results(radio)
            self.boutils.delete_cell_from_current(1)

        button = self.bogui.create_button(
            desc='All done',
            command=all_done
        )

        return button

    def __repr__(self):
        return ''
