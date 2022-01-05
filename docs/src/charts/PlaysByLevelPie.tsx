import React from 'react'
import { useStaticQuery, graphql } from "gatsby"
// import Plot from "react-plotly.js"

import * as _ from 'lodash'
import Loadable from 'react-loadable'

const Plot = Loadable({
    loader: () => import('react-plotly.js'),
    loading: () => (
        <div className="d-flex justify-content-center align-items-center" style={{ height: 200 }}>
            <div className='loader'></div>
        </div>
    ),
});

const gql = graphql`
    query LevelWeekdayArtistCube {
        data: allOlapLevelWeekdayName(
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
        labels: labels.map(_.capitalize)
    }

    let layout = {
        autosize: true,
        margin: { t: 30, b: 0, r: 10, l: 10 },
        legend: { orientation: "h" }
    }

    return (
        // @ts-ignore
        <Plot
            data={[levelTrace]}
            layout={layout}
            useResizeHandler={true}
            style={{ width: '100%', height: '100%', maxHeight: '200px' }} />
    )
}