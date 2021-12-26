import { CreateNodeArgs } from 'gatsby'
import { CharStreams, CommonTokenStream } from 'antlr4ts'
import { Python3Lexer } from './antlr/Python3Lexer'
import { Python3Parser } from './antlr/Python3Parser'
import { DocstringListener } from './listeners/DocstringListener'
import { Python3Listener } from './antlr/Python3Listener'
import { ParseTreeWalker } from 'antlr4ts/tree/ParseTreeWalker'


exports.onCreateNode = async (args: CreateNodeArgs) => {
    const {
        node, 
        loadNodeContent, 
        actions: { createNode, createParentChildLink, createNodeField },
        createNodeId,
        createContentDigest
    } = args

    if (node.extension !== 'py') return

    const content = await loadNodeContent(node)
     
    let chars = CharStreams.fromString(content)
    let lexer = new Python3Lexer(chars)
    let tokens = new CommonTokenStream(lexer)
    let parser = new Python3Parser(tokens)

    const parseTree = parser.file_input()

    const listener: Python3Listener = new DocstringListener({
        fileInputCallback: (ctx) => {
            const reComment = new RegExp(`^[\s\n]*"""(.+?)(?=""").*`, 's')
            let metches = ctx.text.match(reComment)
            if (metches) {
                createNodeField({
                    node,
                    name: "pythonComment",
                    value: metches[1].trim()
                })
            }
        },
        funcdefCallback: (ctx) => {
            const description = {
                name: ctx.NAME().text,
                line: ctx.start.line,
                docstring: { description: '', arguments: '', returns: '' }
            }

            const reComment = new RegExp(`(?=""")(.+?)(?=""")`, 's')
            const reCommentParam = new RegExp(`(.*)(Description|Arguments|Returns)\s{0,3}:(.*)`, 'si')

            let matches = ctx.text.match(reComment)
            let comments = matches && matches.length > 0 ? matches[1] : null
            
            while (comments) {
                matches = comments.match(reCommentParam)
                if (matches) {
                    comments = matches[1]
                    // @ts-ignore: The key validation is ensured by the regex expression
                    description.docstring[matches[2].toLocaleLowerCase()] = matches[3].trim()
                }
                else comments = ''
            }
    
            const descriptionNode = {
                ...description,
                id: createNodeId(`${node.id} >> ${description.name}`),
                children: [],
                parent: node.id,
                internal: {
                    contentDigest: createContentDigest(description),
                    type: `PythonFunctionDescription`
                }
            }

            createNode(descriptionNode)
            createParentChildLink({ parent: node, child: descriptionNode })
        }
    })

    ParseTreeWalker.DEFAULT.walk(listener, parseTree)
}