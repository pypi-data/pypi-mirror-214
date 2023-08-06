from unittest import TestCase

from pydantic import BaseModel, ValidationError

from compo.compo import Compo

# I have forgot my intention by getting lost in the details.
# Should start with writing README or a unittests.

# The intention is to modify the JSON and get the DOM changes with the given values.
# Also you could save the methods.



class ComponentTests(TestCase):
    """Could I have a single Compo class for both list and dict?

    It might be that yes, so lets create first iteration with the Dict example.
    The Compo class should be a dictionary and thats it.
    """
    maxDiff = None

    def test_html_rendering_using_jinja2_of_compo_dictionary(self):
        """Component as a document"""
        # Component should get its name, template, state.
        # The result should be rendered state.

        # Model should pri

        class ProfileModel(BaseModel):
            first_name: str
            last_name: str


        compo = Compo(
            name="profile", 
            template="<p>{{ first_name }}</p> <p>{{ last_name }}</p>",
            model=ProfileModel,  # This parameter should be optional.
            state={
                "first_name": "Foo",
                "last_name": "Bar",
            }
        )

        # Should type be provided?
        # State should be typed (model should be provided for that).
        rendered_html = compo.render()
        assert rendered_html == "<p>Foo</p> <p>Bar</p>"

    def test_validation_when_type_in_state_does_not_match_the_model(self):
        class ProfileModel(BaseModel):
            first_name: str
            last_name: str

        compo = Compo(
            name="profile", 
            template="<p>{{ first_name }}</p> <p>{{ last_name }}</p>",
            model=ProfileModel,
        )

        # Validation failes for incorrect types
        with self.assertRaises(ValidationError):
            compo.state = {
                "first_name": None,
                "last_name": None,
            }

        # Validation does not fail for correct types
        compo.state = {
            "first_name": "Foo",
            "last_name": "Bar",
        }



    # def test_component_hierarchy(self):
    #     pass

    ## Pydantic works just as I would like.
    # def test_pydentic_rendering_of_nested_components(self):
    #     assert Compo()

    ## Unit testų mini pamoka:
    #
    # def burk():
    #     burtų_rezultatas = "Burtai"
    #     burtų_rezultatas += " "
    #     burtų_rezultatas += "buria"
    #     burtų_rezultatas += "!"
    #     return burtų_rezultatas
    #
    # def test_burk_burtus(self):
    #     assert burk() == "Burtai buria"




    def test_component_tree_app_rendering_from_json(self):
        """ Main user story

        Developer defines components
        Defines their placement order.

        TODO:
        Assigns their state.
        Changes the state making the components to rerender.
        Routing: urls
        CRUD operations to sync with the backend
        Server side rendering during initial loading.
        button click action caching till the pyodide is loaded.
        Rendering the root componenet: how is it mounted to the existing file?  Python code has access to HTML dom during its execution, when its loaded during initial HTML page load in which the Python code is imported.
        """

        # Having
        component_tree_state = {
            "user": {
                "id": 1,
                "first_name": "Foo",
                "last_name": "Bar",
                "email": "foo@example.com",
            },
            "tasks": [
                {"title": "Do something challenging", "user": "users/1"},  # Could have cached information routing method
                {"title": "Get a certificate", "user": "users/1"},  # Could have cached information routing method
            ]
        }

        RootCompo = Compo(
            name="RootCompo", 
            template="""
        <p>{{ user.first_name }}</p> <p>{{ user.last_name }}</p>
        Tasks:
        <li>
        {% for task in tasks %}    <ul>{{ task.title }}</ul>
        {% endfor %}</li>
            """,
            # template="<ProfileCompo state=state />   <TaskList state=state />",
            # model=ProfileModel,  # This parameter should be optional.
            # state={
            #     "first_name": "Foo",
            #     "last_name": "Bar",
            # }
        )
        root_compo = RootCompo()  # It should be callable to be able to have several instances with a different state
        root_compo.state = component_tree_state

        # When
        root_compo_html = root_compo.render()

        # Then
        self.assertEqual(root_compo_html, """
        <p>Foo</p> <p>Bar</p>
        Tasks:
        <li>
            <ul>Do something challenging</ul>
            <ul>Get a certificate</ul>
        </li>
            """)


        # When:  component_tree_state is modified
        root_compo.state["tasks"].append(
            {"title": "Create your own business", "user": "users/1"},  # Could have cached information routing method
        )
        root_compo_html = root_compo.render()

        # Then:  rerendered component state contains changes in the state
        self.assertEqual(root_compo_html, """
        <p>Foo</p> <p>Bar</p>
        Tasks:
        <li>
            <ul>Do something challenging</ul>
            <ul>Get a certificate</ul>
            <ul>Create your own business</ul>
        </li>
            """)


        # A simple way of defining methods for components (state elements) (they could part of compo or part of state)

    def test_rendering_component_into_working_html(self):
        dom = """
        <head></head>
        <body>
            <RootCompo/>
        </body>
        """

        expected_dom = """
        <head></head>
        <body>
            <p>Foo</p> <p>Bar</p>
        </body>
        """


        # the state json should be components tree, but simple json should be able to be added into that tree.
        # When json is being added or editted, the Compo class should be created/updated with validation and component rerendering.
        # When json is added to the component tree - new component should be returned.
        # When json is editted the edited component should be returned, so that its methods could be accessed.
        RootCompo = Compo(
            name="RootCompo",  # Should be taken from the variable/class name, should use typing or something.
            template="""<p>{{ user.first_name }}</p> <p>{{ user.last_name }}</p>""")
        RootCompo.state = {"user": {"first_name": "Foo", "last_name": "Bar"}}


        # When
        rendered_dom = RootCompo.render_to_dom(dom)
        self.assertEqual(rendered_dom, expected_dom)

    def test_rendering_component_tree_into_working_html(self):
        pass





