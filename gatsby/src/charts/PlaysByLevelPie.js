import React from 'react'
import { useStaticQuery, graphql } from "gatsby"
import Plot from "react-plotly.js"

import { capitalizeFirstLetter } from "../helpers"

const gql = graphql`
    query LevelWeekdayArtistCube {
        data: allOlapLevelWeekdayArtists(
            filter: {name: {eq: null}, weekday: {eq: null}, level: {ne: null}}
        ) {
            edges {
                node {
                    level
                    count
                }
            }
        }
    }
`

export default function PlaysByLevelPie() {
    const resp = useStaticQuery(gql)
    const reducer = (acc, { node }) => ([[...acc[0], node.level], [...acc[1], node.count]])
    const [labels, values] = resp.data.edges.reduce(reducer, [[], []])

    const levelTrace = {
        type: 'pie',
        values,
        labels: labels.map(capitalizeFirstLetter),
    }

    return (
        <Plot
            data={[levelTrace]}
            layout={{ title: 'Count by level', width: 350 }} />
    )
}