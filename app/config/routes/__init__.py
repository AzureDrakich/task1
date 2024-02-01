from app.config.routes.routes import Routes
from app.internal import person, article
__routes__ = Routes(routers=(person.router,article.router))