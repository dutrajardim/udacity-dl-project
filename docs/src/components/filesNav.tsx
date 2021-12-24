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
                    <Link className='nav-link' to={`/python-files/${value.slice(0, -3)}`}>
                        {path}
                    </Link>
                </li>
            )
        
        return (
            <li key={idx}>
                <div className='fw-bold'>+ {path}</div>
                <ul className='nav flex-column ps-3'>
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
        <div className="d-flex align-items-start me-3">
            <ul className="nav flex-column">{createList(tree)}</ul>
        </div>
    )
}