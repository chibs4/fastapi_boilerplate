from db.init_db import *

startup_callbacks = (init_db,)
shutdown_callbacks = (close_db,)
