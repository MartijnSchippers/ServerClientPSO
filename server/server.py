"""
File: server.py
Date: 13-01-24
Description: This script defines a Flask application handling routes for Particle Swarm Optimization (PSO) and Rosenbrock PSO computations.
Author: Martijn Schippers
"""

from flask import Flask, request, jsonify
from PSO import PSO
from Rosenbrock_PSO import RosenbrockPSO

class Application:
    """
    The Application class manages the Flask application and defines routes for PSO and Rosenbrock PSO computations.

    Attributes:
        pso (PSO): Instance of the Particle Swarm Optimization class.
        rosenbrock_PSO (RosenbrockPSO): Instance of the Rosenbrock PSO class.
        app (Flask): Flask application instance.
    """

    def __init__(self, app=None):
        """
        Initialize the Application.

        Args:
            app (Flask, optional): Flask application instance. Defaults to None.
        """
        self.pso = PSO()
        self.rosenbrock_PSO = RosenbrockPSO()

        if app is not None:
            self.define_routes(app)

    def define_routes(self, app):
        """
        Define routes for the Flask application.

        Args:
            app (Flask): Flask application instance.
        """
        self.app = app

        @app.route('/compute', methods=['GET'])
        def send_computation_parameters():
            """
            Route: /compute
            Method: GET

            Send computation parameters for PSO.

            Returns:
                str: JSON representation of a random particle for PSO.
            """
            return self.pso.receive_random_particle_JSON()

        @app.route('/submit', methods=["POST"])
        def get_submission():
            """
            Route: /submit
            Method: POST

            Receive and process the submission of PSO computation results.

            Returns:
                str: Acknowledgment message.
            """
            resp = request.get_json()
            self.pso.update_fitness_value(resp["particle_id"], resp["generation"], resp["run_id"], resp["answer"])
            print("CLIENT: ", request.get_json())
            return "Thank you :)"

        @app.route('/rosenbrock/compute', methods=['GET'])
        def send_rosenbrock_parameters():
            """
            Route: /rosenbrock/compute
            Method: GET

            Send computation parameters for Rosenbrock PSO.

            Returns:
                str: JSON representation of a random particle for Rosenbrock PSO.
            """
            return self.rosenbrock_PSO.receive_random_particle_JSON()

        @app.route('/rosenbrock/submit', methods=["POST"])
        def get_rosenbrock_submission():
            """
            Route: /rosenbrock/submit
            Method: POST

            Receive and process the submission of Rosenbrock PSO computation results.

            Returns:
                str: Acknowledgment message.
            """
            resp = request.get_json()
            self.rosenbrock_PSO.update_fitness_value(resp["particle_id"], resp["generation"], resp["run_id"], resp["answer"])
            print("CLIENT: ", request.get_json())
            return "Thank you :)"
