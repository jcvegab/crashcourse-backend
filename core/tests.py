import json

from django.test import Client, TestCase, override_settings

from .models import Category, Course


class GraphQLContractTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Development")
        self.subcategory = Category.objects.create(name="Python", parent=self.category)
        self.course = Course.objects.create(
            name="Django 101",
            real_price="100.00",
            price="80.00",
            discount=20,
            level=1,
            score="4.50",
            tutor_username="teacher",
            users=10,
            category=self.category,
            subcategory=self.subcategory,
        )

    def graphql(self, query):
        return self.client.post(
            "/graphql/",
            data=json.dumps({"query": query}),
            content_type="application/json",
        )

    @staticmethod
    def render_type(type_ref):
        if type_ref["kind"] == "NON_NULL":
            return f"{GraphQLContractTests.render_type(type_ref['ofType'])}!"
        if type_ref["kind"] == "LIST":
            return f"[{GraphQLContractTests.render_type(type_ref['ofType'])}]"
        return type_ref["name"]

    def test_schema_contract(self):
        response = self.graphql(
            """
            {
              __schema {
                queryType { name }
                types {
                  name
                  fields {
                    name
                    args { name defaultValue type { kind name ofType { kind name ofType { kind name } } } }
                    type { kind name ofType { kind name ofType { kind name } } }
                  }
                }
              }
            }
            """
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("errors", response.json())
        types = {item["name"]: item for item in response.json()["data"]["__schema"]["types"]}

        self.assertEqual(response.json()["data"]["__schema"]["queryType"]["name"], "Query")
        self.assertEqual(
            {field["name"] for field in types["Query"]["fields"]},
            {"course", "courses", "category", "categories"},
        )
        self.assertEqual(
            {field["name"] for field in types["CourseType"]["fields"]},
            {
                "id",
                "name",
                "realPrice",
                "price",
                "discount",
                "level",
                "score",
                "tutorUsername",
                "users",
                "category",
                "subcategory",
            },
        )
        self.assertEqual(
            {field["name"] for field in types["CategoryType"]["fields"]},
            {"id", "name", "parent", "categorySet", "courses", "subcourses"},
        )
        query_fields = {field["name"]: field for field in types["Query"]["fields"]}

        self.assertEqual(self.render_type(query_fields["course"]["type"]), "CourseType")
        self.assertEqual(self.render_type(query_fields["courses"]["type"]), "[CourseType]")
        self.assertEqual(self.render_type(query_fields["category"]["type"]), "CategoryType")
        self.assertEqual(self.render_type(query_fields["categories"]["type"]), "[CategoryType]")
        self.assertEqual(self.render_type(query_fields["course"]["args"][0]["type"]), "Int")
        self.assertIsNone(query_fields["course"]["args"][0]["defaultValue"])
        course_fields = {field["name"]: field for field in types["CourseType"]["fields"]}
        self.assertEqual(self.render_type(course_fields["level"]["type"]), "Int!")

    def test_course_queries_preserve_scalars_and_relationships(self):
        response = self.graphql(
            f"""
            {{
              course(id: {self.course.id}) {{
                id name realPrice price discount level score tutorUsername users
                category {{ name }}
                subcategory {{ name parent {{ name }} }}
              }}
              courses {{ id }}
            }}
            """
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["data"]["course"],
            {
                "id": str(self.course.id),
                "name": "Django 101",
                "realPrice": "100.00",
                "price": "80.00",
                "discount": 20,
                "level": 1,
                "score": "4.50",
                "tutorUsername": "teacher",
                "users": 10,
                "category": {"name": "Development"},
                "subcategory": {"name": "Python", "parent": {"name": "Development"}},
            },
        )
        self.assertEqual(response.json()["data"]["courses"], [{"id": str(self.course.id)}])

    def test_category_queries_and_missing_records(self):
        response = self.graphql(
            f"""
            {{
              category(id: {self.category.id}) {{
                name categorySet {{ name }} courses {{ name }} subcourses {{ name }}
              }}
              categories {{ name }}
              missingCourse: course(id: 9999) {{ id }}
              missingCategory: category(id: 9999) {{ id }}
            }}
            """
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["data"]["category"],
            {
                "name": "Development",
                "categorySet": [{"name": "Python"}],
                "courses": [{"name": "Django 101"}],
                "subcourses": [],
            },
        )
        self.assertEqual(response.json()["data"]["categories"], [{"name": "Development"}, {"name": "Python"}])
        self.assertIsNone(response.json()["data"]["missingCourse"])
        self.assertIsNone(response.json()["data"]["missingCategory"])

    def test_graphql_post_is_csrf_exempt(self):
        response = Client(enforce_csrf_checks=True).post(
            "/graphql/",
            data=json.dumps({"query": "{ courses { id } }"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("errors", response.json())

    @override_settings(DEBUG=True)
    def test_graphiql_is_available_in_debug_mode(self):
        response = self.client.get("/graphql/", HTTP_ACCEPT="text/html")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"GraphiQL", response.content)

    @override_settings(DEBUG=False)
    def test_graphiql_is_not_available_outside_debug_mode(self):
        response = self.client.get("/graphql/", HTTP_ACCEPT="text/html")

        self.assertNotIn(b"GraphiQL", response.content)


class RestSmokeTests(TestCase):
    def test_api_root(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "CrashCourse API", "version": "0.1.0"})

    def test_login_and_refresh(self):
        login_response = self.client.post(
            "/auth/login/",
            data=json.dumps({"username": "learner", "password": "secret"}),
            content_type="application/json",
        )
        refresh_response = self.client.post("/auth/refresh/")

        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(
            login_response.json(),
            {
                "access": "mock-access-token",
                "refresh": "mock-refresh-token",
                "user": {"id": 1, "username": "learner"},
            },
        )
        self.assertEqual(refresh_response.status_code, 200)
        self.assertEqual(refresh_response.json(), {"access": "mock-access-token-refreshed"})
