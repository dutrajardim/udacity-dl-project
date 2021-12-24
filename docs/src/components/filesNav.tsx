import React from 'react'
import * as _ from 'lodash'
import { useStaticQuery, graphql, Link } from 'gatsby'

const gql = graphql`
    query {
        allFile(filter: {extension: {eq: "py"}}) {
            nodes { relativePath }
        }
    }
`

function createList (obj) {
    const arr = Object.entries(obj)
    return arr.map(([path, value], idx) => {
        if (typeof(value) === 'string')
            return (
                <li key={idx}>
                    <Link className='nav-link ps-0 p-1 text-truncate' to={`/python-files/${value.slice(0, -3)}`}>
                        <i className="bi bi-file-code pe-2"></i>{path}
                    </Link>
                </li>
            )
        
        return (
            <li key={idx}>
                <div className='fw-bold text-truncate mt-3'>
                    <i className="bi bi-folder2-open pe-2"></i>{path}
                </div>
                <ul className='nav flex-column ps-3 ms-2 mt-1 border-start'>
                    {createList(value)}
                </ul>
            </li>
        )
    })
}

export default function FilesNav () {
    const { allFile } = useStaticQuery(gql)

    const tree = {}
    allFile.nodes.forEach(({relativePath}) => _.set(tree, relativePath.split('/'), relativePath))

    return (
        <div className="d-flex align-items-start ms-3">
            <ul className="nav flex-column">{createList(tree)}</ul>
        </div>
    )
}