from app.config.routes.routes import Routes
from app.internal import person, article, comments, chat
__routes__ = Routes(routers=(person.router,article.router, comments.router, chat.router))