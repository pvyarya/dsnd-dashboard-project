from fasthtml.common import *
import matplotlib.pyplot as plt
import pandas as pd

# Import QueryBase, Employee, Team from employee_events
from employee_events import QueryBase, Employee, Team

# import the load_model function from the utils.py file
from report.utils import load_model

"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
    )

from combined_components import FormGroup, CombinedComponent


# Create a subclass of base_components/dropdown
# called `ReportDropdown`
class ReportDropdown(Dropdown):

    # Overwrite the build_component method
    def build_component(self, entity_id, model):
        # Set the `label` attribute so it is set
        # to the `name` attribute for the model
        self.label = model.name
        # Return the output from the parent class's build_component method
        return super().build_component(entity_id, model)

    # Overwrite the `component_data` method
    def component_data(self, entity_id, model):
        # Using the model argument
        # call the employee_events method
        # that returns the user-type's names and ids
        return model.names()


# Create a subclass of base_components/BaseComponent
# called `Header`
class Header(BaseComponent):

    def build_component(self, entity_id, model):
        # Using the model argument for this method
        # return a fasthtml H1 objects
        # containing the model's name attribute
        return H1(model.name)


# Create a subclass of base_components/MatplotlibViz
# called `LineChart`
class LineChart(MatplotlibViz):

    def visualization(self, entity_id, model):
        if not entity_id:
            return
        # Pass the `asset_id` argument to the model's `event_counts` method
        df = model.event_counts(entity_id)

        # Fill nulls with 0
        df = df.fillna(0)

        # Set the date column as the index
        df = df.set_index('event_date')

        # Sort the index
        df = df.sort_index()

        # Convert to cumulative counts
        df = df.cumsum()

        # Rename columns
        df.columns = ["Positive", "Negative"]

        # Initialize a matplotlib subplot
        fig, ax = plt.subplots()

        # Plot the cumulative counts
        df.plot(ax=ax)

        # Style axis
        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")

        # Set title and labels
        ax.set_title("Cumulative Event Counts")
        ax.set_xlabel("Day")
        ax.set_ylabel("Event Count")

        return fig


# Create a subclass of base_components/MatplotlibViz
# called `BarChart`
class BarChart(MatplotlibViz):

    # Predictor model
    predictor = load_model()

    def visualization(self, entity_id, model):
        # Get model data
        data = model.model_data(entity_id)

        # Get prediction probabilities
        prob = self.predictor.predict_proba(data)
        prob = prob[:,1]

        # pred depends on model type
        if model.name == "team":
            pred = prob.mean()
        else:
            pred = prob[0]

        # Initialize subplot
        fig, ax = plt.subplots()

        # Provided code
        ax.barh([""], [pred])
        ax.set_xlim(0, 1)
        ax.set_title("Predicted Recruitment Risk", fontsize=20)

        # Style axis
        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")

        return fig


# Create a subclass of combined_components/CombinedComponent
# called Visualizations
class Visualizations(CombinedComponent):

    # Children components
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls="grid")


# Create a subclass of base_components/DataTable
# called `NotesTable`
class NotesTable(DataTable):

    def component_data(self, entity_id, model):
        # Using the model and entity_id arguments
        # return the notes
        return model.notes(entity_id)


class DashboardFilters(FormGroup):

    id = "top-filters"
    action = "/update_data"
    method = "POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name="profile_type",
            hx_get="/update_dropdown",
            hx_target="#selector"
        ),
        ReportDropdown(
            id="selector",
            name="user-selection"
        )
    ]


# Create a subclass of CombinedComponents
# called `Report`
class Report(CombinedComponent):

    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        NotesTable()
    ]


# Initialize a fasthtml app
app = FastHTML()

# Initialize the `Report` class
report = Report()


# Create a route for a get request (root path)
@app.get("/")
def index():

    # Call the initialized report
    # pass the integer 1 and an instance
    # of the Employee class as arguments
    # Return the result
    return report(1, Employee())


# Route for employee page
@app.get('/employee/{employee_id}')
def employee_page(employee_id: str):

    # Call the initialized report
    # pass the ID and an instance
    # of the Employee SQL class as arguments
    # Return the result
    return report(employee_id, Employee())


# Route for team page
@app.get("/team/{team_id}")
def team_page(team_id: str):

    # Call the initialized report
    # pass the id and an instance
    # of the Team SQL class as arguments
    # Return the result
    return report(team_id, Team())


# Keep the below code unchanged!
@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)


serve()

