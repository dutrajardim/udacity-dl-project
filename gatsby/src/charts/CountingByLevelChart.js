import React from 'react'

import { useStaticQuery, graphql } from "gatsby"
import Plot from "react-plotly.js"


const gql = graphql`
    query LevelWeekdayArtistCube {
        countByLevel: allOlapLevelWeekdayArtists(
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

const capitalizeFirstLetter = (string) => string.charAt(0).toUpperCase() + string.slice(1);

export default function CountingByLevelChart() {
    const resp = useStaticQuery(gql)

    const countByLevel = resp.countByLevel.edges.reduce((acc, { node }) => ({ ...acc, [node.level]: node.count }), {})

    const levelTrace = {
        type: 'pie',
        values: Object.values(countByLevel),
        labels: Object.keys(countByLevel).map(capitalizeFirstLetter),
    }

    return (
        <Plot
            data={[levelTrace]}
            layout={{ title: 'Count by level', width: 350 }} />
    )
}