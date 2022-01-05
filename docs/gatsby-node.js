const path = require('path')
exports.createPages = async ({ graphql, actions, reporter }) => {
    const { createPage } = actions

    const result = await graphql(`
        query {
            allFile(filter: {extension: {eq: "py"}}) {
                files: nodes {
                    relativePath
                    name
                    fields {
                        pythonComment
                    }
                    functions: childrenPythonFunctionDescription {
                        name
                        line
                        docstring {
                            arguments
                            description
                            returns
                        }
                    }
                }
            }
            site {
                siteMetadata {
                    githubProjectUrl
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
            path: `files/${file.relativePath.slice(0, -3)}`,
            component: pythonFileTemplate,
            context: { file, site: result.data.site }
        })
    })
}

exports.onCreateWebpackConfig = ({ stage, loaders, actions }) => {
    if (stage === 'build-html') {
        actions.setWebpackConfig({
            module: {
                rules: [
                    {
                        test: /plotly.js/,
                        use: loaders.null(),
                    },
                ],
            },
        });
    }
};