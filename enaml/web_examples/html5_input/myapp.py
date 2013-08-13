
import enaml
from enaml.web.api import WebApplication

def main():
    with enaml.imports():
        from myapp import Main

    view = Main()
    view.show()
    
    app = WebApplication()
    app.start()

if __name__ == "__main__":
    main()