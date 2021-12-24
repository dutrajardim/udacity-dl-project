import React from 'react'
import { PageProps } from 'gatsby'

import Layout from '../components/layout'
import FilesNav from '../components/filesNav'

interface PythonFile {
    name,
    fields?: {
        pythonComment: string
    },
    functions: [{
        name: string,
        docstring: {
            description: string,
            arguments: string,
            returns: string
        }
    }]
}

export default function PythonFile({ pageContext }: PageProps) {
    pageContext
    const { file } = (pageContext as { file: PythonFile })

    return (
        <Layout>
            <>
                <div className="row">
                    <div className="col col-md-3">
                        <FilesNav />
                    </div>
                    <div className="col col-md-9 card p-5 shadow rounded ">
                        <div className='row'>
                            <div className="col">
                                <h2>{file.name}</h2>
                                <div className="span">{file.fields?.pythonComment}</div>
                            </div>
                        </div>
                        {file.functions.map((func, idx) => (
                            <div className="row" key={idx}>
                                <h3>{func.name}</h3>
                                <dl>
                                    <dt>Description:</dt>
                                    <dd>{func.docstring.description}</dd>
                                    <dt>Arguments:</dt>
                                    <dd>{func.docstring.arguments}</dd>
                                    <dt>Returns:</dt>
                                    <dd>{func.docstring.returns}</dd>
                                </dl>
                            </div>
                        ))}
                    </div>
                </div>
            </>

        </Layout>
    )
}