import React from 'react'
import { PageProps } from 'gatsby'

import Layout from '../components/layout'
import FilesNav from '../components/filesNav'

interface PythonFile {
    name
    functions: [{
        name: string,
        docstring: {
            description: string,
            args: string,
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
                    <div className="col col-md-5">
                        <FilesNav />
                    </div>
                    <div className="col col-md-7">
                        <div className='row'>
                            <div className="col"><h2>{file.name}</h2></div>
                        </div>
                        {file.functions.map((func, idx) => (
                            <div className="row" key={idx}>
                                <h3>{func.name}</h3>
                                <dl>
                                    <dt>Description:</dt>
                                    <dd>{func.docstring.description}</dd>
                                    <dt>Args:</dt>
                                    <dd>{func.docstring.args}</dd>
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