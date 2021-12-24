import { File_inputContext, FuncdefContext } from '../antlr/Python3Parser'
import { Python3Listener } from '../antlr/Python3Listener'

interface ListenerArgs {
    funcdefCallback: (arg: FuncdefContext) => void,
    fileInputCallback: (arg: File_inputContext) => void
}

export class DocstringListener implements Python3Listener {
    private funcdefCallback 
    private fileInputCallback
    
    constructor({ funcdefCallback, fileInputCallback}: ListenerArgs) {
        this.funcdefCallback = funcdefCallback
        this.fileInputCallback = fileInputCallback
    }

    enterFuncdef (ctx: FuncdefContext) {
        this.funcdefCallback(ctx)
    }

    enterFile_input (ctx: File_inputContext) {
        this.fileInputCallback(ctx)
    }
}