import React from 'react'
import { useStaticQuery, graphql, Link } from 'gatsby'
import { capitalizeFirstLetter } from '../helpers'

const gql = graphql`
    query {
        allFile(filter: {extension: {eq: "py"}}) {
            nodes { relativePath }
        }
    }
`

export default function FilesNav () {
    const { allFile } = useStaticQuery(gql)
    const getName = (path) => 
        (path.slice(0, -3)
            .split('/') // @ts-ignore
            .map(word => capitalizeFirstLetter(word).replaceAll("_", " ")))
            .join(' > ')

    return (
        <div className="d-flex align-items-start">
            <div className="nav flex-column me-3" aria-orientation="vertical">
                {allFile.nodes.map(({relativePath}, idx) => (
                    <li className="nav-item" key={idx}>
                        <Link className='nav-link active' to={`/python-files/${relativePath.slice(0, -3)}`}>{getName(relativePath)}</Link>
                    </li>
                ))}
            </div>
        </div>
    )
}