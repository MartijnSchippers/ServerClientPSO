from flask import Flask, request, jsonify
from PSO import PSO

class Application:
    pso : PSO

    def __init__(self, app=None):
        self.pso = PSO()
        if app is not None:
            self.define_routes(app)

    def define_routes(self, app):
        self.app = app

        # ROUTES
        @app.route('/compute', methods=['GET'])
        def send_computation_parameters():
            # For demonstration purposes, let's assume the result is a dummy value
            return self.pso.receive_random_particle_JSON()

        @app.route('/submit', methods=["POST"])
        def get_submission():
            resp = request.get_json()
            self.pso.update_fitness_value(resp["particle_id"], resp["generation"], resp["run_id"], resp["answer"])
            print("CLIENT: ", request.get_json())
            return "Thank you :)"