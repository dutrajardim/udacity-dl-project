import { FuncdefContext } from '../antlr/Python3Parser'
import { Python3Listener } from '../antlr/Python3Listener'

interface ListenerArgs {
    funcdefCallback: (arg: FuncdefContext) => void
}

export class DocstringListener implements Python3Listener {
    private funcdefCallback 

    constructor({ funcdefCallback }: ListenerArgs) {
        this.funcdefCallback = funcdefCallback
    }

    enterFuncdef (ctx: FuncdefContext) {
        this.funcdefCallback(ctx)
    }
}