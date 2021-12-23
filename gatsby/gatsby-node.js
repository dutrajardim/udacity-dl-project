const path = require('path')
exports.createPages = async ({ graphql, actions, reporter }) => {
    const { createPage } = actions

    const result = await graphql(`
        query {
            allFile(filter: {extension: {eq: "py"}}) {
                files: nodes {
                    relativePath
                    name
                    functions: childrenPythonFunctionDescription {
                        name
                        docstring {
                            args
                            description
                            returns
                        }
                    }
                }
            }
        }
    `)
 
    if (result.errors) {
        reporter.panicOnBuild(`Error while running Graphql query.`)
        return
    }

    const pythonFileTemplate = path.resolve('src/templates/pythonFile.tsx')

    result.data.allFile.files.forEach(file => {
        createPage({
            path: `python-files/${file.relativePath.slice(0,-3)}`,
            component: pythonFileTemplate,
            context: { file }
        })
    })
}