import React from 'react'
import { PageProps } from 'gatsby'
import * as _ from 'lodash'

import Layout from '../components/layout'
import FilesNav from '../components/filesNav'

interface PythonFile {
    relativePath: string,
    name: string,
    fields?: {
        pythonComment: string
    },
    functions: [{
        name: string,
        line: number,
        docstring: {
            description: string,
            arguments: string,
            returns: string
        }
    }]
}

export default function PythonFile({ pageContext }: PageProps) {
    pageContext
    const { file, site } = (pageContext as { file: PythonFile, site: { siteMetadata: { githubProjectUrl: string } } })

    return (
        <Layout>
            <>
                <div className="row">
                    <div className="col-12 col-md-3 mb-5 order-md-2">
                        <FilesNav />
                    </div>
                    <div className="col-12 col-md-9 order-md-1">
                        <div className='row pb-3'>
                            <div className="col">
                                <h2>{_.capitalize(file.name.replace(/_/g, " "))}</h2>
                                <small className="text-muted">
                                    <i className="bi bi-file-code pe-2"></i>{file.relativePath}
                                </small>
                                <div className="my-3">{file.fields?.pythonComment}</div>
                            </div>
                        </div>
                        {file.functions.map((func, idx) => (
                            <div className="border-start border-3 px-4 mb-5" key={idx}>
                                <h3 className="mb-4"><i className="bi bi-cpu pe-3"></i>{func.name}</h3>
                                <dl>
                                    <dt>Description:</dt>
                                    <dd>{func.docstring.description}</dd>
                                    <dt>Arguments:</dt>
                                    <dd>{func.docstring.arguments}</dd>
                                    <dt>Returns:</dt>
                                    <dd>{func.docstring.returns}</dd>
                                </dl>
                                <a className="link-primary" target="_blank" href={`${site.siteMetadata.githubProjectUrl}/${file.relativePath}#L${func.line}`}>
                                    <i className="bi bi-github pe-2"></i>View on Github
                                </a>
                            </div>
                        ))}
                    </div>
                </div>
            </>

        </Layout>
    )
}