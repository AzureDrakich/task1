from app.config.routes.routes import Routes
from app.internal import person, article, comments
__routes__ = Routes(routers=(person.router,article.router, comments.router))