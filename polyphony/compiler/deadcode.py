from .ir import *
from logging import getLogger
logger = getLogger(__name__)


class DeadCodeEliminator(object):
    def process(self, scope):
        if scope.is_namespace() or scope.is_class() or scope.is_method():
            return
        usedef = scope.usedef
        for blk in scope.traverse_blocks():
            dead_stms = []
            for stm in blk.stms:
                if stm.is_a([MOVE, PHIBase]):
                    if stm.is_a(MOVE) and stm.src.is_a([TEMP, ATTR]) and stm.src.symbol().is_param():
                        continue
                    if stm.is_a(MOVE) and stm.src.is_a(CALL):
                        continue
                    defvars = usedef.get_vars_defined_at(stm)
                    for var in defvars:
                        if not var.is_a(TEMP):
                            break
                        uses = usedef.get_stms_using(var.symbol())
                        if uses:
                            break
                    else:
                        dead_stms.append(stm)
            for stm in dead_stms:
                blk.stms.remove(stm)
                logger.debug('removed dead code: ' + str(stm))
