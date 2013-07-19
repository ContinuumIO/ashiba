import enaml
from enaml.web.api import WebApplication

def main():
    with enaml.imports():
        from myapp import Main

    app = WebApplication()

    view = Main(message="Hello World, from Python!")
    view.show()

    # Start the application event loop
    app.start()

if __name__ == "__main__":
    main()
