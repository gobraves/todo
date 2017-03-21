from flask import Blueprint, Flask

def add_index(app, route_fn):
    @route_fn
    def root():
        """
        Serve SPA static page.
        """
        return app.send_static_file('index.html')