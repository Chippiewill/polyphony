from .ir import *
from .irhelper import reduce_relexp


class PHIInlining(object):
    def process(self, scope):
        self.phis = {}
        for blk in scope.traverse_blocks():
            for phi in blk.collect_stms([PHI, UPHI]):
                if not phi.var.symbol().is_induction():
                    self.phis[phi.var.symbol()] = phi
        phis_ = list(self.phis.values())
        for phi in phis_:
            new_args = []
            new_ps = []
            for i, (arg, p) in enumerate(zip(phi.args, phi.ps)):
                if arg.is_a([TEMP, ATTR]) and arg.symbol() in self.phis and phi != self.phis[arg.symbol()]:
                    inline_phi = self.phis[arg.symbol()]
                    new_args.extend(inline_phi.args)
                    for offs, ip in enumerate(inline_phi.ps):
                        new_p = reduce_relexp(RELOP('And', p, ip))
                        new_ps.append(new_p)
                else:
                    new_args.append(arg)
                    new_ps.append(p)
            phi.args = new_args
            phi.ps = new_ps