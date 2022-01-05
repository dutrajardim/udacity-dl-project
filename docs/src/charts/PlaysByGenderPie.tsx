import React from 'react'
import { useStaticQuery, graphql } from 'gatsby'
// import Plot from 'react-plotly.js'
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
    query {
        data: allOlapYaerWeekGender(
            filter: {week: {eq: null}, year: {eq: null}, gender: {ne: null}}
        ) {
            edges {
                node {
                    count
                    gender
                }
            }
        }
    }
`

const labelsMap = {
    'F': 'Female',
    'M': 'Male',
    'unknown': 'Anonymous'
}

export default function PlaysByGenderPie() {
    const resp = useStaticQuery(gql)
    const reducer = (acc, { node }) => ([[...acc[0], node.gender], [...acc[1], node.count]])
    const [labels, values] = resp.data.edges.reduce(reducer, [[], []])

    const countingTrace = {
        type: 'pie',
        values: values,
        labels: labels.map(v => labelsMap[v])
    }

    let layout = {
        autosize: true,
        margin: { t: 30, b: 0, r: 10, l: 10 },
        legend: { orientation: "h" }
    }

    return (
        // @ts-ignore
        <Plot
            data={[countingTrace]}
            layout={layout}
            useResizeHandler={true}
            style={{ width: '100%', height: '100%', maxHeight: '200px' }} />
    )
}